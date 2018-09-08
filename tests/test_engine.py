import pytest
from sputnik.parser import Parser


def test_program():
    SputnikParser = Parser('tests/engine.sputnik')

    proggy = SputnikParser.get_program()
    assert len(proggy.operations) == 3
