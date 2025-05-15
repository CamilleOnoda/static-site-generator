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
        