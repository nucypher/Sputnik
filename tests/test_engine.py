import pytest
from sputnik.engine import Sputnik
from sputnik.parser import Parser


def test_program():
    SputnikParser = Parser('tests/engine.sputnik')

    proggy = SputnikParser.get_program()
    assert len(proggy.operations) == 3


def test_sputnik():
    SputnikParser = Parser('tests/engine.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    sputnik.execute_program(test='yes')
    assert sputnik.program.variables['test'] == 'yes'

    assert sputnik.program.state == 'yes'
