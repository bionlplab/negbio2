import io
import logging
import os

import bioc
import tqdm


def scan_document(*_, **kwargs):
    """
    Scan each document in a list of BioC source files, apply fn, and print to directory.
    The output file names are directory/{stem}{suffix}

    Args:
        kwargs:
            source(list): a list of source pathnames
            directory(str): output directory
            fn:
                fn should expect the following arguments in this given order:
                    sequence1
                    sequence2
                    ...
                    non_sequence1
                    non_sequence2
                    ...
            suffix: suffix of output files
            skip_exists: if the output file exists, do not process the file
            verbose(boolean):
    """
    source = kwargs.pop('source')
    verbose = kwargs.pop('verbose', True)
    directory = os.path.expanduser(kwargs.pop('directory'))
    suffix = kwargs.pop('suffix')
    skip_exists = kwargs.pop('skip_exists', False)
    fn = kwargs.pop('fn')
    non_sequences = kwargs.pop('non_sequences', [])

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose, unit='collection'):
        stem = os.path.splitext(os.path.basename(pathname))[0]
        dstname = os.path.join(directory, '{}{}'.format(stem, suffix))

        if skip_exists:
            if os.path.exists(dstname):
                continue

        # add file lock
        lckname = dstname + '.lck'
        if os.path.exists(lckname):
            continue

        with open(lckname, 'w') as _:
            pass

        try:
            with io.open(pathname, encoding='utf8') as fp:
                collection = bioc.load(fp)
        except:
            logging.exception('Cannot read %s', pathname)
            continue

        new_documents = []
        for document in tqdm.tqdm(collection.documents, unit='doc', disable=not verbose, leave=False):
            try:
                document = fn(document, *non_sequences)
                if document is None or not isinstance(document, bioc.BioCDocument):
                    raise TypeError('The function need to return a document: %s' % fn)
            except TypeError as e:
                raise e
            except SystemExit:
                exit(1)
            except:
                logging.exception('Cannot process %s', document.id)
            new_documents.append(document)
        collection.documents = new_documents

        try:
            with io.open(dstname, 'w', encoding='utf8') as fp:
                bioc.dump(collection, fp)
        except:
            logging.exception('Cannot write %s', pathname)
        finally:
            os.remove(lckname)


def scan_collection(*_, **kwargs):
    """
    Scan each document in a list of BioC source files, apply fn, and print to directory.
    The output file names are directory/{stem}{suffix}

    Args:
        kwargs:
            source(list): a list of source pathnames
            directory(str): output directory
            fn:
                fn should expect the following arguments in this given order:
                    sequence1
                    sequence2
                    ...
                    non_sequence1
                    non_sequence2
                    ...
            suffix: suffix of output files
            verbose(boolean):
    """
    source = kwargs.pop('source')
    verbose = kwargs.pop('verbose', True)
    directory = os.path.expanduser(kwargs.pop('directory'))
    suffix = kwargs.pop('suffix')
    fn = kwargs.pop('fn')
    non_sequences = kwargs.pop('non_sequences', [])

    if not os.path.exists(directory):
        os.makedirs(directory)

    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose):
        stem = os.path.splitext(os.path.basename(pathname))[0]
        dstname = os.path.join(directory, '{}{}'.format(stem, suffix))
        try:
            with io.open(pathname, encoding='utf8') as fp:
                collection = bioc.load(fp)
            args = [collection] + non_sequences
            fn(*args)
            with io.open(dstname, 'w', encoding='utf8') as fp:
                bioc.dump(collection, fp)
        except:
            logging.exception('Cannot process %s', pathname)
