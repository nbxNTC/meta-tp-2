FloatList = list[float]


class Individual:
    """
    A class used to represent an Individual in float-based Genetic Algorithms

    ...

    Attributes
    ----------
    kind : str
        the individual specific representation (float, for now)
    value : FloatList
        the list of float parameters that represents the float-based individual
    fitness : float
        the fitness value attatched to this individual
    generation : int
        the generation that generated the individual

    Methods
    -------
    """

    kind = "float"

    def __init__(self, value: FloatList = [], generation: int = 0) -> None:
        self.fitness = None
        self.value = value
        self.generation = generation
