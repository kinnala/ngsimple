import os
import tarfile
import tempfile
import json

import docker
import meshio


def get_container(image: str = 'pymor/ngsolve_py3.7',
                  tag: str = '5a68d5f17ad108242600cc7f479b4ca1b49b81a6'):
    """Pull and/or start a container that has `netgen`.

    Parameters
    ----------
    image
        The container image name to use.

    Returns
    -------
    An object representing the container.

    """
    client = docker.from_env()

    for line in client.api.pull(image,
                                tag=tag,
                                stream=True,
                                decode=True):
        if "status" in line:
            print(line["status"])

    ctr = client.containers.create(image,
                                   command='sleep infinity',
                                   detach=True)
    ctr.start()

    return ctr


def clean_container(ctr):
    """Kill and remove the container."""
    ctr.kill()
    ctr.remove()


def write_to_container(ctr, geo: str, suffix: str = ".geo") -> str:
    """Write a given string to a file inside the container.

    Parameters
    ----------
    ctr
    geo
    suffix

    Returns
    -------
    The filename of the file written inside the container.

    """

    # write string to a temporary file on host
    tmpfile = tempfile.NamedTemporaryFile(suffix=suffix,
                                          mode='w',
                                          delete=False)
    tmpfile.write(geo)
    tmpfile.seek(0)
    tmpfile.close()

    # create a tar archive
    tarname = tmpfile.name + ".tar"
    tar = tarfile.open(tarname, mode='w')
    try:
        tar.add(tmpfile.name,
                arcname=os.path.basename(tmpfile.name))
    finally:
        tar.close()
        os.remove(tmpfile.name)

    # unpack tar contents to container root
    with open(tarname, 'rb') as fh:
        ctr.put_archive("/", fh.read())

    os.remove(tarname)

    return "/" + os.path.basename(tmpfile.name)


def fetch_from_container(ctr, filename: str):
    """Fetch the resulting mesh from container.

    Parameters
    ----------
    ctr
    filename

    Returns
    -------
    Mesh object from `meshio`.

    """

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tar",
                                          mode='wb',
                                          delete=False)
    bits, _ = ctr.get_archive("{}".format(filename))
    basename = os.path.basename(filename)
    try:
        for chunk in bits:
            tmpfile.write(chunk)
        tmpfile.seek(0)
        tmpfile.close()
        tar = tarfile.open(tmpfile.name, mode='r')
        tar.extract(basename, tmpfile.name + "_out")
    finally:
        tar.close()
        os.remove(tmpfile.name)

    mesh = meshio.read(tmpfile.name + "_out/" + basename)
    os.remove(tmpfile.name + "_out/" + basename)
    os.rmdir(tmpfile.name + "_out")

    return mesh


def generate(geo: str, params: str = None, verbose: bool = False):
    """Generate a mesh based on `geo`-specification.

    Parameters
    ----------
    geo
        A description of the domain via constructive solid geometry.
        See https://github.com/NGSolve/netgen/tree/master/tutorials
        for more information.
    params
        Additional command line parameters for `netgen`.  For example,
        '-fine' generates a more refined mesh.
    verbose
        If `True`, print the output of `netgen`.

    Returns
    -------
    Mesh object from `meshio`.

    """
    params = "" if params is None else params + ' '
    ctr = get_container()
    filename = write_to_container(ctr, geo)

    # run netgen
    res = ctr.exec_run(("netgen {}"
                        "-geofile={} "
                        "-meshfile=/output.msh "
                        "-meshfiletype=\"Gmsh2 Format\" "
                        "-batchmode").format(params, filename),
                       stream=False,
                       demux=False)
    if verbose:
        print(res.output)

    mesh = fetch_from_container(ctr, "/output.msh")
    clean_container(ctr)

    return mesh
