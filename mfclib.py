#!/usr/bin/python
# coding: latin-1

import sqlite3
import os
class mfclib:

	def _set_cache(self, key, val):
		self._cache[key] = val
		return val

	def _get_cache(self, key, default=None):
		if not self._cache.has_key(key):
			return default
		return self._cache[key]

	def _db_exec(self, sql, data=None):
		if not data == None:
			return self._c.execute(sql, data)
		return self._c.execute(sql)

	def _db_one(self):
		return self._c.fetchone()

	def _db_fetch_all(self):
		return self._c.fetchall()

	def __init__(self, file):
		self._cache = {}
		self._db = sqlite3.connect(file)
		self._c = self._db.cursor()
		if not self._has_db():
			self._create_structure()

	def _has_db(self):
		self._db_exec('select count(*) "total" from sqlite_master where type like "table" and name like "fc_terms"')
		if self._db_one()[0] == 0:
			return False
		return True

	def _create_structure(self):
		self._db_exec("create table fc_terms (term_id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT);")
		self._db_exec("create table fc_tags (tag_id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT);")
		self._db_exec("create table fc_taggeds (tag_id INTEGER, term_id INTEGER)")
		self._db_exec("create table fc_phrases (phrase_id INTEGER PRIMARY KEY AUTOINCREMENT);")
		self._db_exec("create table fc_rel (tag_id INTEGER, term_id1 INTEGER, term_id2 INTEGER);")
		self._db_exec("create table fc_sym (tag_id1 INTEGER, term_id1 INTEGER, tag_id2 INTEGER, term_id2 INTEGER);")
		self._db_exec("create table fc_links (tag_id INTEGER, term_id INTEGER, phrase_id INTEGER);")
		self._db_exec("create table fc_review (term_id INTEGER, date INTEGER);")
		self._db_exec("create table fc_status (term_id INTEGER, corrects INTEGER, errors INTEGER, karma INTEGER);")
		
		return None


	def add_tag(self, name):
		data = {'tag' : name}

		self._db_exec("select tag_id from fc_tags where tag = :tag", data)
		if self._db_one() == None:
			self._db_exec("insert into fc_tags (tag) values (:tag)", data)
			self._db_exec("select tag_id from fc_tags where tag = :tag", data)
			return self._db_one()[0]
		
		return None

	def edit_tag(self, tag_id, name):
		self._db_exec("update fc_tags set tag = :tag where tag_id = :tag_id", {'tag':name, 'tag_id':tag_id})

	def get_tags(self):
		self._db_exec("select * from fc_tags")
		cache = self._db_fetch_all()
		return cache

	def get_tag_id(self, tag):
		
		data = {'tag': tag}

		self._db_exec("select tag_id from fc_tags where tag like :tag", data)
		res = self._db_one()
		
		if res != None:
			return res[0]
		return None

	def get_tag_by_id(self, tag_id):
		
		data = {'tag_id': tag_id}

		self._db_exec("select tag from fc_tags where tag_id = :tag_id", data)
		res = self._db_one()
		
		if res != None:
			return res[0]
		return None



	def add_term(self, term):
		self._db_exec("select count(*) total from fc_terms where term like :term", {'term' : term})
		if self._db_one()[0] == 0:
			self._db_exec("insert into fc_terms (term) values (:term)", {'term' : term})
		
		self._db_exec("select term_id from fc_terms where term like :term", {'term' : term})
		return self._db_one()[0]

	def tag(self, term_id, tag_id):
		data = {'term_id' : term_id, 'tag_id' : tag_id}
		self._db_exec("select count(*) total from fc_taggeds where term_id = :term_id and tag_id = :tag_id", data)
		if self._db_one() == None:
			self._db_exec("insert into fc_taggeds (term_id, tag_id) values (:term_id, :tag_id)", data)
			return True
		return False

		


	def get_terms_by_tag(self, tag_id):
		
		self._db_exec("select terms.term_id, terms.term from fc_tagged, terms where fc_tagged.tag_id = :tag_id", {'tag_id' : tag_id})
		return self._db_fetch_all()	
	

#UnitTest		
if __name__ == '__main__':


	db_name = '/tmp/.mfclib_unittest.data'
	test = mfclib(db_name)
	#add tag test
	test.add_tag('English')
	tags = test.get_tags()

	assert str(tags) == "[(1, u'English')]", 'Add tag test FAILED!'

	test.add_tag('English')
	tags = test.get_tags()

	assert str(tags) == "[(1, u'English')]", 'Add duplicated tag FAILED!'

	test.add_tag('French')
	tags = test.get_tags()
	
	assert str(tags) == "[(1, u'English'), (2, u'French')]", 'Add second tag test FAILED!'
	assert 1 == test.get_tag_id('English'), 'Add get tag_id FAILED!'
	assert 1 == test.get_tag_id('englisH'), 'Add get tag_id FAILED!'
	assert 2 == test.get_tag_id('FrEnCh'), 'Add get tag_id FAILED!'
	assert None == test.get_tag_id('German'), 'Add get tag_id FAILED!'

	assert 'English' == test.get_tag_by_id(1), 'Add get tag_by_id FAILED!'
	assert 'French' == test.get_tag_by_id(2), 'Add get tag_by_id FAILED!'
	assert None == test.get_tag_by_id(3), 'Add get tag_id FAILED!'


	print 'Congrats! Test passed!'


	os.system('rm ' + db_name)

