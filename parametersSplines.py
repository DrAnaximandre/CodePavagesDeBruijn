
def color_index_function1(nbp, maxi):
    return nbp / maxi


class ParametersSplines(object) :


    def __init__(self,
                 PALETTE : str = 'TWILIGHT',
                 ONLY_PERIODIC : bool = False,
                 MIN_LENGTH : int = 5,
                 COLOR_INDEX_FUNCTION : callable = color_index_function1,
                 LINE_WIDTH: float = 1.0,
                 # voir splines.py pour la signification de S et MAGN
                 S: float = 1.5,
                 MAGN: int = 50,
        ) :

        self.PALETTE = PALETTE
        self.ONLY_PERIODIC = ONLY_PERIODIC
        self.MIN_LENGTH = MIN_LENGTH
        self.COLOR_INDEX_FUNCTION = COLOR_INDEX_FUNCTION
        self.LINE_WIDTH = LINE_WIDTH
        self.S = S
        self.MAGN = MAGN

    def latex(self):
        s = (f'$\n\n$Spline Palette={self.PALETTE}, Periodic={self.ONLY_PERIODIC}, \
MinLength={self.MIN_LENGTH}, ColorIndexFunction={self.COLOR_INDEX_FUNCTION}, \
LineWidth={self.LINE_WIDTH}, S={self.S}, Magn:{self.MAGN}')
        return s
