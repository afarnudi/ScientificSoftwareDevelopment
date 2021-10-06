#import pytest
from capitalise import capitalise

def test_capitalise():
    assert(capitalise("ali")=="Ali")

def test_capitalise_second_word_not_capitalised():
    assert(capitalise('ali farnudi')!='Ali Farnudi')

#def test_raises_exception_on_non_string_arguments():
#    with pytest.raises(AttributeError):
    #with pytest.raises(TypeError):
#        capitalise(9)
