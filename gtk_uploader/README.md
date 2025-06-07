# GTK Movie Uploader

This small GUI program allows you to append entries to
[`movies.json`](https://github.com/Kgkkjjj/shows-/blob/main/movies.json`).
It fetches the existing file from GitHub, adds a new movie entry, and
saves the result locally. If you set a `GITHUB_TOKEN` environment variable,
you can extend the code to upload the modified file back to GitHub using the
REST API.

## Building

Make sure `gtk+-3.0`, `libcurl`, and `jansson` development packages are
installed. Then run:

```bash
make
```

This produces an executable named `uploader`.

## Running

Execute the binary and fill in the title, path, and size fields. Clicking
**Upload** downloads the current JSON file, appends your entry, and writes the
updated file to `movies.json`. Uploading to GitHub requires additional logic
and a personal access token set in `GITHUB_TOKEN`.
