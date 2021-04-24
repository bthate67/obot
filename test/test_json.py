# This file is placed in the Public Domain.

from obj import O, Obj, Object, default
from zzz import js, unittest

class Test_JSON(unittest.TestCase):

    def test_jsonO(self):
        o = O()
        o.test = "bla"
        v = js.dumps(o, default=default)
        self.assertTrue(str(o) == v)

    def test_jsonObject(self):
        o = Object()
        o.test = "bla"
        v = js.dumps(o, default=default)
        self.assertEqual(str(o),v)

    def test_jsonreconstructO(self):
        o = O()
        o.test = "bla"
        v = js.dumps(o, default=default)
        vv = js.loads(v, object_hook=Obj)
        self.assertEqual(repr(o), repr(vv))

    def test_jsonreconstruvtObject(self):
        o = Object()
        o.test = "bla"
        v = js.dumps(o, default=default)
        vv = js.loads(v, object_hook=Obj)
        self.assertEqual(repr(o), repr(vv))
    