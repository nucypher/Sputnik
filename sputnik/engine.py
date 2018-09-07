class Engine:
    """
    The Sputnik engine that controls the flow of a Sputnik program.
    """

    def __init__(self, program):
        self.program = program


class Program:
    """
    The Sputnik program object class that holds the state of the Sputnik
    program execution.
    """

    def __init__(self):
        self.state = None
        self.variables = dict()
