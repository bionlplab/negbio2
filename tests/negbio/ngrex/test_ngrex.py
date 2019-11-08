import pytest

from negbio import ngrex


def test_compile():
    p = '@'
    with pytest.raises(TypeError):
        ngrex.compile(p)
