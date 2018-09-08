class Sputnik:
    """
    The Sputnik engine that controls the flow of a Sputnik program.

    TODO: Hash the variables and states throughout execution.
    """

    OP_CODES = [
        'BOOTSTRAP',
        'PUSH',
        'HALT',
        'EXIT',
    ]

    def __init__(self, program, bootstrapping_key):
        """
        Initializes the Sputnik Engine with a Program and a FHE bootstrapping
        key.
        """
        self.program = program
        self.bootstrapping_key = bootstrapping_key

    def execute_program(self, exec_index=None, **kwargs):
        """
        Begins program execution loop at the provided `exec_index`. If an
        `exec_index` is not provided, the program will find the entrance index
        and set it minus one for the next execution call.
        """
        if exec_index is None:
            self.program.set_exec_index(self.program.find_entrance() - 1)

        # TODO: Other exit states other than `is_halted`
        while not self.program.is_halted:
            op_code, args = self.program.increment_exec_index_and_get_op()
            self.execute_operation(op_code, args, **kwargs)

    def execute_operation(self, op_code, args, **kwargs):
        """
        Executes the given operation.
        """
        # Check if the OPCODE is in the list of OP_CODES
        if not op_code in Sputnik.OP_CODES:
            raise SyntaxError("{} is not a valid OPCODE".format(op_code))

        # Get the OPCODE function
        op_code_func = getattr(self, op_code)
        op_code_func(args, **kwargs)

    def BOOTSTRAP(self, args, **kwargs):
        """
        Sputnik Program entrance OPCODE. Sets up the variables to be used during
        execution by checking the global kwargs for the entrance variables.
        """
        entrance_vars = dict()
        for var_name in args:
            var_data = kwargs.get(var_name, None)
            if not var_data:
                continue
            entrance_vars[var_name] = var_data
        self.program.set_entrance_vars(**entrance_vars)

    def PUSH(self, args, **kwargs):
        """
        Pushes the from_var data to the to_var.
        """
        from_var, to_var = args
        from_var_data = self.program.get_variable_data(from_var)

        if to_var == 'STATE':
            self.program.state = from_var_data
        else:
            self.program.variables[to_var] = from_var_data

    def HALT(self, args, **kwargs):
        """
        Kills program execution and dumps all program information. Mostly used
        for debugging.
        """
        self.program.is_halted = True
        halt_info = self.program.freeze()
        return halt_info

    def EXIT(self, args, **kwargs):
        """
        Sputnik Program exit OPCODE. Kills the program and returns the program
        state.
        """
        # TODO: Probably need an error for empty state...
        self.program.is_halted = True
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
        self.exec_index = None
        self.is_halted = False

    def get_variable_data(self, var_name):
        """
        Returns the data for the variable identified by `var_name`.
        """
        var = self.variables.get(var_name, None)
        if not var:
            raise SyntaxError("{} doesn't exist".format(var_name))
        return var

    def find_entrance(self):
        """
        Finds and returns the index where the BOOTSTRAP call is performed.
        """
        for idx, operation in enumerate(self.operations):
            if operation[0] == 'BOOTSTRAP':
                return idx
        raise SyntaxError("No entrance could be found -- needs a BOOTSTRAP")

    def set_entrance_vars(self, **kwargs):
        """
        Sets the program's entrance variables during a BOOTSTRAP call.
        """
        # TODO: Error if empty?
        self.variables.update(kwargs)

    def set_exec_index(self, exec_index):
        """
        Sets the exec_index for the next execution.
        """
        self.exec_index = exec_index

    def increment_exec_index_and_get_op(self):
        """
        Increments the exec_index and returns the operation at the new index.
        """
        self.exec_index += 1
        return self.get_op_at_index(self.exec_index)

    def get_op_at_index(self, op_index):
        """
        Returns the operation at the `op_index` in a tuple.

        (OP_CODE, (args))
        """
        instructions = self.operations[op_index]
        op_code = instructions[0]
        args = instructions[1:]
        return (op_code, tuple(args))

    def freeze(self):
        """
        Returns all program state information in a dict.
        """
        state_info = dict()
        state_info['operations'] = self.operations.copy()
        state_info['state'] = self.state
        state_info['variables'] = self.variables.copy()
        state_info['exec_index'] = self.exec_index
