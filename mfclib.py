#!/usr/bin/python
# coding: latin-1

import hashlib
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
    	self._db_exec("create table fc_phrases (phrase_id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, md5 TEXT);")
    	self._db_exec("create table fc_rel (tag_id INTEGER, term_id1 INTEGER, term_id2 INTEGER);")
    	self._db_exec("create table fc_sym (tag_id1 INTEGER, term_id1 INTEGER, tag_id2 INTEGER, term_id2 INTEGER);")
    	self._db_exec("create table fc_links (tag_id INTEGER, term_id INTEGER, phrase_id INTEGER);")
    	self._db_exec("create table fc_review (term_id INTEGER, date INTEGER);")
    	self._db_exec("create table fc_status (term_id INTEGER, corrects INTEGER, errors INTEGER, karma REAL);")
    
    	return None
    
    def link(self, tag_id, term_id, phrase_id):
    	if not self.is_int(phrase_id) or not self.is_int(tag_id) or not self.is_int(term_id):
    		return None
    
    
                data = {'phrase_id':phrase_id, 'tag_id' : tag_id, 'term_id' : term_id}
                self._db_exec("insert into fc_links (tag_id, term_id, phrase_id) values (:tag_id, :term_id, :phrase_id)", data)
    	return True
    
    def get_linked_terms(self, phrase_id):
    	if not self.is_int(phrase_id):
    		return None
    	self._db_exec("select fc_links.term_id, fc_terms.term from fc_links, fc_terms where fc_links.term_id = fc_terms.term_id and fc_links.phrase_id = :phrase_id", {'phrase_id':phrase_id})
        return self._db_one()
    
    def get_phrase_by_id(self, phrase_id ):
    	self._db_exec("select phrase from fc_phrases where phrase_id = :phrase_id", {'phrase_id':phrase_id})
        return self._db_one()
    
    
    def get_phrase_id(self, phrase):
    	m = hashlib.md5()
        m.update(phrase.upper())
        md5 = m.hexdigest()

    	self._db_exec("select phrase_id from fc_phrases where md5 = :md5", {'md5':md5})
        return self._db_one()
    
    def get_phrase_id_by_md5(self, md5):
    	self._db_exec("select phrase_id from fc_phrases where md5 = :md5", {'md5':md5})
        return self._db_one()
    
    
    def add_phrase(self, text):
    	m = hashlib.md5()
    	m.update(text.upper())
    	md5 = m.hexdigest()
    
    	phrase_id = self.get_phrase_id_by_md5(md5)
    
    	if phrase_id == None:
    		data = {'phrase_id':phrase_id, 'text' : text, 'md5' : md5}
    		self._db_exec("insert into fc_phrases (phrase_id, text, md5) values (:phrase_id, :text, :md5)", data)
    		phrase_id = self.get_phrase_id_by_md5(md5)
    
    	return phrase_id
    
    def add_tag(self, name):
    	data = {'tag' : name}
    
    	self._db_exec("select tag_id from fc_tags where tag = :tag", data)
    	if self._db_one() == None:
    		self._db_exec("insert into fc_tags (tag) values (:tag)", data)
    		self._db_exec("select tag_id from fc_tags where tag = :tag", data)
    		return {'tag_id' : self._db_one()[0]}
    
    	return None
    
    def edit_tag(self, tag_id, name):
    	self._db_exec("update fc_tags set tag = :tag where tag_id = :tag_id", {'tag':name, 'tag_id':tag_id})
    
    def del_tag(self, tag_id):
    	self._db_exec("delete from fc_tags where tag_id = :tag_id", {'tag_id':tag_id})
    
    
    def get_tags(self):
    	self._db_exec("select * from fc_tags")
    	obj = {'tags':[]}
    	cache = self._db_fetch_all()
    	for tag in cache:
    		obj['tags'].append({'tag_id':tag[0], 'tag':tag[1]})
    
    	return obj
    
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
    	res = self._db_one()[0]
    	if res == 0:
    		self._db_exec("insert into fc_terms (term) values (:term)", {'term' : term})
    		self._db_exec("select term_id from fc_terms where term like :term", {'term' : term})
    		res = self._db_one()[0]
    		self._db_exec("insert into fc_status (term_id, corrects, errors, karma) values (:id,0,0,0.1)", {'id' : res})
    
    	return res
    
    def get_term_id(self, term):
    	data = {'term': term}
    	self._db_exec("select term_id from fc_terms where term like :term", data)
    	res = self._db_one()
    	if res != None:
    		return res[0]
    	return None
    
    def get_term_by_id(self, term_id):
    
    	if not self.is_int(term_id):
    		return None
    
    	data = {'term_id': term_id}
    
    	self._db_exec("select term from fc_terms where term_id = :term_id", data)
    
    	res = self._db_one()
    
    	if res != None:
    		return res[0]
    	return None
    
    def tag(self, term_id, tag_id):
    	if self.is_int(term_id) == False or self.is_int(tag_id) == False:
    		return False
    
    
    	data = {'term_id' : term_id, 'tag_id' : tag_id}
    
    	self._db_exec("select count(*) total from fc_taggeds where term_id = :term_id and tag_id = :tag_id", data)
    	if self._db_one()[0] == 0:
    		self._db_exec("insert into fc_taggeds (term_id, tag_id) values (:term_id, :tag_id)", data)
    		return True
    	return False
    
    
    def get_karma(self, term_id):
    	self._db_exec('select karma, corrects, errors from fc_status where term_id = :term_id', {'term_id':term_id})
    	res = self._db_one()
    	if res == None:
    		return None
    	return {'karma':res[0], 'corrects' : res[1], 'errors' : res[2], 'level':self._get_level(res[0])}
    
    
    def karma(self, term_id, ok):
    
    	status = self.get_karma(term_id)
    
    	if status == None:
    		return None
    
    	karma = status[0]
    
    	if ok == True:
    		karma = karma + ((karma * 2.2) + ((status[1] - status[2]) * 0.2))
    		if karma >= 1.0e14:
    			karma = 1.0e14
    		self._db_exec('update fc_status set corrects = corrects + 1, karma = :karma where term_id = :term_id',{'karma':karma, 'term_id':term_id})
    	else:
    
    		karma = karma + ((karma * 2.2) + (status[1]-status[2] * 0.3))
    		if karma < 0.1:
    			karma = 0.1
    		self._db_exec('update fc_status set errors = errors + 1, karma = :karma where term_id = :term_id',{'karma':karma, 'term_id':term_id})
    	return {'karma' : karma}
    
    
    def get_terms_by_tag_id(self, tag_id):
    
    	if not self.is_int(tag_id):
    		return None
    
    	self._db_exec("select term.term_id, term.term from fc_taggeds tagged, fc_terms term where tagged.tag_id = :tag_id", {'tag_id' : tag_id})
    	res = self._db_fetch_all()
    	obj = {'terms': []}
    	for i in res:
    		obj['terms'].append({'term_id':i[0], 'term' : i[1]})
    	return obj
    
    def get_terms_by_tag(self, tag):
    
    	tag_id = self.get_tag_id(tag)
    
    	if not self.is_int(tag_id):
    		return None
    
    	self._db_exec("select term.term_id, term.term from fc_taggeds tagged, fc_terms term where tagged.tag_id = :tag_id", {'tag_id' : tag_id})
        res = self._db_fetch_all()
        
        obj = {'terms': []}
        for i in res:
    		obj['terms'].append({'term_id':i[0], 'term' : i[1]})
    	return obj
        
        
    	return self._db_fetch_all()
    
    def get_tags_by_term_id(self, term_id):
    	self._db_exec("select fc_taggeds.tag_id tag_id, fc_tags.tag tag from fc_taggeds, fc_tags where fc_tags.tag_id = fc_taggeds.tag_id and  term_id = :term_id", {'term_id':term_id})
        res = self._db_fetch_all()
        obj = {'tags': []}
        for i in res:
        	obj['tags'].append({'tag_id':i[0], 'tag' : i[1]})
    	return obj
    
    def _get_level(self, karma):
    	if karma < 151.1:
    		return 1
    	elif karma < 50915:
    		return 2
    	elif karma < 17084817:
    		return 3
    	elif karma < 58702992580:
    		return 4
    	elif karma < 6.30318583297e13:
    		return 5
    	elif karma == 1e14:
    		return 6
    
    def close(self):
    	self._db.commit()
    	self._db.close()
    
    def is_int(self, s):
    	if s == None:
    		return False
    	try:
    		int(s)
    		return True
    	except ValueError:
    		return False

