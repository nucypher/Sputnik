hashes: bytes32[int128]
maxpointer: public(int128)

@public
def __init__():
    self.maxpointer = 0

@public
def add(_h: bytes32):
    self.hashes[self.maxpointer] = _h
    self.maxpointer += 1

@public
@constant
def read(_n: int128) -> bytes32:
    assert _n < self.maxpointer
    assert _n >= 0
    return self.hashes[_n]
