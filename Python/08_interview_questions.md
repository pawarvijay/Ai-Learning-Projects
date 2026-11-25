# 08. Python Interview Questions (Node.js Dev Transition)

## 🟢 Beginner Level

### Q1: What is the difference between `list`, `tuple`, and `set`?
* **List (`[]`):** Ordered, mutable (can add/remove items), allows duplicates. (Like JS Array).
* **Tuple (`()`):** Ordered, **immutable** (read-only after creation), allows duplicates. Often used for dictionary keys or fixed records.
* **Set (`{}`):** Unordered, unique elements only. (Like JS `Set`).

### Q2: What is the difference between `==` and `is`?
* **`==`:** Equality check — checks if the **values** are equal (like JS `===`).
* **`is`:** Identity check — checks if both variables point to the exact same **memory address** (like checking `objA === objB` reference equality).

### Q3: How do default arguments work in Python functions, and what is the mutable default argument trap?
* **Trap:** Default arguments are evaluated **once when the function is defined**, not each time it is called.
* **Wrong:** `def append_to(item, target=[]): target.append(item)` (Shares the same list across all calls!).
* **Fix:** `def append_to(item, target=None): if target is None: target = []`

---

## 🟡 Intermediate Level

### Q4: Explain Python's GIL (Global Interpreter Lock). How does it affect async vs multi-threading?
* The **GIL** is a mutex that prevents multiple native threads from executing Python bytecodes at once in CPython.
* **Impact:** CPU-bound tasks cannot achieve true multi-core parallelism using threads (use `multiprocessing` instead).
* **I/O-bound tasks:** Network calls, database queries, and async I/O (`asyncio`) release the GIL, performing with high concurrency similar to Node.js.

### Q5: What are Generators and the `yield` keyword? How do they save memory?
* A function with `yield` produces an iterator that generates values **on demand (lazily)** rather than storing the entire list in RAM.
* Equivalent to JS Generator functions (`function*` and `yield`).

### Q6: How does error handling differ between JavaScript and Python?
```python
# JS: try { ... } catch (err) { ... } finally { ... }
# Python:
try:
    result = 10 / 0
except ZeroDivisionError as err:
    print(f"Error: {err}")
else:
    print("Runs ONLY if NO error occurred")
finally:
    print("Always runs")
```

---

## 🔴 Advanced Level

### Q7: What are Python Magic / Dunder Methods (`__init__`, `__str__`, `__call__`, `__enter__`)?
* Dunder (double-underscore) methods allow custom classes to hook into Python's native operators and lifecycle:
  * `__init__`: Constructor.
  * `__str__` / `__repr__`: String representations (like JS `.toString()`).
  * `__call__`: Allows an object instance to be called directly like a function `my_obj()`.
  * `__enter__` / `__exit__`: Context managers (used in `with open(...) as f:`).

### Q8: How does Python's `asyncio` compare to the Node.js Event Loop?
* **Node.js:** Single-threaded event loop built into the runtime engine (libuv) by default; all I/O is asynchronous out-of-the-box.
* **Python:** Event loop is an explicit opt-in module (`asyncio`). Synchronous blocking calls (e.g., `requests.get()` or `time.sleep()`) will **block the entire event loop** unless run in an executor or replaced with async libraries (`httpx.get()`, `asyncio.sleep()`).

### Q9: What is Monkey Patching in Python and when should it be avoided?
* Dynamically modifying a module or class at runtime.
* Common in testing/mocking libraries, but avoided in production business logic because it causes unpredictable side-effects.\n