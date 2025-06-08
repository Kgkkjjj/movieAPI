CC = gcc
CFLAGS = `pkg-config --cflags gtk+-3.0 libcurl jansson`
LIBS = `pkg-config --libs gtk+-3.0 libcurl jansson`

uploader: main.c
	$(CC) -o uploader main.c $(CFLAGS) $(LIBS)

clean:
	rm -f uploader
