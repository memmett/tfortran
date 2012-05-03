"""tfortran tests"""

def test_tfortran():
    import tfortran
    tfortran.transform_file('tests/test1.t.f90', 
                            dim=3, 
                            row_major=True, 
                            interleave=True,
                            output='tests/test1.f90')


if __name__ == '__main__':
    test_tfortran()
