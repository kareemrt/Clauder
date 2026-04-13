/*
 * server.c — A minimal HTTP/1.1 web server in C
 *
 * Build:  make
 * Run:    ./server [port]   (default port: 8080)
 */

#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <limits.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define DEFAULT_PORT   8080
#define BACKLOG        10
#define BUF_SIZE       8192
#define PATH_MAX_LEN   512
#define MAX_FILE_SIZE  (16 * 1024 * 1024)  /* 16 MiB file size limit */

/* Silence warn_unused_result on write() — we do best-effort I/O */
#define WRITE_IGNORE(fd, buf, len) \
    do { ssize_t _r = write((fd), (buf), (len)); (void)_r; } while (0)

/* ------------------------------------------------------------------ */
/* Helpers                                                              */
/* ------------------------------------------------------------------ */

static void die(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fputc('\n', stderr);
    exit(EXIT_FAILURE);
}

/* RFC 1123 date string into buf (must be ≥ 30 bytes) */
static void http_date(char *buf, size_t len)
{
    time_t now = time(NULL);
    struct tm *gmt = gmtime(&now);
    strftime(buf, len, "%a, %d %b %Y %H:%M:%S GMT", gmt);
}

/* ------------------------------------------------------------------ */
/* MIME types                                                           */
/* ------------------------------------------------------------------ */

static const struct { const char *ext; const char *mime; } mime_map[] = {
    { "html", "text/html; charset=utf-8"       },
    { "htm",  "text/html; charset=utf-8"       },
    { "css",  "text/css"                        },
    { "js",   "application/javascript"          },
    { "json", "application/json"                },
    { "png",  "image/png"                       },
    { "jpg",  "image/jpeg"                      },
    { "jpeg", "image/jpeg"                      },
    { "gif",  "image/gif"                       },
    { "ico",  "image/x-icon"                    },
    { "svg",  "image/svg+xml"                   },
    { "txt",  "text/plain; charset=utf-8"       },
    { NULL,   "application/octet-stream"        },
};

static const char *mime_for(const char *path)
{
    const char *dot = strrchr(path, '.');
    if (dot) {
        ++dot;
        for (int i = 0; mime_map[i].ext; ++i)
            if (strcasecmp(dot, mime_map[i].ext) == 0)
                return mime_map[i].mime;
    }
    return "application/octet-stream";
}

/* ------------------------------------------------------------------ */
/* Response sending                                                     */
/* ------------------------------------------------------------------ */

static void send_response(int fd, int status, const char *status_text,
                           const char *content_type, const char *body,
                           size_t body_len)
{
    char date[32];
    http_date(date, sizeof date);

    char header[1024];
    int hlen = snprintf(header, sizeof header,
        "HTTP/1.1 %d %s\r\n"
        "Date: %s\r\n"
        "Server: Clauder/1.0\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n",
        status, status_text, date, content_type, body_len);

    /* Ignore partial-write errors on the header — best effort */
    WRITE_IGNORE(fd, header, (size_t)hlen);
    if (body && body_len > 0)
        WRITE_IGNORE(fd, body, body_len);
}

static void send_error(int fd, int status, const char *status_text)
{
    char body[256];
    int blen = snprintf(body, sizeof body,
        "<!DOCTYPE html><html><body><h1>%d %s</h1></body></html>\n",
        status, status_text);
    send_response(fd, status, status_text,
                  "text/html; charset=utf-8", body, (size_t)blen);
}

/* ------------------------------------------------------------------ */
/* Serve a file from the filesystem                                     */
/* ------------------------------------------------------------------ */

