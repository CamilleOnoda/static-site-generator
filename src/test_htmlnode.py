import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        attr_dict = {
            "href": "website link",
            "target": "_blank",
            }
        node = HTMLNode(props=attr_dict)
        str_repr = ' href="website link" target="_blank"'
        node1 = HTMLNode(props=None)
        str_repr1 = ""
        self.assertEqual(node1.props_to_html(), str_repr1)
        self.assertEqual(node.props_to_html(), str_repr)

    def test_htmlNode_object(self):
        node = HTMLNode("h1","hello world")
        self.assertEqual(node.__repr__(),"HTMLNode(h1, hello world, children: None, None)")

    def test_default_to_none(self):
        node = HTMLNode("h1","hello world",)
        self.assertEqual(node.props,None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(),"<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I don't have any tag")
        self.assertEqual(node.to_html(), "I don't have any tag")

    def test_leafNode_object(self):
        node = LeafNode("p", "hello world")
        self.assertEqual(node.__repr__(), "LeafNode(p, hello world, None)")