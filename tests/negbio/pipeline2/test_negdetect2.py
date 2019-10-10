from pathlib import Path

import bioc

import tests
from negbio.pipeline2.negdetect2 import get_text

__tests_dir = Path(tests.__file__).parent

phrases_file = __tests_dir / 'data/patterns/chexpert_phrases.yml'


def test_get_text():
    s = bioc.BioCSentence()
    s.offset = 100
    s.text = 'no evidence of pulmonary edema'
    loc = (25 + 100, 30 + 100)

    expected = 'no evidence of pulmonary $X$'
    actual = get_text(s, loc)
    assert expected == actual, '{} vs {}'.format(expected, actual)


# def test_pattern():
#     text = 'no evidence of pulmonary $X$'
#     pattern = re.compile('no evidence of ([^ ]+ ){,3}\$X\$', re.I)
#     m = pattern.search(text)
#     assert m is not None
#
#     pattern = """\\bdrain\\b"""
#     m = re.search(pattern, '123drain')
#     assert m is None
#
#     m = re.search(pattern, '123 drain.')
#     assert m is not None

# with open(phrases_file) as fp:
#     obj = yaml.load(fp, yaml.FullLoader)
#     pattern = obj['Support Devices']['include'][1]
#
# m = re.search(pattern, '123 lines.')
# assert m is not None
#
# m = re.search(pattern, '123line123')
# assert m is None


if __name__ == '__main__':
    test_get_text()
    # test_pattern()
