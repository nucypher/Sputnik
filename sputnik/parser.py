from sputnik.engine import Program


class Parser:
    """
    Sputnik parser to parse .sputnik files and format opcodes into a more useful
    format for machine reading.

    TODO:
        - Any pre-processing?
        - Is there a better way to parse? Probably. Is it more complex? Probably.
    """

    def __init__(self, file_path: str):
        # TODO: If there is any pre-processing stuff, do it here.
        # Open the file, parse the contents into a digestable format
        with open(file_path, 'r') as f:
            # Structure the raw data into lines
            self.raw_data = f.read()
            self.lines = self.raw_data.split('\n')[:-1]

            # Format each line as a tuple-structured operation
            self.operations = list()
            for line in self.lines:
                # Skip lines that begin with `;` -- they're comments
                if line.startswith(';'):
                    continue
                self.operations.append(tuple(line.split(' ')))

    def get_program(self):
        """
        Returns a Program object for Sputnik operation execution.
        """
        return Program(self.operations)
