from negbio.pipeline.section_split import split_document
from tests.negbio.utils import text_to_bioc


def test_split_document():
    text = """findings: pa and lat cxr at 7:34 p.m.. heart and mediastinum are
stable. lungs are unchanged. air- filled cystic changes. no
pneumothorax. osseous structures unchanged scoliosis
impression: stable chest.
dictating 
"""
    d = text_to_bioc([text], type='d/p')
    d = split_document(d)
    assert len(d.passages) == 4
    assert d.passages[0].text == 'findings:'
    assert d.passages[1].text == """pa and lat cxr at 7:34 p.m.. heart and mediastinum are
stable. lungs are unchanged. air- filled cystic changes. no
pneumothorax. osseous structures unchanged scoliosis"""
    assert d.passages[2].text == 'impression:'
    assert d.passages[3].text == """stable chest.
dictating"""
