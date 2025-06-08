#include <gtk/gtk.h>
#include <jansson.h>
#include <curl/curl.h>

/* Helper structure to hold downloaded data */
typedef struct {
    GString *str;
} Buffer;

static size_t write_cb(void *ptr, size_t size, size_t nmemb, void *userdata) {
    Buffer *buf = (Buffer *)userdata;
    g_string_append_len(buf->str, ptr, size * nmemb);
    return size * nmemb;
}

static GtkWidget *title_entry;
static GtkWidget *path_entry;
static GtkWidget *size_entry;

static void on_upload_clicked(GtkButton *button, gpointer user_data) {
    const char *title = gtk_entry_get_text(GTK_ENTRY(title_entry));
    const char *path = gtk_entry_get_text(GTK_ENTRY(path_entry));
    const char *size_text = gtk_entry_get_text(GTK_ENTRY(size_entry));
    double size = g_ascii_strtod(size_text, NULL);

    CURL *curl = curl_easy_init();
    Buffer buf = { g_string_new(NULL) };

    curl_easy_setopt(curl, CURLOPT_URL, "https://raw.githubusercontent.com/Kgkkjjj/shows-/main/movies.json");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buf);
    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) {
        g_warning("Failed to fetch movies.json: %s", curl_easy_strerror(res));
        g_string_free(buf.str, TRUE);
        return;
    }

    json_error_t jerr;
    json_t *root = json_loads(buf.str->str, 0, &jerr);
    g_string_free(buf.str, TRUE);

    if (!root || !json_is_array(root)) {
        g_warning("Invalid JSON format: %s", jerr.text);
        if(root) json_decref(root);
        return;
    }

    json_t *item = json_pack("{s:s,s:s,s:f}",
                             "title", title,
                             "path", path,
                             "size_mb", size);
    json_array_append_new(root, item);

    char *out = json_dumps(root, JSON_INDENT(2));
    json_decref(root);

    /* Save updated file locally */
    g_file_set_contents("movies.json", out, -1, NULL);

    const char *token = g_getenv("GITHUB_TOKEN");
    if (token && *token) {
        /*
         * TODO: Implement GitHub API upload with token.
         * This typically involves a PUT request to
         * https://api.github.com/repos/Kgkkjjj/shows-/contents/movies.json
         * with appropriate JSON payload containing the new file content
         * and commit message.
         */
        g_message("Token found. Upload logic not implemented in this example.");
    } else {
        g_message("GITHUB_TOKEN not set. Saved movies.json locally only.");
    }

    g_free(out);
}

int main(int argc, char **argv) {
    gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Movie Uploader");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);

    GtkWidget *grid = gtk_grid_new();
    gtk_grid_set_row_spacing(GTK_GRID(grid), 5);
    gtk_grid_set_column_spacing(GTK_GRID(grid), 5);
    gtk_container_add(GTK_CONTAINER(window), grid);

    GtkWidget *title_label = gtk_label_new("Title:");
    title_entry = gtk_entry_new();
    gtk_grid_attach(GTK_GRID(grid), title_label, 0, 0, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), title_entry, 1, 0, 1, 1);

    GtkWidget *path_label = gtk_label_new("Path:");
    path_entry = gtk_entry_new();
    gtk_grid_attach(GTK_GRID(grid), path_label, 0, 1, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), path_entry, 1, 1, 1, 1);

    GtkWidget *size_label = gtk_label_new("Size MB:");
    size_entry = gtk_entry_new();
    gtk_grid_attach(GTK_GRID(grid), size_label, 0, 2, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), size_entry, 1, 2, 1, 1);

    GtkWidget *upload_btn = gtk_button_new_with_label("Upload");
    g_signal_connect(upload_btn, "clicked", G_CALLBACK(on_upload_clicked), NULL);
    gtk_grid_attach(GTK_GRID(grid), upload_btn, 0, 3, 2, 1);

    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(window);
    gtk_main();
    return 0;
}
