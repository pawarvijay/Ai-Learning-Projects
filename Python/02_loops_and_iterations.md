# 02. Loops & Iterations (JS vs Python)

## For-of (Array Iteration)
```python
# JS: for (const item of items) { console.log(item); }
items = ["apple", "banana", "cherry"]
for item in items:
    print(item)
```

## For-loop with Index
```python
# JS: items.forEach((item, index) => { ... });
for index, item in enumerate(items):
    print(f"{index}: {item}")
```

## Classic Indexed Range Loop
```python
# JS: for (let i = 0; i < 5; i++) { ... }
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

## While Loop
```python
# JS: while (count > 0) { count--; }
count = 5
while count > 0:
    print(count)
    count -= 1
```

## Break & Continue
```python
for x in range(10):
    if x == 2:
        continue  # skip
    if x == 5:
        break     # stop
```

## List Comprehensions (JS .map & .filter replacement)
```python
# JS: numbers.map(x => x * 2)
doubled = [x * 2 for x in numbers]

# JS: numbers.filter(x => x > 5)
filtered = [x for x in numbers if x > 5]

# JS: numbers.filter(x => x > 5).map(x => x * 2)
result = [x * 2 for x in numbers if x > 5]
```\n