**ngsimple**: A simple Python wrapper for running
[Netgen](https://github.com/NGSolve/netgen) in a container

Install with
```
pip install ngsimple
```
**ngsimple** requires Docker and
[docker-py](https://github.com/docker/docker-py)
for pulling container images and interacting with the mesh generator.
Moreover, the output is read using [meshio](https://github.com/nschloe/meshio).
