class Sputnik:
    """
    The Sputnik engine that controls the flow of a Sputnik program.

    TODO: Hash the variables and states throughout execution.
    """

    OP_CODES = [
        'BOOTSTRAP',
        'PUSH',
        'NAND',
        'OR',
        'AND',
        'XOR',
        'XNOR',
        'NOT',
        'COPY',
        'CONST',
        'NOR',
        'ANDNY',
        'ANDYN',
        'ORNY',
        'ORYN',
        'MUX',
        'HALT',
        'EXIT',
        'RECOVER',
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

        exec_condition = None
        while not self.program.is_halted and not self.program.is_killed:
            op_code, args = self.program.increment_exec_index_and_get_op()
            exec_condition = self.execute_operation(op_code, args, **kwargs)
            # TODO: Use exec_condition for logging/debugging/etc

        # If the program is halted, we return the entire finite state machine.
        # If the program is killed, we return the STATE like normal.
        if self.program.is_halted or self.program.is_killed:
            return exec_condition

    def execute_operation(self, op_code, args, **kwargs):
        """
        Executes the given operation.
        """
        # Check if the OPCODE is in the list of OP_CODES
        if not op_code in Sputnik.OP_CODES:
            raise SyntaxError("{} is not a valid OPCODE".format(op_code))

        # Get the OPCODE function
        op_code_func = getattr(self, op_code)
        try:
            return op_code_func(args, **kwargs)
        except Exception:
            state_info = self.program.freeze()
            raise RuntimeError("{} with args {} and state {}".format(
                               op_code, args, state_info))

    def BOOTSTRAP(self, args, **kwargs):
        """
        Sputnik Program entrance OPCODE. Sets up the variables to be used during
        execution by checking the global kwargs for the entrance variables.

        TODO: Handle bootstrapping key
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
        self.program.set_variable_data(to_var, from_var_data)

    def NAND(self, args, **kwargs):
        """
        Performs a logical NAND on two bits.
        IN: A, B
        """
        pass

    def OR(self, args, **kwargs):
        """
        Performs a logical OR on two bits.
        IN: A, B
        """
        pass

    def AND(self, args, **kwargs):
        """
        Performs a logical AND on two bits.
        IN: A, B
        """
        pass

    def XOR(self, args, **kwargs):
        """
        Performs a logical XOR on two bits.
        IN: A, B
        """
        var1, var2 = args
        var1 = self.program.get_variable_data(var1)
        var2 = self.program.get_variable_data(var2)

        self.program.set_variable_data('STATE', var1 ^ var2)

    def XNOR(self, args, **kwargs):
        """
        Performs a logical XNOR on two bits.
        IN: A, B
        """
        pass

    def NOT(self, args, **kwargs):
        """
        Performs a logical NOT on one bit.
        IN: A
        """
        pass

    def COPY(self, args, **kwargs):
        """
        wtf is this?
        IN: A
        """
        pass

    def CONST(self, args, **kwargs):
        """
        wtf is this?
        IN: A
        """
        pass

    def NOR(self, args, **kwargs):
        """
        Performs a logical NOR on two bits.
        IN: A, B
        """
        pass

    def ANDNY(self, args, **kwargs):
        """
        Performs a logical AndNY on two bits (NOT(A) AND B)
        IN: A, B
        """
        pass

    def ANDYN(self, args, **kwargs):
        """
        Performs a logical AndYN on two bits (A and NOT(B))
        IN: A, B
        """
        pass

    def ORNY(self, args, **kwargs):
        """
        Performs a logical OrNY on two bits (NOT(A) OR B)
        IN: A, B
        """
        pass

    def ORYN(self, args, **kwargs):
        """
        Performs a logical OrYN on two bits (A OR NOT(B))
        IN: A, B
        """
        pass

    def MUX(self, args, **kwargs):
        """
        Performs a logical ternary multiplexer (A?B:C = A*B + NOT(A)*C)
        IN: A, B, C
        """
        pass

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
        self.program.is_killed = True
        return self.program.state

    def RECOVER(self, args, **kwargs):
        """
        Recovers a program at any point by loading the entire program
        state information.
        """
        # TODO: This would be neat to recover from a HALT, but it's gonna
        #       take a little refactoring.
        pass


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
        self.is_killed = False

    def get_variable_data(self, var_name):
        """
        Returns the data for the variable identified by `var_name`.
        If the var is the global STATE, then it will return it instead.
        """
        if var_name == 'STATE':
            return self.state

        var = self.variables.get(var_name, None)
        return var

    def set_variable_data(self, var_name, var_data):
        """
        Sets the data for the variable identified by `var_name`.
        if the var is the global STATE, then it will set the STATE instead.
        """
        if var_name == 'STATE':
            self.state = var_data
        else:
            self.variables[var_name] = var_data

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
        state_info['is_killed'] = self.is_killed
        state_info['is_halted'] = self.is_halted
        return state_info
