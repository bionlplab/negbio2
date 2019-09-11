import os
import tempfile

import bioc
import pytest

from negbio.pipeline.scan import scan_collection, scan_document
from tests.negbio.utils import text_to_bioc


def create_collections():
    filenames = []
    top_dir = tempfile.mkdtemp()
    for i in range(10):
        c = text_to_bioc(['No pneumothorax.'], 'c/d/p')
        filename = os.path.join(top_dir, '{}.xml'.format(i))
        with open(filename, 'w') as fp:
            bioc.dump(c, fp)
        filenames.append(filename)
    return filenames


def fake_collection_fn(collection, source):
    collection.source = source


def test_scan_collection():
    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    os.rmdir(output_dir)

    scan_collection(source=filenames, directory=output_dir, fn=fake_collection_fn,
                    non_sequences=['xxx'], suffix='.xml', verbose=True)
    for filename in filenames:
        filename = os.path.join(output_dir, os.path.basename(filename))
        with open(filename) as fp:
            c = bioc.load(fp)
        assert c.source == 'xxx'


def test_scan_collection_skip():
    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    # remove one file
    os.remove(filenames[0])
    scan_collection(source=filenames, directory=output_dir, fn=fake_collection_fn,
                    non_sequences=['xxx'], suffix='.xml', verbose=True)
    assert not os.path.exists(os.path.join(output_dir, filenames[0]))


def fake_document_fn(document, id):
    document.id = id
    return document


def test_scan_document():
    filenames = create_collections()

    output_dir = tempfile.mkdtemp()
    os.rmdir(output_dir)
    scan_document(source=filenames, directory=output_dir, fn=fake_document_fn,
                  non_sequences=['xxx'], suffix='.xml', verbose=True)
    for filename in filenames:
        filename = os.path.join(output_dir, os.path.basename(filename))
        with open(filename) as fp:
            c = bioc.load(fp)
        assert c.documents[0].id == 'xxx'


def test_scan_document_return_none():
    def fake_fn_no_return(*_):
        pass

    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    with pytest.raises(TypeError):
        scan_document(source=filenames, directory=output_dir, fn=fake_fn_no_return,
                      non_sequences=['xxx'], suffix='.xml', verbose=True)


def test_scan_document_error():
    def fake_document_fn2(_, __):
        raise KeyError

    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    scan_document(source=filenames, directory=output_dir, fn=fake_document_fn2,
                  non_sequences=['xxx'], suffix='.xml', verbose=True)
    for filename in filenames:
        filename = os.path.join(output_dir, os.path.basename(filename))
        with open(filename) as fp:
            c = bioc.load(fp)
        assert c.documents[0].id == ''


def test_scan_document_skip():
    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    os.remove(filenames[0])
    scan_document(source=filenames, directory=output_dir, fn=fake_document_fn,
                  non_sequences=['xxx'], suffix='.xml', verbose=True)
    assert not os.path.exists(os.path.join(output_dir, filenames[0]))