static void serve_file(int fd, const char *path)
{
    FILE *f = fopen(path, "rb");
    if (!f) {
        if (errno == EACCES)
            send_error(fd, 403, "Forbidden");
        else
            send_error(fd, 404, "Not Found");
        return;
    }

    struct stat st;
    if (fstat(fileno(f), &st) != 0 || !S_ISREG(st.st_mode)) {
        fclose(f);
        send_error(fd, 403, "Forbidden");
        return;
    }

    size_t file_size = (size_t)st.st_size;
    if (file_size > MAX_FILE_SIZE) {
        fclose(f);
        send_error(fd, 413, "Content Too Large");
        return;
    }
    char *buf = malloc(file_size);
    if (!buf) {
        fclose(f);
        send_error(fd, 500, "Internal Server Error");
        return;
    }

    if (fread(buf, 1, file_size, f) != file_size) {
        free(buf);
        fclose(f);
        send_error(fd, 500, "Internal Server Error");
        return;
    }
    fclose(f);

    send_response(fd, 200, "OK", mime_for(path), buf, file_size);
    free(buf);
}

/* ------------------------------------------------------------------ */
/* Default index page (served when no files exist)                     */
/* ------------------------------------------------------------------ */

static const char INDEX_HTML[] =
    "<!DOCTYPE html>\n"
    "<html lang=\"en\">\n"
    "<head><meta charset=\"utf-8\"><title>Clauder</title></head>\n"
    "<body>\n"
    "<h1>Welcome to Clauder Web Server</h1>\n"
    "<p>Place your files in the server's working directory.</p>\n"
    "</body>\n"
    "</html>\n";

/* ------------------------------------------------------------------ */
/* Request parsing and dispatch                                         */
/* ------------------------------------------------------------------ */

/*
 * Sanitise a URL path so it cannot escape the working directory.
 * Uses realpath() to resolve the canonical path and confirms it remains
 * within the server's working directory.
 * Returns 0 on success (out is set to the relative path), -1 if unsafe.
 */
static int sanitise_path(const char *url_path, char *out, size_t out_len)
{
    /* Strip leading slash; serve relative to cwd */
    const char *p = url_path;
    while (*p == '/')
        ++p;

    /* Empty path → index.html */
    if (*p == '\0')
        p = "index.html";

    /* Reject any path component containing ".." (fast pre-check) */
    if (strstr(p, ".."))
        return -1;

    if (strlen(p) >= out_len)
        return -1;

    /* Resolve cwd to its canonical form */
    char *cwd = realpath(".", NULL);
    if (!cwd)
        return -1;

    /* Build absolute path = cwd + "/" + p */
    size_t abs_len = strlen(cwd) + 1 + strlen(p) + 1;
    char *abs_request = malloc(abs_len);
    if (!abs_request) {
        free(cwd);
        return -1;
    }
    snprintf(abs_request, abs_len, "%s/%s", cwd, p);

    /* Resolve the canonical path (resolves symlinks, .., etc.) */
    char *resolved = realpath(abs_request, NULL);
    free(abs_request);

    if (!resolved) {
        /*
         * File doesn't exist yet — realpath() fails for non-existent paths
         * on some systems.  The ".." pre-check above is sufficient in this
         * case; allow the path through so the caller can return 404.
         */
        snprintf(out, out_len, "%s", p);
        free(cwd);
        return 0;
    }

    /* Verify the resolved path starts with cwd */
    size_t cwd_len = strlen(cwd);
    if (strncmp(resolved, cwd, cwd_len) != 0 ||
        (resolved[cwd_len] != '/' && resolved[cwd_len] != '\0')) {
        free(resolved);
        free(cwd);
        return -1;
    }
    free(cwd);

    /* Return the relative portion */
    const char *rel = resolved + cwd_len;
    while (*rel == '/')
        ++rel;

    if (strlen(rel) >= out_len) {
        free(resolved);
        return -1;
    }

    snprintf(out, out_len, "%s", rel);
    free(resolved);
    return 0;
}

