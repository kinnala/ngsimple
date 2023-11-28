# ngsimple

[![PyPI](https://img.shields.io/pypi/v/ngsimple)](https://pypi.org/project/ngsimple/)

Suppose you wanted to use Netgen in a Python script to generate tetrahedral
meshes but did not want to spend time installing the entire [Netgen/NGSolve](https://ngsolve.org/)
package which ships with it's own Python interpreter.  This is a simple wrapper
for running Netgen mesh generator inside a container and functions for calling
it transparently from any Python interpreter.

_This is work-in-progress.  Currently using the following container: https://hub.docker.com/r/ngsxfem/ngsolve. In future, plan is to use a dedicated more lightweight container._

## Installation

Install with
```
pip install ngsimple
```
ngsimple requires Docker and
[docker-py](https://github.com/docker/docker-py)
for pulling container images and interacting with the mesh generator.
The output mesh is read back to Python using [meshio](https://github.com/nschloe/meshio).

## Example


```python
from ngsimple import generate

mesh = generate("""algebraic3d

solid main = sphere (0, 0, 0; 1);

tlo main;
point (0, 0, 0);
""", verbose=True)

from vedo import show

show(mesh)
```

![Netgen output mesh](https://user-images.githubusercontent.com/973268/89173063-549e0000-d58c-11ea-98b9-91d9ef9f218d.png)

# Changelog

## 0.2.0

- Update to a working container image
- Allow specifying `image` and `tag` in `generate`