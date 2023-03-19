import unittest

from ws_login_flaskr.hal import HalCollection, HalItemFactory

class TestHalCollections(unittest.TestCase):
    def test_hal_empty_collection(self):
        resp = HalCollection().to_dict()
        self.assertEqual(resp['pageSize'], 0)
        self.assertEqual(resp['_links']['self']['href'], 'foobar')


class TestHalItemFactory(unittest.TestCase):
    def test_basic_object(self):
        data = { "id": 1, "foo": "bar"}

        hal_factory = HalItemFactory(lambda x: f'/data/{x["id"]}', lambda x: x)

        resp = hal_factory.to_hal(data)

        self.assertEqual(resp['_links']['self']['href'], '/data/1')
        # assert data is present
        self.assertEqual(resp['id'], 1)
        self.assertEqual(resp['foo'], 'bar')
    
    def test_basic_object_with_links(self):
        data = { "id": 1, "foo": "bar"}

        hal_factory = HalItemFactory(lambda x: f'/data/{x["id"]}', lambda x: x)
        hal_factory.with_link("something", lambda r: r + '/something')

        resp = hal_factory.to_hal(data)

        self.assertEqual(resp['_links']['self']['href'], '/data/1')
        self.assertEqual(resp['_links']['something']['href'], '/data/1/something')
        # assert data is present
        self.assertEqual(resp['id'], 1)
        self.assertEqual(resp['foo'], 'bar')

    def test_basic_object_with_embedded(self):
        data = { "id": 1, "foo": "bar"}

        hal_factory = HalItemFactory(lambda x: f'/data/{x["id"]}', lambda x: x)
        embedded_factory = HalItemFactory(lambda x: f'/some_other_value/{x["id"]}', lambda x: x)
        hal_factory.with_embedded("nested", embedded_factory, lambda x: {'id': 2, 'embedded': 'value'})

        resp = hal_factory.to_hal(data, with_embedded=['nested'])

        self.assertEqual(resp['_links']['self']['href'], '/data/1')
        self.assertEqual(resp['_embedded']['nested']['embedded'], 'value')
        # assert data is present
        self.assertEqual(resp['id'], 1)
        self.assertEqual(resp['foo'], 'bar')

    def test_basic_object_with_embedded_list(self):
        data = { "id": 1, "foo": "bar"}

        hal_factory = HalItemFactory(lambda x: f'/data/{x["id"]}', lambda x: x)
        embedded_factory = HalItemFactory(lambda x: f'/some_other_value/{x["id"]}', lambda x: x)
        hal_factory.with_embedded_list("nested", embedded_factory, lambda x: [{'id': 2, 'embedded': 'value'}, {'id': 2, 'embedded': 'value'},])

        resp = hal_factory.to_hal(data, with_embedded=['nested'])

        self.assertEqual(resp['_links']['self']['href'], '/data/1')
        self.assertEqual(resp['_embedded']['nested'][0]['embedded'], 'value')
        # assert data is present
        self.assertEqual(resp['id'], 1)
        self.assertEqual(resp['foo'], 'bar')


