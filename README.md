# caseless

[![Testing Status](https://github.com/clintval/caseless/actions/workflows/test.yml/badge.svg)](https://github.com/clintval/caseless/actions/workflows/test.yml)
[![PyPi Release](https://badge.fury.io/py/caseless.svg)](https://badge.fury.io/py/caseless)
[![Python Versions](https://img.shields.io/pypi/pyversions/caseless.svg)](https://pypi.python.org/pypi/caseless/)
[![MyPy Checked](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A caseless typed dictionary in Python

```console
❯ pip install caseless
```

Features:

- Caseless key matching 
- Typing for support in typed codebases

```python
from caseless import CaselessDict

CaselessDict({"lower": "my-value"}) == CaselessDict({"LOWER": "my-value"})
```
