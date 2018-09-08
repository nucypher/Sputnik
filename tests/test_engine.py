import pytest
from sputnik.engine import Sputnik
from sputnik.parser import Parser


def test_program():
    SputnikParser = Parser('tests/engine.sputnik')

    proggy = SputnikParser.get_program()
    assert len(proggy.operations) == 4


def test_sputnik():
    SputnikParser = Parser('tests/engine.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    sputnik.execute_program(test='yes')
    assert sputnik.program.variables['test'] == 'yes'
    assert sputnik.program.state == 'yes'
    assert sputnik.program.state == sputnik.program.variables['new_var']


def test_engine_halt():
    SputnikParser = Parser('tests/abc.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    output = sputnik.execute_program(a=1, b=2, c=3)
