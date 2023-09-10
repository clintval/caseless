# caseless

A caseless typed dictionary in Python

```console
❯ pip install caseless
```

Features:

- Caseless key matching 
- Typing for support in typed codebases

Read the documentation at: [caseless.readthedocs.io](caseless.readthedocs.io)

```python
from caseless import CaselessDict

CaselessDict({1: 2, "lower": "UPPER"}) != CaselessDict({3: 4, "LOWER": "UPPER"})

```