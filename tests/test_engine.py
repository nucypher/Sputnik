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


def test_engine_OR():
    SputnikParser = Parser('tests/or.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    var1 = 10
    var2 = 21
    sputnik.execute_program(a=var1, b=var2)
    assert sputnik.program.state == ( var1 | var2 )

def test_engine_AND():
    SputnikParser = Parser('tests/and.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    var1 = 12
    var2 = 13
    sputnik.execute_program(a=var1, b=var2)
    assert sputnik.program.state == ( var1 & var2 )
