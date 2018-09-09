#1
import nufhe
import numpy
import web3
import pickle
from web3.auto.gethdev import w3
from binascii import unhexlify
from sputnik.engine import Sputnik
from sputnik.parser import Parser
from vyper import compiler


if __name__ == '__main__':
    #2
    # Setup Sputnik and deploy vyper contract
    SputnikParser = Parser('contracts/otp.sputnik')
    proggy = SputnikParser.get_program()
    sputnik = Sputnik(proggy, None)

    with open('contracts/hasheater.vy', 'r') as f:
        contract_code = f.read()

    contract_bytecode = compiler.compile(contract_code).hex()
    contract_abi = compiler.mk_full_signature(contract_code)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx_hash = Contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_abi)

    #3
    # Setup numpy (insecure, but it's a hackathon...)
    rng = numpy.random.RandomState()

    #4
    # Setup NuFHE
    secret_key, bootstrap_key = nufhe.make_key_pair(sputnik.thr, rng, transform_type='NTT')
    size = 32

    #5
    # Setup our plaintext and pad, then encrypt them
    plain = numpy.array(
        [False, False, False, False, False, False, False, False,
         True, True, True, True, True, True, True, True,
         False, False, False, False, False, False, False, False,
         True, True, True, True, True, True, True, True]
    )
    pad = rng.randint(0, 2, size=size).astype(numpy.bool)

    enc_plain = nufhe.encrypt(sputnik.thr, rng, secret_key, plain)
    enc_pad = nufhe.encrypt(sputnik.thr, rng, secret_key, pad)

    #6
    # Execute the homomorphic contract
    contract_state_out, merkle_tree = sputnik.execute_program(plain=enc_plain, pad=enc_pad, test_key=bootstrap_key)

    #7 Show the reference vs the homomorphic contract output
    reference = plain ^ pad
    dec_fhe_ref = nufhe.decrypt(sputnik.thr, secret_key, contract_state_out)

    #8
    ## Commit the root to the blockchain and print it 
    root = merkle_tree.get_merkle_root()
    h1 = contract.functions.add(root).transact()
    w3.eth.waitForTransactionReceipt(h1)
    print(root)

    #9
    # Verify that logic computation was done by checking the blockchain
    contract_execution_root = contract.functions.read(0).call()