static void handle_client(int fd)
{
    char buf[BUF_SIZE];
    ssize_t nread = read(fd, buf, sizeof buf - 1);
    if (nread <= 0)
        return;
    buf[nread] = '\0';

    /* Parse the request line: METHOD SP path SP HTTP/... */
    char method[16], url[PATH_MAX_LEN], proto[16];
    if (sscanf(buf, "%15s %511s %15s", method, url, proto) != 3) {
        send_error(fd, 400, "Bad Request");
        return;
    }

    /* Only GET and HEAD are supported */
    int is_head = (strcasecmp(method, "HEAD") == 0);
    if (strcasecmp(method, "GET") != 0 && !is_head) {
        send_error(fd, 405, "Method Not Allowed");
        return;
    }

    /* Strip query string */
    char *q = strchr(url, '?');
    if (q) *q = '\0';

    char path[PATH_MAX_LEN];
    if (sanitise_path(url, path, sizeof path) != 0) {
        send_error(fd, 400, "Bad Request");
        return;
    }

    printf("%s %s\n", method, url);
    fflush(stdout);

    /* Try to open the requested file */
    struct stat st;
    int exists = (stat(path, &st) == 0 && S_ISREG(st.st_mode));

    if (!exists && strcmp(path, "index.html") == 0) {
        /* No index.html → serve built-in welcome page */
        if (!is_head)
            send_response(fd, 200, "OK",
                          "text/html; charset=utf-8",
                          INDEX_HTML, sizeof INDEX_HTML - 1);
        else
            send_response(fd, 200, "OK",
                          "text/html; charset=utf-8",
                          NULL, sizeof INDEX_HTML - 1);
        return;
    }

    if (!exists) {
        send_error(fd, 404, "Not Found");
        return;
    }

    if (!is_head)
        serve_file(fd, path);
    else {
        /* HEAD: send headers only */
        char date[32];
        http_date(date, sizeof date);
        char header[512];
        int hlen = snprintf(header, sizeof header,
            "HTTP/1.1 200 OK\r\n"
            "Date: %s\r\n"
            "Server: Clauder/1.0\r\n"
            "Content-Type: %s\r\n"
            "Content-Length: %lld\r\n"
            "Connection: close\r\n"
            "\r\n",
            date, mime_for(path), (long long)st.st_size);
        WRITE_IGNORE(fd, header, (size_t)hlen);
    }
}

/* ------------------------------------------------------------------ */
/* Main                                                                 */
/* ------------------------------------------------------------------ */

static volatile sig_atomic_t g_running = 1;

static void on_signal(int sig)
{
    (void)sig;
    g_running = 0;
}

int main(int argc, char *argv[])
{
    int port = DEFAULT_PORT;
    if (argc == 2) {
        char *end;
        long lport = strtol(argv[1], &end, 10);
        if (*end != '\0' || lport <= 0 || lport > 65535)
            die("Invalid port: %s", argv[1]);
        port = (int)lport;
    }

    /* Ignore SIGPIPE so writes to closed sockets don't kill the process */
    signal(SIGPIPE, SIG_IGN);
    signal(SIGINT,  on_signal);
    signal(SIGTERM, on_signal);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0)
        die("socket: %s", strerror(errno));

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof opt);

    struct sockaddr_in addr = {
        .sin_family      = AF_INET,
        .sin_port        = htons((uint16_t)port),
        .sin_addr.s_addr = INADDR_ANY,
    };

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof addr) < 0)
        die("bind: %s", strerror(errno));

    if (listen(server_fd, BACKLOG) < 0)
        die("listen: %s", strerror(errno));

    printf("Clauder web server listening on port %d\n", port);
    char cwd_buf[PATH_MAX];
    printf("Serving files from: %s\n",
           getcwd(cwd_buf, sizeof cwd_buf) ? cwd_buf : "(unknown)");
    fflush(stdout);

    while (g_running) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof client_addr;

        int client_fd = accept(server_fd,
                               (struct sockaddr *)&client_addr,
                               &client_len);
        if (client_fd < 0) {
            if (errno == EINTR)
                break;
            perror("accept");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof client_ip);
        printf("Connection from %s\n", client_ip);

        handle_client(client_fd);
        close(client_fd);
    }

    close(server_fd);
    printf("\nServer stopped.\n");
    return EXIT_SUCCESS;
}
