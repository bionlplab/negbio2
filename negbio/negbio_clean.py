"""
Clean up sentences

Usage:
    negbio_pipeline cleanup [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .negbio.xml]
    --verbose               Print more information about progress.
    --output=<directory>    Specify the output directory.
    --overwrite             Overwrite the output file.
"""

from negbio.cli_utils import parse_args
from negbio.pipeline2.cleanup import CleanUp
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    cleanup = CleanUp()
    pipeline = NegBioPipeline(pipeline=[('CleanUp', cleanup)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
