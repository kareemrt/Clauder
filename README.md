# Clauder
Claude Bot

## Web Server (C)

A lightweight HTTP/1.1 web server written in C that serves static files from its working directory.

### Features

- Serves static files (HTML, CSS, JS, images, …) from the current directory
- Built-in welcome page when no `index.html` is present
- `GET` and `HEAD` method support
- Automatic MIME-type detection
- Path traversal protection
- Configurable port via command-line argument

### Build

```bash
make
```

### Run

```bash
# Default port 8080
./server

# Custom port
./server 9000
```

### Usage

1. Start the server in any directory that contains your static files.
2. Open your browser at `http://localhost:8080` (or whatever port you chose).

### Clean

```bash
make clean
```
