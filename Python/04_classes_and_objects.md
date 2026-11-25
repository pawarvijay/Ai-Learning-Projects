# 04. Classes & Object Creation (JS vs Python)

## Class Syntax
```python
# JavaScript                      # Python
class User {                      class User:
  constructor(name, email) {          def __init__(self, name: str, email: str):
    this.name = name;                     self.name = name
    this.email = email;                   self.email = email
  }                                   
  getGreeting() {                     def get_greeting(self) -> str:
    return `Hi, ${this.name}`;            return f"Hi, {self.name}"
}                                 

# Instantiation:
# JS: const u = new User("Alex", "a@a.com");
u = User("Alex", "a@a.com")      # Notice: NO 'new' keyword
```

## Inheritance & Super
```python
class Admin(User):
    def __init__(self, name: str, email: str, role: str):
        super().__init__(name, email)
        self.role = role
```

## Modern Data Classes (TypeScript Interfaces)
```python
# TypeScript:
# interface Product { id: number; title: string; price: number; }

from dataclasses import dataclass

@dataclass
class Product:
    id: int
    title: str
    price: float = 0.0

p = Product(id=1, title="Laptop", price=999.0)
print(p.title)
```

## Pydantic (Production Class Validation)
```python
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

# Automatically validates types at runtime; throws error if invalid
user = UserSchema(id=1, name="Alex", email="alex@test.com")
print(user.model_dump())  # Converts to dict
```\n