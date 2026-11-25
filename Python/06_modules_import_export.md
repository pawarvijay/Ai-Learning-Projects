# 06. Modules: Import & Export, Packages & Barrel Pattern (JS vs Python)

## 1. Concept Mapping
* In Python, **every `.py` file is automatically an exported module**.
* There is no explicit `export` keyword. Any top-level variable, function, or class in a file is importable.

---

## 2. Basic Exporting & Importing

### Defining Exports (`utils.py`)
```python
API_URL = "https://api.domain.com"

def format_date(d):
    return str(d)

class Logger:
    def log(self, msg):
        print(msg)
```

### Importing (`main.py`)
```python
# JS: import { format_date, API_URL } from './utils.js';
from utils import format_date, API_URL

# JS: import * as Utils from './utils.js';
import utils
utils.format_date(d)

# JS: import { Logger as CustomLogger } from './utils.js';
from utils import Logger as CustomLogger
```

---

## 3. Two Ways to Import from Nested Folders

Assume this directory structure:
```text
src/
├── main.py
└── mock_mcp/
    ├── __init__.py
    └── mock_mcp_tool.py   <-- Contains: def mock_mcp_tool_execute(...)
```

### Option A: Standard Direct Import (File Path)
Directly imports pointing to the specific file.
```python
# JS equivalent: import { mock_mcp_tool_execute } from './mock_mcp/mock_mcp_tool.js';
from mock_mcp.mock_mcp_tool import mock_mcp_tool_execute

mock_mcp_tool_execute("calc", {"price": 100})
```

### Option B: The "Barrel" Import via `__init__.py` (Advanced & Industry Standard)
Just like an `index.js` in Node.js, `__init__.py` bundles and re-exports items so consumers don't need to know internal file names.

1. **Inside `mock_mcp/__init__.py` (The Receptionist):**
   ```python
   # Re-export from internal file to folder level
   from .mock_mcp_tool import mock_mcp_tool_execute

   # Explicit public API whitelist
   __all__ = ["mock_mcp_tool_execute"]
   ```

2. **Inside `main.py` (Clean Consumer):**
   ```python
   # JS equivalent: import { mock_mcp_tool_execute } from './mock_mcp';
   from mock_mcp import mock_mcp_tool_execute

   mock_mcp_tool_execute("calc", {"price": 100})
   ```

---

## 4. What is `__all__`? (The Public Whitelist)

`__all__ = ["func1", "func2"]` is a list of strings that defines the **explicit public contract** of a module:

* **Restricts Wildcards:** If someone runs `from mock_mcp import *`, Python will **ONLY** export what is inside `__all__`. Internal variables (`import os`, `API_SECRET`) stay private.
* **IDE Autocomplete:** Guides VS Code/PyCharm to suggest only intended public functions when typing `from mock_mcp import `.
* **Linters & CI:** Clean enterprise projects enforce `__all__` to prevent accidental namespace leakage.

---

## 5. The `if __name__ == '__main__':` Guard (Main Module Guard)

Prevents execution code from running when a file is imported by another file.

```python
def main():
    print("Application running directly!")

# In Node.js: if (require.main === module) { main(); }
# In Python:
if __name__ == "__main__":
    main()
```

| How file is used | Code inside `if __name__ == '__main__':` |
| :--- | :---: |
| **Run directly** (`python main.py`) | ✅ **Runs** (`__name__` is `"__main__"`) |
| **Imported** (`from main import app`) | ❌ **Skipped** (`__name__` is `"main"`) |
