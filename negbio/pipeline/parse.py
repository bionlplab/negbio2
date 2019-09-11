import logging
import os
import string
import tempfile

from bllipparser import ModelFetcher
from bllipparser import RerankingParser


class Bllip(object):
    def __init__(self, model_dir=None):
        if model_dir is None:
            logging.debug("downloading GENIA+PubMed model if necessary ...")
            model_dir = ModelFetcher.download_and_install_model(
                'GENIA+PubMed', os.path.join(tempfile.gettempdir(), 'models'))
        self.model_dir = os.path.expanduser(model_dir)

        logging.debug('loading model %s ...' % self.model_dir)
        self.rrp = RerankingParser.from_unified_model_dir(self.model_dir)

    def parse(self, s):
        """Parse the sentence text using Reranking parser.

        Args:
            s(str): one sentence

        Returns:
            ScoredParse: parse tree, ScoredParse object in RerankingParser; None if failed
        """
        if s is None or (isinstance(s, str) and len(s.strip()) == 0):
            raise ValueError('Cannot parse empty sentence: {}'.format(s))

        try:
            nbest = self.rrp.parse(str(s))
            return nbest[0].ptb_parse
        except:
            raise ValueError('Cannot parse sentence: {}'.format(s))


class NegBioParser(Bllip):

    PARSE_TREE_ATTRIBUTE = 'parse tree'

    def parse_doc(self, document):
        """
        Parse sentences in BioC format

        Args:
            document(BioCDocument): one document

        Returns:
            BioCDocument
        """
        for passage in document.passages:
            for sentence in passage.sentences:
                text = sentence.text
                if text in string.punctuation:
                    sentence.infons[self.PARSE_TREE_ATTRIBUTE] = None
                    continue
                try:
                    tree = self.parse(text)
                    sentence.infons[self.PARSE_TREE_ATTRIBUTE] = str(tree)
                except:
                    sentence.infons[self.PARSE_TREE_ATTRIBUTE] = None
                    logging.exception('No parse tree for sentence: %s', sentence.offset)
        return document
