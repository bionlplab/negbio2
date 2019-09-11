from StanfordDependencies import StanfordDependencies

from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc


class TestNegBioPtb2DepConverter:
    def test_convert_doc(self):
        text = 'No pneumothorax.'
        tree = '(S1 (S (S (NP (DT No) (NN pneumothorax))) (. .)))'
        d = text_to_bioc([text], type='d/p/s')
        s = d.passages[0].sentences[0]
        s.infons['parse tree'] = tree

        c = NegBioPtb2DepConverter()
        d = c.convert_doc(d)
        s = d.passages[0].sentences[0]

        assert len(s.annotations) == 3, len(s.annotations)
        assert len(s.relations) == 2
        assert s.annotations[0].text == 'No'
        assert s.annotations[0].infons['tag'] == 'DT'
        assert s.annotations[0].infons['lemma'] == 'no'
        assert s.annotations[0].total_span.offset == 0

        assert s.annotations[1].text == 'pneumothorax'
        assert s.annotations[1].infons['tag'] == 'NN'
        assert s.annotations[1].infons['lemma'] == 'pneumothorax'
        assert s.annotations[1].total_span.offset == 3

        assert s.annotations[2].text == '.'
        assert s.annotations[2].infons['tag'] == '.'
        assert s.annotations[2].infons['lemma'] == '.'
        assert s.annotations[2].total_span.offset == 15

        assert s.relations[0].infons['dependency'] == 'neg'
        assert s.relations[0].nodes[0].refid == 'T0'
        assert s.relations[0].nodes[1].refid == 'T1'

        assert s.relations[1].infons['dependency'] == 'punct'
        assert s.relations[1].nodes[0].refid == 'T2'
        assert s.relations[1].nodes[1].refid == 'T1'

        # test empty parse tree
        del s.annotations[:]

        del s.infons['parse tree']
        c.convert_doc(d)

        s.infons['parse tree'] = None
        c.convert_doc(d)

    def test_convert_doc_no_jpype(self):
        c = NegBioPtb2DepConverter()
        c._backend = 'subprocess'
        c._sd = StanfordDependencies.get_instance(backend=c._backend)
        text = 'No pneumothorax.'
        tree = '(S1 (S (S (NP (DT No) (NN pneumothorax))) (. .)))'
        d = text_to_bioc([text], type='d/p/s')
        s = d.passages[0].sentences[0]
        s.infons['parse tree'] = tree
        d = c.convert_doc(d)
        s = d.passages[0].sentences[0]
        assert 'lemma' not in s.annotations[1].infons
