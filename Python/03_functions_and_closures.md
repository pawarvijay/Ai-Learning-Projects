# 03. Functions & Scope (JS vs Python)

## Basic Function Definition
```python
# JS: function add(a, b = 10) { return a + b; }
def add(a: int, b: int = 10) -> int:
    return a + b
```

## Arrow Functions (Lambdas)
```python
# JS: const square = x => x * x;
square = lambda x: x * x
```

## Rest & Spread Parameters (*args, **kwargs)
```python
# JS Rest: function logAll(first, ...rest) { }
def log_all(first, *args):
    print(first, args)  # args is a tuple

# JS Spread: const merged = { ...obj1, ...obj2 };
merged = {**obj1, **obj2}

# Passing arbitrary named options (JS options object)
# JS: function config({ host, port, ...rest })
def config(**kwargs):
    print(kwargs.get("host"))  # kwargs is a dict
```

## Destructuring Return Values (Multiple Returns)
```python
# JS: const [status, data] = getResult();
def get_result():
    return 200, {"id": 1}  # Returns tuple

status, data = get_result()
```

## Decorators (Higher-Order Functions / Express Middleware)
```python
import functools

def log_execution(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@log_execution
def fetch_user(user_id):
    return {"id": user_id}
```\n