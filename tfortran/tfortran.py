"""Templated Fortran (tfortran)."""

from transforms import transforms

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

    for transform in transforms:
        transform.dim = dim
        transform.compress = compress
        transform.interleave = interleave
        transform.row_major = row_major
        template = transform(template)

    with open(output, 'w') as f:
        f.write(template)
