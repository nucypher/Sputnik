import nufhe
import numpy
import pickle
import pytest

from reikna.cluda import any_api
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




def test_homomorphic_otp():
    SputnikParser = Parser('tests/otp.sputnik')
    proggy = SputnikParser.get_program()
    sputnik = Sputnik(proggy, None)

    rng = numpy.random.RandomState()
    secret_key, bootstrap_key = nufhe.make_key_pair(sputnik.thr, rng, transform_type='NTT')

    size = 32

    plain = numpy.array(
        [False, False, False, False, False, False, False, False,
         True, True, True, True, True, True, True, True,
         False, False, False, False, False, False, False, False,
         True, True, True, True, True, True, True, True]
    )
    pad = rng.randint(0, 2, size=size).astype(numpy.bool)

    enc_plain = nufhe.encrypt(sputnik.thr, rng, secret_key, plain)
    enc_pad = nufhe.encrypt(sputnik.thr, rng, secret_key, pad)

    enc_otp = sputnik.execute_program(plain=enc_plain, pad=enc_pad, test_key=bootstrap_key)
    assert plain is not enc_plain
    assert enc_otp is not enc_plain

    dec_otp = nufhe.decrypt(sputnik.thr, secret_key, enc_otp)
    dec_pad = nufhe.decrypt(sputnik.thr, secret_key, enc_pad)
    assert dec_otp is not plain
    assert (plain ^ pad).all() == dec_otp.all()


#def test_engine_halt():
#    SputnikParser = Parser('tests/abc.sputnik')
#    proggy = SputnikParser.get_program()
#    sputnik = Sputnik(proggy, None)
#    output = sputnik.execute_program(a=1, b=2, c=3)
#
# 
#def test_engine_OR():
#    SputnikParser = Parser('tests/or.sputnik')
#    proggy = SputnikParser.get_program()
#
#    sputnik = Sputnik(proggy, None)
#    var1 = 10
#    var2 = 21
#    sputnik.execute_program(a=var1, b=var2)
#    assert sputnik.program.state == (var1 | var2)
#
#
#def test_engine_AND():
#    SputnikParser = Parser('tests/and.sputnik')
#    proggy = SputnikParser.get_program()
#
#    sputnik = Sputnik(proggy, None)
#    var1 = 12
#    var2 = 13
#    sputnik.execute_program(a=var1, b=var2)
#    assert sputnik.program.state == (var1 & var2)
#
#
#def test_engine_XOR():
#    SputnikParser = Parser('tests/xor.sputnik')
#    proggy = SputnikParser.get_program()
#
#    sputnik = Sputnik(proggy, None)
#    var1 = 5
#    var2 = 55
#    sputnik.execute_program(a=var1, b=var2)
#    assert sputnik.program.state == (var1 ^ var2)
#
#
#def test_engine_XOR_combo():
#    SputnikParser = Parser('tests/xor-combo.sputnik')
#    proggy = SputnikParser.get_program()
#
#    sputnik = Sputnik(proggy, None)
#    var1 = 7
#    var2 = 17
#    sputnik.execute_program(a=var1, b=var2)
#    assert sputnik.program.state == ((var1 | var2) ^ (var1 & var2)) & (var1 ^ var2)
#
#
#def test_engine_entrance():
#    SputnikParser = Parser('tests/entrance_vars.sputnik')
#    proggy = SputnikParser.get_program()
#
#    sputnik = Sputnik(proggy, None)
#    sputnik.execute_program(test_key='test')
#    assert sputnik.program.state == None
