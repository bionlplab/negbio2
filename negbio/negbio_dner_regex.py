"""
Detect concepts from vocab

Usage:
    negbio_dner_chexpert [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .chexpert.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --phrases_file=<file>   File containing phrases for each observation. [default: patterns/cxr14_phrases_v2.yml]
    --overwrite             Overwrite the output file.
"""
from pathlib import Path

from negbio.pipeline2.dner_chexpert import ChexpertExtractor
from negbio.cli_utils import parse_args
from negbio.pipeline2.pipeline import NegBioPipeline


if __name__ == '__main__':
    argv = parse_args(__doc__)
    phrases_file = Path(argv['--phrases_file'])
    extractor = ChexpertExtractor(phrases_file, phrases_file.stem)
    pipeline = NegBioPipeline(pipeline=[('ChexpertExtractor', extractor)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
