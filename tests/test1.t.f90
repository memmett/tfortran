module test1
  implicit none
  use iso_c_binding
contains

  subroutine divergence1(f, {{ nx, ny, nz }}, divf) bind(c, name="divergence1")
    real(c_double), intent(in)        :: f({{nx, ny, nz}})
    integer(c_int), intent(in), value :: {{ nx, ny, nz }}
    real(c_double), intent(out)       :: divf({{nx, ny, nz}})

    do multi({{i, j, k}}; {{nx, ny, nz}})
       ! body of multi do
    end do multi
  end subroutine divergence1

  subroutine divergence2(f, {{n}}, divf) bind(c, name="divergence2")
    real(c_double), intent(in)        :: f({{n;.}})
    integer(c_int), intent(in), value :: {{n}}
    real(c_double), intent(out)       :: divf({{n}})

    do multi({{i, j, k}}; {{n}})
       ({
       ! some 1d code;
       ! some 2d code;
       ! some 3d code
       })
    end do multi

    z = [{ [{ 1; 2; 3 }] x**2; + y**2; + z**2 }]

  end subroutine divergence2

end module test1
