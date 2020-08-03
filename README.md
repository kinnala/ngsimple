**ngsimple**: A simple Python wrapper for running
[Netgen](https://github.com/NGSolve/netgen) in a container

# Installation

Install with
```
pip install ngsimple
```
**ngsimple** requires Docker and
[docker-py](https://github.com/docker/docker-py)
for pulling container images and interacting with the mesh generator.
Moreover, the output is read using [meshio](https://github.com/nschloe/meshio).

# Example

```python
from ngsimple import generate

mesh = generate("""
algebraic3d

solid main = sphere (0, 0, 0; 1);

tlo main;
point (0, 0, 0);
""")

from vedo import show

show(mesh)
```

![Netgen output mesh](https://user-images.githubusercontent.com/973268/89173063-549e0000-d58c-11ea-98b9-91d9ef9f218d.png)
