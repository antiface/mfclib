#!/usr/bin/python
# coding: latin-1

import sys, os
from mfclib import mfclib

sys.path.append('./')


#UnitTest - TDD
db_name = '.mfclib_unittest.data'
os.system('rm ' + db_name)

test = mfclib(db_name)
#add tag test
test.add_tag('English')
tags = test.get_tags()

#add_tag
assert len(tags['tags']) == 1 and tags['tags'][0]['tag_id'] == 1 and tags['tags'][0]['tag'] == 'English', 'Add tag test FAILED!'

test.add_tag('English')
tags = test.get_tags()

assert len(tags['tags']) == 1, 'Add duplicated tag FAILED!'

test.add_tag('French')
tags = test.get_tags()

assert len(tags['tags']) == 2, 'Add second tag test FAILED!'

#get_tag_id
assert 1 == test.get_tag_id('English'), 'Add get tag_id FAILED!'
assert 1 == test.get_tag_id('englisH'), 'Add get tag_id FAILED!'
assert 2 == test.get_tag_id('FrEnCh'), 'Add get tag_id FAILED!'
assert None == test.get_tag_id('German'), 'Add get tag_id FAILED!'
#get_tag_by_id
assert 'English' == test.get_tag_by_id(1), 'Add get tag_by_id FAILED!'
assert 'French' == test.get_tag_by_id(2), 'Add get tag_by_id FAILED!'
assert None == test.get_tag_by_id(3), 'Add get tag_id FAILED!'

test.edit_tag(2, 'Fremch')

assert 'Fremch' == test.get_tag_by_id(2), 'Edit tag FAILED!'
assert 2 == test.get_tag_id("FREMch"), 'Edit tag FAILED!'
assert None == test.get_tag_id("FREnch"), 'Edit tag FAILED!'

test.del_tag(2)
assert None == test.get_tag_id(2), 'Delete tag FAILED!'

test.add_tag('French')
assert 3 == test.get_tag_id('French'), 'Get tag id FAILED!'

#add_term
id1 = test.add_term('World')

#get_term_id
id2 = test.get_term_id('World')

assert id1 == id2, 'Add Term/Get Term Id FAILED!'

#tag / get_term_id /get_tag_id / get_terms_by_tag_id
assert test.tag(test.get_term_id('World'),test.get_tag_id('English')), 'Tag fail'
assert not test.tag(test.get_term_id('Monde'),test.get_tag_id('French')), 'Tag fail'
assert test.get_terms_by_tag_id(1)['terms'][0]['term_id'] == 1, 'Get terms by tag id Fail'
assert len(test.get_terms_by_tag('English')['terms']) == 1, 'Get terms by tag FAIL'

#get_tags_by_term_id
test.tag(1,3)
ids = test.get_tags_by_term_id(1)

assert len(ids['tags']) == 2, 'Get tags by term_id FAIL'

laws = test.add_term('Laws')

#get karma / get level

assert round(test.get_karma(1)['karma'],2) == 0.1, 'Karma Fail'
assert round(test.karma(1, True)['karma'],2) == 0.32, 'Level Fail'
assert test.get_karma(1)['level'] == 1, 'Level Fail'


#add phrase / get phrase
text = 'Hello World of Laws!'
assert test.add_phrase(text)[0] == 1, 'Add phrase fail'
assert test.get_phrase_id(text)[0] == 1, 'Get Phrase Id Fail'


#link / get linked terms
test.link(2,1,1)
print test.get_linked_terms(1)

print test.rel(1,1,2)
print test.get_rel(1,1)


test.close()

print 'Congrats! Test passed!'
