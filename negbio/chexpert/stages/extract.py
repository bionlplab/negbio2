"""Define observation extractor class."""
import re
import itertools
from collections import defaultdict
from tqdm import tqdm
from negbio.chexpert.constants import CARDIOMEGALY, ENLARGED_CARDIOMEDIASTINUM, OBSERVATION

import bioc


class Extractor(object):
    """Extract observations from impression sections of reports."""
    def __init__(self, mention_phrases_dir, unmention_phrases_dir,
                 verbose=False):
        self.verbose = verbose
        self.observation2mention_phrases\
            = self.load_phrases(mention_phrases_dir, "mention")
        self.observation2unmention_phrases\
            = self.load_phrases(unmention_phrases_dir, "unmention")
        self.add_unmention_phrases()

    def load_phrases(self, phrases_dir, phrases_type):
        """Read in map from observations to phrases for matching."""
        observation2phrases = defaultdict(list)
        for phrases_path in phrases_dir.glob("*.txt"):
            with phrases_path.open() as f:
                for line in f:
                    phrase = line.strip().replace("_", " ")
                    observation = phrases_path.stem.replace("_", " ").title()
                    if line:
                        observation2phrases[observation].append(phrase)

        if self.verbose:
            print("Loading {} phrases for {} observations.".format(phrases_type, len(observation2phrases)))

        return observation2phrases

    def add_unmention_phrases(self):
        cardiomegaly_mentions\
            = self.observation2mention_phrases[CARDIOMEGALY]
        enlarged_cardiom_mentions\
            = self.observation2mention_phrases[ENLARGED_CARDIOMEDIASTINUM]
        positional_phrases = (["over the", "overly the", "in the"],
                              ["", " superior", " left", " right"])
        positional_unmentions = [e1 + e2
                                 for e1 in positional_phrases[0]
                                 for e2 in positional_phrases[1]]
        cardiomegaly_unmentions = [e1 + " " + e2.replace("the ", "")
                                   for e1 in positional_unmentions
                                   for e2 in cardiomegaly_mentions
                                   if e2 not in ["cardiomegaly",
                                                 "cardiac enlargement"]]
        enlarged_cardiomediastinum_unmentions\
            = [e1 + " " + e2
               for e1 in positional_unmentions
               for e2 in enlarged_cardiom_mentions]

        self.observation2unmention_phrases[CARDIOMEGALY]\
            = cardiomegaly_unmentions
        self.observation2unmention_phrases[ENLARGED_CARDIOMEDIASTINUM]\
            = enlarged_cardiomediastinum_unmentions

    def overlaps_with_unmention(self, sentence, observation, start, end):
        """Return True if a given match overlaps with an unmention phrase."""
        unmention_overlap = False
        unmention_list = self.observation2unmention_phrases.get(observation,
                                                                [])
        for unmention in unmention_list:
            unmention_matches = re.finditer(unmention, sentence.text)
            for unmention_match in unmention_matches:
                unmention_start, unmention_end = unmention_match.span(0)
                if start < unmention_end and end > unmention_start:
                    unmention_overlap = True
                    break  # break early if overlap is found
            if unmention_overlap:
                break  # break early if overlap is found

        return unmention_overlap

    def add_match(self, impression, sentence, ann_index, phrase,
                  observation, start, end):
        """Add the match data and metadata to the impression object
        in place."""
        annotation = bioc.BioCAnnotation()
        annotation.id = ann_index
        annotation.infons['CUI'] = None
        annotation.infons['semtype'] = None
        annotation.infons['term'] = phrase
        annotation.infons[OBSERVATION] = observation
        annotation.infons['annotator'] = 'CheXpert labeler'
        length = end - start
        annotation.add_location(bioc.BioCLocation(sentence.offset + start,
                                                  length))
        annotation.text = sentence.text[start:start+length]

        impression.annotations.append(annotation)

