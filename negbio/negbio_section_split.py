"""
Split the report into sections based on titles.

Usage:
    negbio_pipeline section_split [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .secsplit.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --pattern=<file>        Specify section title list for matching.
    --overwrite             Overwrite the output file.
"""
import logging
import re

from negbio.cli_utils import parse_args
from negbio.pipeline2.pipeline import NegBioPipeline
from negbio.pipeline2.section_split import SectionSplitter


def read_section_titles(pathname):
    with open(pathname) as fp:
        titles = [line.strip() for line in fp]
        p = '|'.join(titles)
        logging.debug('Section patterns: %s', p)
        return re.compile(p, re.IGNORECASE | re.MULTILINE)


if __name__ == '__main__':
    argv = parse_args(__doc__)

    if argv['--pattern'] is None:
        pattern = None
    else:
        pattern = read_section_titles(argv['--pattern'])

    splitter = SectionSplitter(pattern)
    pipeline = NegBioPipeline(pipeline=[('SectionSplitter', splitter)])
    pipeline.scan(source=argv['<file>'], suffix=argv['--suffix'],
                  directory=argv['--output'], overwrite=argv['--overwrite'])
