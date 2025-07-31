# ⏱️ Python `datetime.strftime` / `strptime` Format Cheatsheet

Use `datetime.now().strftime(...)` to format dates/times into strings.

Use `datetime.strptime(string, format)` to parse a string back into a `datetime` object.

---

## 📆 Common Directives

| Directive | Meaning              | Example    |
| --------- | -------------------- | ---------- |
| `%Y`      | Year (4-digit)       | `2025`     |
| `%y`      | Year (2-digit)       | `25`       |
| `%m`      | Month (01–12)        | `07`       |
| `%B`      | Month name           | `July`     |
| `%b`      | Month abbreviation   | `Jul`      |
| `%d`      | Day of month (01–31) | `31`       |
| `%A`      | Weekday name         | `Thursday` |
| `%a`      | Weekday abbreviation | `Thu`      |

---

## ⏰ Time Formatting

| Directive | Meaning                     | Example  |
| --------- | --------------------------- | -------- |
| `%H`      | Hour (00–23)                | `14`     |
| `%I`      | Hour (01–12)                | `02`     |
| `%p`      | AM/PM                       | `PM`     |
| `%M`      | Minute (00–59)              | `55`     |
| `%S`      | Second (00–59)              | `07`     |
| `%f`      | Microsecond (000000–999999) | `803421` |

---

## 📦 Full Examples

```python
from datetime import datetime

now = datetime.now()

now.strftime("%Y-%m-%d %H:%M:%S")       # 2025-07-31 12:34:56
now.strftime("%A, %B %d %Y")            # Thursday, July 31 2025
now.strftime("%I:%M %p")                # 12:34 PM
now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")   # ISO-like with microseconds
```
