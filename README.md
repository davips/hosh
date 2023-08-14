![test](https://github.com/davips/hosh/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/hosh/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/hosh)
<a href="https://pypi.org/project/hosh">
<img src="https://img.shields.io/pypi/v/hosh.svg?label=release&color=blue&style=flat-square" alt="pypi">
</a>
![Python version](https://img.shields.io/badge/python-≥3.8-blue.svg)
[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845)
[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)
[![API documentation](https://img.shields.io/badge/API-autogenerated-a030a0.svg)](https://davips.github.io/hosh)
[![Manual](https://img.shields.io/badge/manual-handcrafted-a030a0.svg)](https://hosh.page)
[![Downloads](https://static.pepy.tech/badge/hosh)](https://pepy.tech/project/hosh)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hosh)

# hosh - Identification based on group theory
[Website](https://hosh.page) |
[Latest Release](https://pypi.org/project/hosh) |
[Current Code](https://github.com/davips/hosh) |
[API Documentation](https://davips.github.io/hosh)

This [Python library](https://pypi.org/project/hosh) / [code](https://github.com/davips/hosh) provides a reference implementation for the UT*.4 specification presented [here](https://arxiv.org/abs/2109.06028).
A previous version, containing extra group theory content, is available in the package [GaROUPa](https://pypi.org/project/garoupa).

Please see the [website](https://hosh.page) for more detailed usage information.

We adopt a novel paradigm to universally unique identification (UUID), making identifiers deterministic and predictable, 
even before an object is generated by a (possibly costly) process.   
Here, data versioning and composition of processing steps are directly mapped as simple operations over identifiers.
We call each of the latter a `Hosh`, i.e., an identifier is an _**o**perable **h**a**sh**_.

A first implementation of the remaining ideas from the [paper](https://arxiv.org/abs/2109.06028) is provided in this
[cacheable lazy dict](https://pypi.org/project/ldict/2.211016.3) which depends on `hosh` and serves as an advanced usage example.
<br>
A second (entirely rewritten) version is available in the package [idict](https://pypi.org/project/idict), succeeded by [hoshmap](https://pypi.org/project/hoshmap).
The most recent rewritten version of a hosh-based dict (and the most robust, recommended, one) is available in the package [hdict](https://pypi.org/project/hdict).


## Overview
A product of identifiers produces a new identifier as shown below, where sequences of bytes (`b"..."`) are passed to simulate binary objects to be hashed.

![img.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img.png) | New identifiers are easily <br> created from the identity <br> element `ø`. Also available as `identity` for people <br>or systems allergic to <br>utf-8 encoding.
-------------------------|-------------------------

![img_1.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_1.png) | Operations can be reverted by the inverse of the identifier.
-------------------------|-------------------------

![img_2.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_2.png) | Operations are associative. <br>They are order-sensitive by default, <br>in which case they are called _ordered_ ids.
-------------------------|-------------------------

However, order-insensitive (called _unordered_) and order-insensitive-among-themselves (called _hybrid_) identifiers are also available. | .
-------------------------|-------------------------
![img_3.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_3.png) | .

This is how they affect each other: | .
-------------------------|-------------------------
![img_4.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_4.png) | .

The chance of collision is determined by the number of possible identifiers of each type.
Some versions are provided, e.g.: UT32.4, UT40.4 (default), UT64.4.
They can be easily implemented in other languages and are 
intended to be a specification on how to identify multi-valued objects and multi-step processes.
Unordered ids use a very narrow range of the total number of identifiers.
This is not a problem as they are not very useful.

One use for unordered ids could be the embedding of authorship or other metadata into an object without worrying about the timing, since the resulting id will remain the same, no matter when the unordered id is operated with the id of the object under construction. | . 
-------------------------|-------------------------
![img_5.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_5.png) | . 

Conversely, hybrid ids are excelent to represent values in a data structure like a map, 
since the order is not relevant when the consumer process looks up for keys, not indexes.
Converselly, a chain of a data processing functions usually implies one step is dependent on the result of the previous step.
This makes ordered ids the perfect fit to identify functions (and also their composition, as a consequence).

### Relationships can also be represented
Here is another possible use. ORCIDs are managed unique identifiers for researchers.
They can be directly used as digests to create operable identifiers.
We recommend the use of 40 digits to allow operations with SHA-1 hashes. 
They are common in version control repositories among other uses.
![img_orcid.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_orcid.png)

Unordered relationships are represented by hybrid ids.
Automatic transparent conversion between ORCID dashes by a hexdecimal character can be implemented in the future if needed.
![img_orcid-comm.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_orcid-comm.png)

## More info
Aside from the [paper](https://arxiv.org/abs/2109.06028), [PyPI package](https://pypi.org/project/hosh) 
and [GitHub repository](https://github.com/davips/hosh), 
one can find more information, at a higher level application perspective, 
in this presentation:
![image](https://raw.githubusercontent.com/davips/hosh/14cb45b888eb8a18ae093d200075c1a8a7e9cacb/examples/capa-slides-gdocs.png)
A lower level perspective is provided in the [API documentation](https://davips.github.io/hosh).

## Python installation
### from package
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI
pip install hosh
```

### from source
```bash
git clone https://github.com/davips/hosh
cd hosh
poetry install
```

### Examples
Some usage examples.

**Basic operations**
<details>
<p>

```python3
from hosh import Hosh, ø  # ø is a shortcut for identity (AltGr+O in most keyboards)

# Hoshes (operable hash-based elements) can be multiplied.
a = Hosh(content=b"Some large binary content...")
b = Hosh(content=b"Some other binary content. Might be, e.g., an action or another large content.")
c = a * b
print(f"{a} * {b} = {c}")
"""
8CG9so9N1nQ59uNO8HGYcZ4ExQW5Haw4mErvw8m8 * 7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 = z3EgxfisgqbNXBd0eqDuFiaTblBLA5ZAUbvEZgOh
"""
```

```python3
print(~b)
# Multiplication can be reverted by the inverse hosh. Zero is the identity hosh.
print(f"{b} * {~b} = {b * ~b} = 0")
"""
Q6OjmYZSJ8pB3ogBVMKBOxVp-oZ80czvtUrSyTzS
7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 * Q6OjmYZSJ8pB3ogBVMKBOxVp-oZ80czvtUrSyTzS = 0000000000000000000000000000000000000000 = 0
"""
```

```python3

print(f"{b} * {ø} = {b * ø} = b")
"""
7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 * 0000000000000000000000000000000000000000 = 7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 = b
"""
```

```python3

print(f"{c} * {~b} = {c * ~b} = {a} = a")
"""
z3EgxfisgqbNXBd0eqDuFiaTblBLA5ZAUbvEZgOh * Q6OjmYZSJ8pB3ogBVMKBOxVp-oZ80czvtUrSyTzS = 8CG9so9N1nQ59uNO8HGYcZ4ExQW5Haw4mErvw8m8 = 8CG9so9N1nQ59uNO8HGYcZ4ExQW5Haw4mErvw8m8 = a
"""
```

```python3

print(f"{~a} * {c} = {~a * c} = {b} = b")
"""
RNvSdLI-5RiBBGL8NekctiQofWUIeYvXFP3wvTFT * z3EgxfisgqbNXBd0eqDuFiaTblBLA5ZAUbvEZgOh = 7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 = 7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 = b
"""
```

```python3

# Division is shorthand for reversion.
print(f"{c} / {b} = {c / b} = a")
"""
z3EgxfisgqbNXBd0eqDuFiaTblBLA5ZAUbvEZgOh / 7N-L-10JS-H5DN0-BXW2e5ENWFQFVWswyz39t8s9 = 8CG9so9N1nQ59uNO8HGYcZ4ExQW5Haw4mErvw8m8 = a
"""
```

```python3

# Hosh multiplication is not expected to be commutative.
print(f"{a * b} != {b * a}")
"""
z3EgxfisgqbNXBd0eqDuFiaTblBLA5ZAUbvEZgOh != wwSd0LaGvuV0W-yEOfgB-yVBMlNLA5ZAUbvEZgOh
"""
```

```python3

# Hosh multiplication is associative.
print(f"{a * (b * c)} = {(a * b) * c}")
"""
RuTcC4ZIr0Y1QLzYmytPRc087a8cbbW9Nj-gXxAz = RuTcC4ZIr0Y1QLzYmytPRc087a8cbbW9Nj-gXxAz
"""
```


</p>
</details>


## Performance
Computation time for the simple operations performed by `hosh` can be considered negligible for most applications,
since the order of magnitude of creating and operating identifiers is around a few μs:
![img_6.png](https://raw.githubusercontent.com/davips/hosh/main/examples/img_6.png)
The package [hoshrust](https://pypi.org/project/hoshrust) was a faster implementation of an earlier version of `hosh`.
As the performance of the current `hosh` seems already very high (only ~2x slower than if it was implemented in native code in like _rust_), 
we don't have plans for a new 'rust' implementation in the near future.

## Grants
This work was partially supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0).
