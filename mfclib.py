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
		self._db_exec('select count(*) "total" from sqlite_master where type like "table" and name like "fc_words"')
		if self._db_one()[0] == 0:
			return False
		return True

	def _create_structure(self):
		self._db_exec("create table fc_words (word_id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT);")
		self._db_exec("create table fc_tags (tag_id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT);")
		self._db_exec("create table fc_taggeds (tag_id INTEGER, word_id INTEGER)")
		self._db_exec("create table fc_phrases (phrase_id INTEGER PRIMARY KEY AUTOINCREMENT);")
		self._db_exec("create table fc_rel (tag_id INTEGER, word_id1 INTEGER, word_id2 INTEGER);")
		self._db_exec("create table fc_sym (tag_id1 INTEGER, word_id1 INTEGER, tag_id2 INTEGER, word_id2 INTEGER);")
		self._db_exec("create table fc_links (tag_id INTEGER, word_id INTEGER, phrase_id INTEGER);")
		self._db_exec("create table fc_review (word_id INTEGER, date INTEGER);")
		self._db_exec("create table fc_status (word_id INTEGER, corrects INTEGER, errors INTEGER, karma INTEGER);")
		
		return None


	def add_tag(self, name):
		data = {'tag' : name}

		self._db_exec("insert into fc_tags (tag) values (:tag)", data)
		self._set_cache('langs', None)
		self._db_exec("select tag_id from fc_tags where tag = :tag", data)
		return self._set_cache('word', self._db_one()[0])

	def edit_tag(self, tag_id, name):
		self._set_cache('tags', None)
		self._db_exec("update fc_tags set tag = :tag where tag_id = :tag_id", {'tag':name, 'tag_id':tag_id})


	def get_tags(self):
		cache = self._get_cache('tags')
		
		if cache == None:
			self._db_exec("select * from fc_tags")
			cache = self._db_fetch_all()
			self._set_cache('tags', cache)

		return cache

	def add_word(self, word):
		self._db_exec("select count(*) total from fc_words where word like :word", {'word' : word})
		if self._db_one()[0] == 0:
			self._db_exec("insert into fc_words (word) values (:word)", {'word' : word})
		
		self._db_exec("select word_id from fc_words where word like :word", {'word' : word})
		return self._db_one()[0]

	def tag(self, word_id, tag_id):
		data = {'word_id' : word_id, 'tag_id' : tag_id}
		self._db_exec("select count(*) total from fc_taggeds where word_id = :word_id and tag_id = :tag_id", data)
		if self._db_one()[0] == 0:
			self._db_exec("insert into fc_taggeds (word_id, tag_id) values (:word_id, :tag_id)", data)
			return True
		return False

		


	def get_words_by_tag(self, tag_id):
		
		self._db_exec("select words.word_id, words.word from fc_tagged, words where fc_tagged.tag_id = :tag_id", {'tag_id' : tag_id})
		return self._db_fetch_all()	
	

#UnitTest		

test = mfclib('test.data')

test.add_tag('English')

tags = test.get_tags()
print tags

word_id = test.add_word("Love")


print test.tag(word_id, tags[0][0])
print test.tag(word_id, tags[0][0])







os.system('rm test.data')

