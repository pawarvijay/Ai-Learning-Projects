# 01. Variables & Types (JS vs Python)

## Primitive Types
```python
# JavaScript                      # Python
let name = "Alex";                name = "Alex"           # str
let age = 30;                     age = 30                # int
let price = 19.99;                price = 19.99           # float
let isActive = true;              is_active = True        # bool (Capital T/F)
let data = null;                  data = None             # NoneType
let undef;                        # No 'undefined' in Python (raises NameError)
```

## String Interpolation (Template Literals)
```python
# JS: `User ${name} is ${age} years old`
msg = f"User {name} is {age} years old"
```

## Type Conversions
```python
# JS: Number("42"), String(42), Boolean(1)
num = int("42")
text = str(42)
flag = bool(1)
```

## Type Hinting (TypeScript Equivalent)
```python
# TypeScript                      # Python 3.10+
let score: number = 100;          score: int = 100
let tags: string[] = ["a", "b"];  tags: list[str] = ["a", "b"]
let user: { id: number };         user: dict[str, int] = {"id": 1}
```\n