class Printable:
    """
        Provides a default **__str__** method to python classes so that their attributes are convertible to a string
    """

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
