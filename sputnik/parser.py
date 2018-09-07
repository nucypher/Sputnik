class Parser:
    """
    Sputnik parser to parse .sputnik files and format opcodes into a more useful
    format for machine reading.

    TODO:
        - Return a program object?
        - Any pre-processing?
        - Is there a better way to parse? Probably. Is it more complex? Probably.
    """

    def __init__(self, file_path: str):
        # Open the file, parse the contents into a digestable format
        with open(file_path, 'r') as f:
            # Structure the raw data into lines
            self.raw_data = f.read()
            self.lines = self.raw_data.split('\n')[:-1]

            # Format each line as a tuple-structured operation
            self.operations = list()
            for line in self.lines:
                self.operations.append(tuple(line.split(' ')))
