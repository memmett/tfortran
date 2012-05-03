"""Templated Fortran (tfortran)."""

from transforms import Transform

def transform_file(filename, output="out.f90",
                   dim=1, interleave=False, compress=True, row_major=False):
    """Apply tfortran source code transformations.

    :param filename: input file name
    :param dim:      dimension
    :param output:   output file name
    """

    template = None
    with open(filename, 'r') as f:
        template = f.read()

    transform = Transform()
    transform.dim = dim
    transform.compress = compress
    transform.interleave = interleave
    transform.row_major = row_major

    transformed = transform.transform(template)

    with open(output, 'w') as f:
        f.write(transformed)
