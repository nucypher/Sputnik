class Sputnik:
    """
    The Sputnik engine that controls the flow of a Sputnik program.

    TODO: Hash the variables and states throughout execution.
    """

    OP_CODES = [
        'BOOTSTRAP',
        'PUSH',
        'EXIT',
    ]

    def __init__(self, program, bootstrapping_key):
        """
        Initializes the Sputnik Engine with a Program and a FHE bootstrapping
        key.
        """
        self.program = program
        self.bootstrapping_key = bootstrapping_key

    def BOOTSTRAP(self, **kwargs):
        """
        Sputnik Program entrance OPCODE. Sets up the variables to be used during
        execution.
        """
        # TODO: Check arguments?
        self.program.variables.update(kwargs)

    def PUSH(self, from_var, to_var):
        """
        Creates a variable `to_var` and pushes the data in `from_var` to `to_var`.
        """
        from_var_data = self.program.get_variable(from_var)
        self.program.variables.update({to_var: from_var_data})

    def EXIT(self):
        """
        Sputnik Program exit OPCODE. Kills the program and returns the program
        state.
        """
        # TODO: Probably need an error for empty state...
        return self.program.state


class Program:
    """
    The Sputnik program object class that holds the state of the Sputnik
    program execution.
    """

    def __init__(self, operations):
        """
        Initializes a Sputnik Program with a list of operations to perform.
        This object should be retrieved via the Sputnik Parser.
        """
        self.operations = operations
        self.state = None
        self.variables = dict()

    def get_variable_data(self, var_name):
        """
        Returns the data for the variable identified by `var_name`.
        """
        var = self.variables.get(var_name, None)
        if not var:
            raise SyntaxError("{} doesn't exist".format(var_name))
        return var
