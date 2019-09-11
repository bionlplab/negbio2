from StanfordDependencies import StanfordDependencies

from negbio.pipeline2.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc


class TestNegBioPtb2DepConverter:
    def test_convert_doc2(self):
        text = "Can't exclude 1 cm lesion in or near lower esophagus (for example series 2 image 91) BOOKMARK (1.1 cm) appearing or better demonstrated."
        tree = "(S1 (S (S (VP (MD Can) (RB n't) (VP (VB exclude) (NP (NP (ADJP (CD 1) (NN cm)) (NN lesion)) (PP (IN in) (NP (NP (NP (test_convert_doc2CC or) (JJ near) (NP (NP (JJR lower) (NN esophagus)) (PRN (-LRB- -LRB-) (PP (IN for) (NP (NN example))) (NP (NN series) (CD 2) (NN image) (CD 91)) (-RRB- -RRB-))) (NN BOOKMARK)) (PRN (-LRB- -LRB-) (NP (CD 1.1) (NN cm)) (-RRB- -RRB-))) (VP (VBG appearing) (ADVP (CC or) (ADVP (RBR better))) (VP (VBN demonstrated))))))))) (. .)))"
        d = text_to_bioc([text], type='d/p/s')
        s = d.passages[0].sentences[0]
        s.infons['parse tree'] = tree

        c = NegBioPtb2DepConverter()
        c(d)
