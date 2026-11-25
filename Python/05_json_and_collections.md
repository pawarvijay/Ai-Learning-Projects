# 05. JSON & Array Manipulation (JS vs Python)

## Dictionaries vs Objects
```python
# JS Object: const user = { id: 1, name: "Alex" };
user = {"id": 1, "name": "Alex"}

# Access (Safe vs Direct)
# JS: user.id OR user["id"]
# Python:
direct = user["id"]           # Raises KeyError if missing
safe = user.get("age", 25)     # Returns default (25) if missing
```

## JSON Serialization
```python
import json

# JS: JSON.stringify(user)
json_str = json.dumps(user)

# JS: JSON.parse(json_str)
parsed_dict = json.loads(json_str)
```

## Array / List Operations
```python
items = ["a", "b", "c"]

# JS: items.push("d")
items.append("d")

# JS: items.pop()
items.pop()

# JS: items.includes("b")
if "b" in items:
    print("Found")

# JS: items.length
total = len(items)

# JS: items.slice(0, 2)
subset = items[0:2]
```

## Array of JSON Objects Manipulation
```python
users = [
    {"id": 1, "name": "Alice", "role": "admin", "age": 28},
    {"id": 2, "name": "Bob", "role": "user", "age": 34},
    {"id": 3, "name": "Charlie", "role": "user", "age": 22}
]

# 1. Filter (JS: users.filter(u => u.role === 'user'))
regular_users = [u for u in users if u["role"] == "user"]

# 2. Map (JS: users.map(u => u.name))
names = [u["name"] for u in users]

# 3. Find (JS: users.find(u => u.id === 2))
bob = next((u for u in users if u["id"] == 2), None)

# 4. Sort (JS: users.sort((a, b) => a.age - b.age))
sorted_users = sorted(users, key=lambda u: u["age"])

# 5. Reduce / Sum (JS: users.reduce((acc, u) => acc + u.age, 0))
total_age = sum(u["age"] for u in users)
```\n