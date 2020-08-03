import docker
import tarfile
import tempfile
import meshio


def get_container():
    """Pull, start and/or reuse a container containing `netgen`."""
    client = docker.from_env()
    return client.containers.list()[0]


def write_to_container(ctr, geo: str, suffix: str = ".geo") -> str:
    """Write a given string to a file inside the container."""

    # write string to a temporary file on host
    tmpfile = tempfile.NamedTemporaryFile(suffix=suffix, mode='w')
    tmpfile.write(geo)
    tmpfile.seek(0)

    # create a tar archive
    tar = tarfile.open(tmpfile.name + ".tar", mode='w')
    try:
        tar.add(tmpfile.name)
    finally:
        tar.close()
        tmpfile.close()

    # unpack tar contents to container root
    data = open(tmpfile.name + ".tar", 'rb').read()
    container.put_archive("/", data)

    return tmpfile.name


def generate(geo: str, verbose: bool = True):
    """Generate a mesh based on `geo`-specification."""

    ctr = get_container()
    filename = write_to_container(ctr, geo)

    # run netgen
    res = container.exec_run(("netgen "
                              "-geofile=/{} "
                              "-meshfile=/output.msh "
                              "-meshfiletype=\"Gmsh2 Format\" "
                              "-batchmode").format(filename),
                             stream=False,
                             demux=False)
    if verbose:
        print(res.output)

    # write output mesh to a temporary tar file
    out = open(tmpfilename + ".out.tar", 'wb')
    bits, _ = container.get_archive("/output.msh")
    for chunk in bits:
        out.write(chunk)
    out.close()

    # extract mesh file from the temporary tar file
    tar = tarfile.open(tmpfilename + ".out.tar", mode='r')
    tar.extract("output.msh", tmpfilename + ".out")
    tar.close()

    mesh = meshio.read(
        tmpfilename + ".out/output.msh"
    )

    return mesh
