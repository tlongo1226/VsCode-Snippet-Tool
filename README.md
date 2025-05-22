# Snippet Tool – Convert Code to VS Code Snippet JSON

This tool allows you to select code in your editor, copy it, press a keybinding(default=ctrl+alt+s), and transform the code into properly escaped snippet format for use in VS Code.

✅ **Features**
- GUI input for snippet name, prefix, scope, and editable snippet body
- Automatically escapes and formats selected code
- Supports adding to existing `.code-snippets` files
- Cross-platform: Works on Linux and Windows (Python standard library only)
- Includes logging with midnight rollover (in `logs/`)

---

## 🔧 Installation

Clone the repo:

```bash
git clone https://github.com/yourusername/snippet-tool.git
cd snippet-tool
```

### Example Folder Layout
```
snippet-tool/
├── snippet_tool/               # Python module for the GUI + snippet formatter
│   ├── __init__.py
│   ├── gui.py                  # ttk GUI for input
│   ├── converter.py            # Converts code to snippet format
│   ├── utils.py                # Reusable utilities (e.g., escaping, file handling)
│   └── logger.py               # Sets up midnight-rolling logger
│
├── logs/                       # Where logs are written to (created at runtime)
│
├── snippets/                   # Where generated snippet files are stored
│   └── example.code-snippets   # Example VS Code snippet file
│
├── tests/                      # Optional: Unit tests for modules
│   └── test_converter.py
│
├── requirements.txt            # If third-party libs are eventually allowed
├── LICENSE
├── .gitignore
├── README.md
└── run.py                      # Entrypoint (launches GUI)
```

### 🧩 Configure a VS Code Task
VS Code tasks let you run scripts with a single command. You'll use this to launch the Snippet Tool.

#### 📁 Step-by-Step
Open your project or workspace in VS Code.

Press Ctrl+Shift+P → select “Tasks: Configure Task”

Choose “Create tasks.json from template” → select “Others”

Replace the contents of .vscode/tasks.json with:

<details> <summary>📄 <strong>Example: <code>tasks.json</code></strong></summary>
### ✅ Windows (Python installed as python)
  
```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Snippet Tool",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/snippet-tool/run.py"
      ],
      "presentation": {
        "echo": true,
        "reveal": "silent",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

### 🐧 Linux/macOS (use python3)
```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Snippet Tool",
      "type": "shell",
      "command": "python3",
      "args": [
        "${workspaceFolder}/snippet-tool/run.py"
      ],
      "presentation": {
        "echo": true,
        "reveal": "silent",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```
</details>
✅ Replace the path to run.py if your folder structure is different.

### 🎹  Set Up a Custom Keybinding
Bind a key (like Ctrl+Alt+S) to trigger your task.

### 🧭 Instructions
1. Press Ctrl+Shift+P → select “Preferences: Open Keyboard Shortcuts (JSON)”
2. Add this block to the JSON array:
```
{
  "key": "ctrl+alt+s",
  "command": "workbench.action.tasks.runTask",
  "args": "Run Snippet Tool",
  "when": "editorTextFocus"
}
```


### 🧪  Using the Tool
Once set up:

Select a block of code in your editor

Press your custom keybinding (default: Ctrl+Alt+S)

The snippet tool GUI will launch

Edit and confirm the snippet content, and save it into a VS Code .code-snippets file



### 📦 Optional: Global Setup
If you want to use the tool across all projects:

Use an absolute path in tasks.json

Install the snippet tool in a consistent location (e.g., ~/snippet-tool or C:\Tools\snippet-tool)

Optionally create a script/alias to launch it from terminal or file explorer
