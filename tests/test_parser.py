from sputnik.parser import Parser


def test_parser_read_testfile():
    SputnikParser = Parser('tests/parser.sputnik')

    assert SputnikParser.raw_data is not ''
    assert len(SputnikParser.lines) == 3
    assert len(SputnikParser.operations) == 3

    # Test Operations lengths
    bootstrap = SputnikParser.operations[0]
    assert len(bootstrap) == 3

    xor = SputnikParser.operations[1]
    assert len(xor) == 5

    end = SputnikParser.operations[2]
    assert len(end) == 1
