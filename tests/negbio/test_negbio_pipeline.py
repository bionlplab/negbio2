import tempfile
from pathlib import Path
from subprocess import call

import bioc
from bioc import biocitertools

from tests.negbio.utils import get_example_dir


def test_ssplit():
    source = get_example_dir() / '1.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.ssplit.xml'
    cmd = f'python negbio/negbio_pipeline.py ssplit --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ssplit.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.ssplit.xml') as fp:
        expected = bioc.load(fp)

    for actual_sen, expected_sen in zip(biocitertools.sentences(actual),
                                        biocitertools.sentences(expected)):
        assert actual_sen.offset == expected_sen.offset


def test_section_split():
    source = get_example_dir() / '1.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.secsplit.xml'
    cmd = f'python negbio/negbio_pipeline.py section_split ' \
          f'--output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.secsplit.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.secsplit.xml') as fp:
        expected = bioc.load(fp)

    for actual_doc, expected_doc in zip(actual.documents, expected.documents):
        for actual_p, expected_p in zip(actual_doc.passages, expected_doc.passages):
            assert actual_p.offset == expected_p.offset


def test_parse():
    source = get_example_dir() / '1.ssplit.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.parse.xml'
    cmd = f'python negbio/negbio_pipeline.py parse --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ssplit.parse.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.parse.xml') as fp:
        expected = bioc.load(fp)

    for actual_sen, expected_sen in zip(biocitertools.sentences(actual),
                                        biocitertools.sentences(expected)):
        assert actual_sen.infons['parse tree'] == expected_sen.infons['parse tree']


def test_ptb2ud():
    source = get_example_dir() / '1.parse.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.ptb2ud.xml'
    cmd = f'python negbio/negbio_pipeline.py ptb2ud --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.parse.ptb2ud.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.ptb2ud.xml') as fp:
        expected = bioc.load(fp)

    for actual_ann, expected_ann in zip(biocitertools.annotations(actual, level=bioc.SENTENCE),
                                        biocitertools.annotations(expected, level=bioc.SENTENCE)):
        assert actual_ann.text == expected_ann.text


def test_neg():
    source = get_example_dir() / '1.ptb2ud.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.neg.xml'
    cmd = f'python negbio/negbio_pipeline.py neg --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ptb2ud.neg.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.neg.xml') as fp:
        expected = bioc.load(fp)

    for actual_ann, expected_ann in zip(biocitertools.annotations(actual, level=bioc.SENTENCE),
                                        biocitertools.annotations(expected, level=bioc.SENTENCE)):
        if 'negation' in expected_ann.infons:
            assert actual_ann.infons['negation']
        else:
            assert 'negation' not in actual_ann.infons


def test_neg_chexpert():
    source = get_example_dir() / '1.ptb2ud.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.neg_chexpert.xml'
    cmd = f'python negbio/negbio_pipeline.py neg_chexpert --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ptb2ud.neg_chexpert.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.neg.xml') as fp:
        expected = bioc.load(fp)

    for actual_ann, expected_ann in zip(biocitertools.annotations(actual, level=bioc.SENTENCE),
                                        biocitertools.annotations(expected, level=bioc.SENTENCE)):
        if 'negation' in expected_ann.infons:
            assert actual_ann.infons['negation']
        else:
            assert 'negation' not in actual_ann.infons


def test_cleanup():
    source = get_example_dir() / '1.ptb2ud.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.cleanup.xml'
    cmd = f'python negbio/negbio_pipeline.py cleanup --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ptb2ud.cleanup.xml') as fp:
        actual = bioc.load(fp)

    sens = list(biocitertools.sentences(actual))
    assert len(sens) == 0


def test_text2bioc():
    source1 = get_example_dir() / '00019248.txt'
    source2 = get_example_dir() / '00000086.txt'
    output = tempfile.mktemp()
    cmd = f'python negbio/negbio_pipeline.py text2bioc --output={output} {source1} {source2}'
    call(cmd.split())
    with open(output) as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.xml') as fp:
        expected = bioc.load(fp)

    for actual_doc, expected_doc in zip(actual.documents, expected.documents):
        assert actual_doc.id == expected_doc.id
        for actual_p, expected_p in zip(actual_doc.passages, expected_doc.passages):
            assert actual_p.text.strip() == expected_p.text.strip()


def test_dner_chexpert():
    source = get_example_dir() / '1.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.dner_chexpert.xml'
    cmd = f'python negbio/negbio_pipeline.py dner_chexpert ' \
          f'--output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.dner_chexpert.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.neg.xml') as fp:
        expected = bioc.load(fp)

    for actual_ann, expected_ann in zip(biocitertools.annotations(actual, level=bioc.SENTENCE),
                                        biocitertools.annotations(expected, level=bioc.SENTENCE)):
        assert actual_ann.text == expected_ann.text