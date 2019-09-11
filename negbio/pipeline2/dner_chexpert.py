import itertools
import re

from negbio.chexpert.stages.extract import Extractor
from negbio.pipeline2.pipeline import Pipe


class ChexpertExtractor(Extractor, Pipe):
    def __call__(self, document, *args, **kwargs):
        annotation_index = itertools.count()
        for passage in document.passages:
            for sentence in passage.sentences:
                obs_phrases = self.observation2mention_phrases.items()
                for observation, phrases in obs_phrases:
                    for phrase in phrases:
                        matches = re.finditer(phrase, sentence.text)
                        for match in matches:
                            start, end = match.span(0)
                            if self.overlaps_with_unmention(sentence, observation, start, end):
                                continue
                            self.add_match(passage, sentence, str(next(annotation_index)), phrase,
                                           observation, start, end)
        return document
