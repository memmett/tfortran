"""tfortran tests"""

def test_tfortran():
    import tfortran
    tfortran.transform_file('tests/test1.t.f90', dim=3, output='tests/test1.f90')


if __name__ == '__main__':
    test_tfortran()
