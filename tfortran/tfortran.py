"""Templated Fortran (tfortran)."""

from transforms import transforms

def transform_file(filename, dim=1, output="out.f90"):
    """Apply tfortran source code transformations.

    :param filename: input file name
    :param dim:      dimension
    :param output:   output file name
    """

    template = None
    with open(filename, 'r') as f:
        template = f.read()

    for transform in transforms:
        transform.dim = dim
        template = transform(template)

    with open(output, 'w') as f:
        f.write(template)
