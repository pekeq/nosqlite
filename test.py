# encoding: utf8

import unittest
import nosqlite

class Test(unittest.TestCase):
    def setUp(self):
        self.client = nosqlite.Client('.')
        self.database = self.client.memory

    def test_unicode_string(self):
        collection = self.database.index
        dummy = nosqlite.client(u'.')

        collection.insert({'data':u'111'})
        collection.insert({u'xxx':u'table'})
        collection.copy(u'collection2')

        collection.insert({'a': u'あいうえお'})

        r = collection.find_one(fields=[u'data'])
        self.assertDictEqual({'data':'111'}, r)

    def test_keyword_escape(self):
        collection = self.database.index

        data = {'index':'index'}

        # insert
        collection.insert(data)
        collection.insert({'drop':'table'})

        # find
        self.assertDictEqual(data, collection.find_one(index='index'))
        self.assertDictEqual(data, collection.find_one(index='index', fields=["index"]))

        # update
        collection.update(data, index='index')

        # rename
        collection.rename('table')
        collection.rename('index')

        # copy
        collection.copy('create')

        # delete
        collection.delete(index='index')
        collection.delete()

    def test_nonexist_field(self):
        collection = self.database.collection
        data = {'key1':'val1', 'key2':'val2'}
        collection.insert(data)

        self.assertEqual(data, collection.find_one(key1='val1', fields=['key1','key2','key3']))

    def test_range_query(self):
        collection = self.database.collection
        collection.insert({'data': 5})
        collection.insert({'data':15})

        self.assertEqual([{'data':5}], list(collection.find('data > 0 AND data < 10')))
        self.assertEqual({'data':5}, collection.find_one('data > 0 AND data < 10'))
        self.assertEqual([{'data':5}], list(collection.find('data > ? AND data < ?', t=[0, 10])))
        self.assertEqual({'data':5}, collection.find_one('data > ? AND data < ?', t=[0, 10]))

    def test_sql_injection(self):
        collection = self.database.collection
        data = {'data':"'\""}
        collection.insert(data)

        self.assertEqual(data, collection.find_one(data="'\""))
        self.assertEqual(data, collection.find_one('data=?', t=["'\""]))

        collection.update({'data':"'\""}, data="'\"")
        collection.update({'data':"'\""}, 'data=?', t=["'\""])

        collection.copy('collection2', data="'\"")
        collection.copy('collection3', 'data=?', t=["'\""])

        collection.delete(data="'\"")
        collection.delete('data=?', t=["'\""])


if __name__ == '__main__':
    unittest.main()
