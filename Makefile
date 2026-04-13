CC      = gcc
CFLAGS  = -Wall -Wextra -Wpedantic -std=c11 -O2
TARGET  = server
SRC     = server.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
