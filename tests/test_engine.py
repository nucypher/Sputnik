import nufhe
import numpy
import pytest

from reikna.cluda import any_api
from sputnik.engine import Sputnik
from sputnik.parser import Parser

thr = any_api().Thread.create(interactive=True)
rng = numpy.random.RandomState()
secret_key, bootstrap_key = nufhe.make_key_pair(thr, rng, transform_type='NTT')

size = 32

bits1 = rng.randint(0, 2, size=size).astype(numpy.bool)
bits2 = rng.randint(0, 2, size=size).astype(numpy.bool)

ciphertext1 = nufhe.encrypt(thr, rng, secret_key, bits1)
ciphertext2 = nufhe.encrypt(thr, rng, secret_key, bits2)

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
    assert sputnik.program.state == (var1 | var2)


def test_engine_AND():
    SputnikParser = Parser('tests/and.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    var1 = 12
    var2 = 13
    sputnik.execute_program(a=var1, b=var2)
    assert sputnik.program.state == (var1 & var2)


def test_engine_XOR():
    SputnikParser = Parser('tests/xor.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    var1 = 5
    var2 = 55
    sputnik.execute_program(a=var1, b=var2)
    assert sputnik.program.state == (var1 ^ var2)


def test_engine_XOR_combo():
    SputnikParser = Parser('tests/xor-combo.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    var1 = 7
    var2 = 17
    sputnik.execute_program(a=var1, b=var2)
    assert sputnik.program.state == ((var1 | var2) ^ (var1 & var2)) & (var1 ^ var2)


def test_engine_entrance():
    SputnikParser = Parser('tests/entrance_vars.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    sputnik.execute_program(test_key='test')
    assert sputnik.program.state == None


def test_homomorphic_nand():
    SputnikParser = Parser('tests/nand.sputnik')
    proggy = SputnikParser.get_program()

    sputnik = Sputnik(proggy, None)
    out = sputnik.execute_program(a=ciphertext1, b=ciphertext2, test_key=bootstrap_key)
    import pdb; pdb.set_trace()
