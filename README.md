# caseless

[![Build Status](https://github.com/clintval/caseless/actions/workflows/test.yml/badge.svg)](https://github.com/clintval/caseless/actions/workflows/test.yml)
[![PyPi Release](https://badge.fury.io/py/caseless.svg)](https://badge.fury.io/py/caseless)
[![Python Versions](https://img.shields.io/pypi/pyversions/caseless.svg)](https://pypi.python.org/pypi/caseless/)
[![MyPy Checked](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A caseless typed dictionary in Python.

```console
pip install caseless
```

![Guitar Lake, California](.github/img/cover.jpg)

```python
from caseless import CaselessDict

CaselessDict({"lower": "UPPER"})["LOWER"] == "UPPER"
CaselessDict({"lower": "UPPER"}).get("LOWER") == "UPPER"
CaselessDict({"lower": "value"}) == CaselessDict({"LOWER": "value"})
```
