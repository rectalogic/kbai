# SPDX-License-Identifier: AGPL-3.0-or-later
import enum

# From https://github.com/scriptituk/xfade-easing/blob/main/expr/generic-easings-script.txt


class Easing(enum.Enum):
    LINEAR = """
        st(0, ld(0))
    """
    QUADRATIC_IN = """
        st(0, ld(0) * ld(0))
    """
    QUADRATIC_OUT = """
        st(0, ld(0) * (2 - ld(0)))
    """
    QUADRATIC_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), 2 * ld(0) * ld(0), 2 * ld(0) * (2 - ld(0)) - 1))
    """
    CUBIC_IN = """
        st(0, ld(0)^3)
    """
    CUBIC_OUT = """
        st(0, 1 - (1-ld(0))^3)
    """
    CUBIC_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3))
    """
    QUARTIC_IN = """
        st(0, ld(0)^4)
    """
    QUARTIC_OUT = """
        st(0, 1 - (1-ld(0))^4)
    """
    QUARTIC_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), 8 * ld(0)^4, 1 - 8 * (1-ld(0))^4))
    """
    QUINTIC_IN = """
        st(0, ld(0)^5)
    """
    QUINTIC_OUT = """
        st(0, 1 - (1-ld(0))^5)
    """
    QUINTIC_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), 16 * ld(0)^5, 1 - 16 * (1-ld(0))^5))
    """
    SINUSOIDAL_IN = """
        st(0, 1 - cos(ld(0) * PI / 2))
    """
    SINUSOIDAL_OUT = """
        st(0, sin(ld(0) * PI / 2))
    """
    SINUSOIDAL_IN_OUT = """
        st(0, (1 - cos(ld(0) * PI)) / 2)
    """
    EXPONENTIAL_IN = """
        st(0, if(lte(ld(0), 0), 0, pow(2, 10 * ld(0) - 10)))
    """
    EXPONENTIAL_OUT = """
        st(0, if(gte(ld(0), 1), 1, 1 - pow(2, -10 * ld(0))))
    """
    EXPONENTIAL_IN_OUT = """
        st(0,
         if(lt(ld(0), 0.5),
          if(lte(ld(0), 0), 0, pow(2, 20 * ld(0) - 11)),
          if(gte(ld(0), 1), 1, 1 - pow(2, 9 - 20 * ld(0)))
         )
        )
    """
    CIRCULAR_IN = """
        st(0, 1 - sqrt(1 - ld(0) * ld(0)))
    """
    CIRCULAR_OUT = """
        st(0, sqrt(ld(0) * (2 - ld(0))))
    """
    CIRCULAR_IN_OUT = """
        st(0,
         if(lt(ld(0), 0.5),
          1 - sqrt(1 - 4 * ld(0) * ld(0)),
          1 + sqrt(4 * ld(0) * (2 - ld(0)) - 3)
         ) / 2
        )
    """
    ELASTIC_IN = """
        st(0, cos(20 * (1-ld(0)) * PI / 3) / pow(2, 10 * (1-ld(0))))
    """
    ELASTIC_OUT = """
        st(0, 1 - cos(20 * ld(0) * PI / 3) / pow(2, 10 * ld(0)))
    """
    ELASTIC_IN_OUT = """
        st(0,
         st(1, cos(40 * st(2, 2 * ld(0) - 1) * PI / 9) / 2);
         st(2, pow(2, 10 * ld(2)));
         if(lt(ld(0), 0.5), ld(1) * ld(2), 1 - ld(1) / ld(2))
        )
    """
    BACK_IN = """
        st(0, ld(0) * ld(0) * (ld(0) * 2.70158 - 1.70158))
    """
    BACK_OUT = """
        st(0, 1 - (1-ld(0))^2 * (1 - ld(0) * 2.70158))
    """
    BACK_IN_OUT = """
        st(0,
         if(lt(ld(0), 0.5),
          2 * ld(0) * ld(0) * (2 * ld(0) * 3.59491 - 2.59491),
          1 - 2 * (1-ld(0))^2 * (4.59491 - 2 * ld(0) * 3.59491)
         )
        )
    """
    BOUNCE_IN = """
        st(0,
         st(0, 1 - ld(0));
         1 - (
          st(1, 121/16);
          if(lt(ld(0), 4/11),
           ld(1) * ld(0) * ld(0),
           if(lt(ld(0), 8/11),
            ld(1) * (ld(0) - 6/11)^2 + 3/4,
            if(lt(ld(0), 10/11),
             ld(1) * (ld(0) - 9/11)^2 + 15/16,
             ld(1) * (ld(0) - 21/22)^2 + 63/64
           )
          )
         )
        )
       )
    """
    BOUNCE_OUT = """
        st(0,
          st(1, 121/16);
          if(lt(ld(0), 4/11),
           ld(1) * ld(0) * ld(0),
           if(lt(ld(0), 8/11),
            ld(1) * (ld(0) - 6/11)^2 + 3/4,
            if(lt(ld(0), 10/11),
             ld(1) * (ld(0) - 9/11)^2 + 15/16,
             ld(1) * (ld(0) - 21/22)^2 + 63/64
            )
           )
          )
        )
    """
    BOUNCE_IN_OUT = """
        st(0,
         st(1,
          st(0, st(2, lt(ld(0), 0.5) * 2 - 1) * (1 - 2 * ld(0)));
          st(1, 121/16);
          if(lt(ld(0), 4/11),
           ld(1) * ld(0) * ld(0),
           if(lt(ld(0), 8/11),
            ld(1) * (ld(0) - 6/11)^2 + 3/4,
            if(lt(ld(0), 10/11),
             ld(1) * (ld(0) - 9/11)^2 + 15/16,
             ld(1) * (ld(0) - 21/22)^2 + 63/64
            )
           )
          )
         );
         (1 - ld(2) * ld(1)) / 2
        )
    """
    SQUAREROOT_IN = """
        st(0, sqrt(ld(0)))
    """
    SQUAREROOT_OUT = """
        st(0, 1 - sqrt((1-ld(0))))
    """
    SQUAREROOT_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), sqrt(ld(0) / 2), 1 - sqrt((1-ld(0)) / 2)))
    """
    CUBEROOT_IN = """
        st(0, 1 - pow((1-ld(0)), 1/3))
    """
    CUBEROOT_OUT = """
        st(0, pow(ld(0), 1/3))
    """
    CUBEROOT_IN_OUT = """
        st(0, if(lt(ld(0), 0.5), pow(ld(0) / 4, 1/3), 1 - pow((1-ld(0)) / 4, 1/3)))
    """
