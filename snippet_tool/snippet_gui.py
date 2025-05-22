import os
import sys
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
SNIPPET_DIR = os.path.join(BASE_DIR, "snippets")

# Ensure necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SNIPPET_DIR, exist_ok=True)

# Setup logging
log_file = os.path.join(LOG_DIR, "snippet_tool.log")
logger = logging.getLogger("snippet_tool")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)

def get_clipboard_lines():
    try:
        root = tk.Tk()
        root.withdraw()
        clipboard = root.clipboard_get()
        logger.info("Clipboard successfully read")
        return clipboard.splitlines()
    except Exception as e:
        logger.error(f"Clipboard read error: {e}")
        return ["# Failed to read clipboard: " + str(e)]

def escape_line(line):
    return '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '",'

def list_snippet_files():
    return [f for f in os.listdir(SNIPPET_DIR) if f.endswith(".code-snippets")]

class SnippetApp:
    def __init__(self, root):
        self.root = root
        root.title("Create VS Code Snippet")
        root.geometry("700x500")

        # Snippet file selection
        ttk.Label(root, text="Snippet File:").grid(row=0, column=0, sticky="w")
        self.snippet_file_var = tk.StringVar()
        self.snippet_file_menu = ttk.Combobox(root, textvariable=self.snippet_file_var, values=list_snippet_files(), width=50)
        self.snippet_file_menu.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(root, text="Browse...", command=self.browse_file).grid(row=0, column=2)

        # Name
        ttk.Label(root, text="Snippet Name:").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(root, width=50)
        self.name_entry.grid(row=1, column=1, columnspan=2, pady=5)

        # Prefix
        ttk.Label(root, text="Prefix:").grid(row=2, column=0, sticky="w")
        self.prefix_entry = ttk.Entry(root, width=50)
        self.prefix_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Scope
        ttk.Label(root, text="Scope:").grid(row=3, column=0, sticky="w")
        self.scope_entry = ttk.Entry(root, width=50)
        self.scope_entry.grid(row=3, column=1, columnspan=2, pady=5)

        # Body text area
        ttk.Label(root, text="Snippet Body:").grid(row=4, column=0, sticky="nw")
        self.body_text = tk.Text(root, height=15, width=80)
        self.body_text.grid(row=4, column=1, columnspan=2, pady=10)

        # Populate initial body
        self.set_initial_body()

        # Save button
        ttk.Button(root, text="Save Snippet", command=self.save_snippet).grid(row=5, column=1, pady=10)

        logger.info("Snippet GUI loaded")

    def browse_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".code-snippets",
            filetypes=[("Snippet Files", "*.code-snippets")],
            initialdir=SNIPPET_DIR
        )
        if filepath:
            # Store relative path from snippet dir
            if filepath.startswith(SNIPPET_DIR):
                filepath = os.path.relpath(filepath, SNIPPET_DIR)
            self.snippet_file_var.set(filepath)

    def set_initial_body(self):
        lines = get_clipboard_lines()
        escaped = [escape_line(line) for line in lines]
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert(tk.END, "\n".join(escaped))

    def save_snippet(self):
        filename = self.snippet_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please specify a snippet file.")
            logger.warning("Save attempted with no file specified")
            return

        name = self.name_entry.get().strip()
        prefix = self.prefix_entry.get().strip()
        scope = self.scope_entry.get().strip()
        body_lines = self.body_text.get("1.0", tk.END).strip().splitlines()

        if not name or not prefix:
            messagebox.showerror("Error", "Name and Prefix are required.")
            logger.warning("Missing name or prefix")
            return

        snippet_path = os.path.join(SNIPPET_DIR, filename)
        if not os.path.exists(snippet_path):
            data = {}
        else:
            try:
                with open(snippet_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {filename}: {e}")
                messagebox.showerror("Error", f"{filename} is not a valid JSON file.")
                return

        data[name] = {
            "prefix": prefix,
            "body": body_lines,
            "scope": scope,
            "description": name
        }

        with open(snippet_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info(f"Saved snippet '{name}' to {filename}")
        messagebox.showinfo("Saved", f"Snippet '{name}' saved to '{filename}'.")

def main():
    try:
        root = tk.Tk()
        app = SnippetApp(root)
        root.mainloop()
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
