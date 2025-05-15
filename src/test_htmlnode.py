import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        attr_dict = {
            "href": "website link",
            "target": "_blank",
            }
        node = HTMLNode(props=attr_dict)
        str_repr = ' href="website link" target="_blank"'
        self.assertEqual(node.props_to_html(), str_repr)

    def test_htmlNode_object(self):
        node = HTMLNode("h1","hello world")
        self.assertEqual(node.__repr__(),"HTMLNode(h1, hello world, None, None)")

    def test_default_to_none(self):
        node = HTMLNode("h1","hello world",)
        self.assertEqual(node.props,None)
        