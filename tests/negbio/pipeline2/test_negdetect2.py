import re

import bioc

from negbio.pipeline2.negdetect2 import get_text


def test_get_text():
    s = bioc.BioCSentence()
    s.offset = 100
    s.text = 'no evidence of pulmonary edema'
    loc = (25+100, 30+100)

    expected = 'no evidence of pulmonary $X$'
    actual = get_text(s, loc)
    assert expected == actual, '{} vs {}'.format(expected, actual)


def test_pattern():
    text = 'no evidence of pulmonary $X$'
    pattern = re.compile('no evidence of ([^ ]+ ){,3}\$X\$', re.I)
    m = pattern.search(text)
    assert m is not None


if __name__ == '__main__':
    test_get_text()
    test_pattern()
