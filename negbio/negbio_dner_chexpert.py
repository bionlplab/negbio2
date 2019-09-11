"""
Detect concepts from vocab

Usage:
    negbio_pipeline dner_chexpert [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .chexpert.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --mention_phrases_dir=<directory>       Directory containing mention phrases for each observation. [default: negbio/chexpert/phrases/mention]
    --unmention_phrases_dir=<directory>     Directory containing unmention phrases  for each observation.  [default: negbio/chexpert/phrases/unmention]
    --overwrite             Overwrite the output file.
"""
from pathlib import Path

from negbio.pipeline2.dner_chexpert import ChexpertExtractor
from negbio.cli_utils import parse_args, get_absolute_path
from negbio.pipeline2.pipeline import NegBioPipeline


if __name__ == '__main__':
    argv = parse_args(__doc__)

    argv = get_absolute_path(argv,
                             '--mention_phrases_dir',
                             'negbio/chexpert/phrases/mention')
    argv = get_absolute_path(argv,
                             '--unmention_phrases_dir',
                             'negbio/chexpert/phrases/unmention')

    extractor = ChexpertExtractor(Path(argv['--mention_phrases_dir']),
                                  Path(argv['--unmention_phrases_dir']),
                                  verbose=argv['--verbose'])
    pipeline = NegBioPipeline(pipeline=[('ChexpertExtractor', extractor)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
