import tempfile
from pathlib import Path
from subprocess import call

import bioc
from bioc import biocitertools

from tests.negbio.utils import get_example_dir


def test_neg_chexpert():
    source = get_example_dir() / '1.xml'
    output = Path(tempfile.mktemp())
    cmd = f'python negbio/main_chexpert.py bioc --output={output} {source}'
    call(cmd.split())
    with open(output) as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.neg_chexpert.xml') as fp:
        expected = bioc.load(fp)

    assert len(actual.documents) == len(expected.documents)
    for actual_doc, expected_doc in zip(actual.documents, expected.documents):
        assert actual_doc.id == expected_doc.id
        actual_anns = list(biocitertools.annotations(actual_doc, level=bioc.PASSAGE))
        expected_anns = list(biocitertools.annotations(expected_doc, level=bioc.PASSAGE))
        assert len(actual_anns) == len(expected_anns)

        actual_anns = sorted(actual_anns, key=lambda a: a.total_span.offset)
        expected_anns = sorted(actual_anns, key=lambda a: a.total_span.offset)

        for actual_ann, expected_ann in zip(actual_anns, expected_anns):
            assert actual_ann.total_span == expected_ann.total_span
            if 'negation' in expected_ann.infons:
                assert actual_ann.infons['negation']
            else:
                assert 'negation' not in actual_ann.infons
