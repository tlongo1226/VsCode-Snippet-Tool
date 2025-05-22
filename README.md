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
