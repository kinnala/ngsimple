**ngsimple**: The easiest way to call
[Netgen](https://github.com/NGSolve/netgen) from Python

Suppose you wanted to use Netgen in a Python script to generate tetrahedral
meshes but did not want to spend time installing the entire Netgen/NGSolve
package which ships with it's own Python interpreter.  This is a simple wrapper
for running Netgen mesh generator inside a container and functions for calling
it transparently from any Python interpreter.

# Installation

Install with
```
pip install git+https://github.com/kinnala/ngsimple.git@master
```
ngsimple uses Docker and
[docker-py](https://github.com/docker/docker-py)
for pulling container images and interacting with the mesh generator.
The output mesh is read back to Python using [meshio](https://github.com/nschloe/meshio).

# Example

The examples demonstrate how ngsimple can be coupled with external packages.

## Visualize with vedo

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

## Load to scikit-fem and draw

```python
from ngsimple import generate
from skfem.io.meshio import from_meshio
from skfem.visuals.matplotlib import draw, show

m = from_meshio(generate("""algebraic3d

solid cyls = cylinder ( -100, 0, 0; 200, 0, 0; 40 )
          or cylinder ( 100, -100, 100; 100, 200, 100; 40)
          or cylinder ( 0, 100, -100; 0, 100, 200; 40);
solid sculpture = sphere (50, 50, 50; 80) and not cyls
        and not sphere (50, 50, 50; 50);

tlo sculpture -col=[0.5, 0.5, 0.5];"""))

draw(m)
show()
```

![Matplotlib](https://user-images.githubusercontent.com/973268/92920639-453b8d80-f43b-11ea-9542-a21bc7afd927.png)

## Load to pyfvm and solve Poisson equation

Snippet adapted from [pyfvm](https://github.com/nschloe/pyfvm/) example. (GPLv3 license).

```python
from ngsimple import generate
import pyfvm
from pyfvm.form_language import *
import meshzoo
from scipy.sparse import linalg
import meshplex

class Poisson(object):
    def apply(self, u):
        return integrate(lambda x: -n_dot_grad(u(x)), dS) \
             - integrate(lambda x: 1.0, dV)

    def dirichlet(self, u):
        return [(lambda x: u(x) - 0.0, Boundary())]


mesh = generate("""algebraic3d

solid tor = torus ( 0, 0, 0; 1, 0, 0; 2 ; 1 );

tlo tor;""")

mesh = meshplex.MeshTetra(mesh.points, mesh.get_cells_type("tetra"))

matrix, rhs = pyfvm.discretize_linear(Poisson(), mesh)

u = linalg.spsolve(matrix, rhs)

mesh.write('out.vtk', point_data={'u': u})
```

![Paraview](https://user-images.githubusercontent.com/973268/92920660-4ff62280-f43b-11ea-99ad-31cd27fb4bb6.png)

See [Netgen tutorials](https://github.com/NGSolve/netgen/tree/master/tutorials)
for more information on the format expected by `generate`.
