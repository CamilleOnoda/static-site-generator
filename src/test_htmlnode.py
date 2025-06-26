import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertEqual(node.__repr__(),
                         "HTMLNode(h1, hello world, children: None, None)")

    def test_default_to_none(self):
        node = HTMLNode("h1","hello world",)
        self.assertEqual(node.props,None)


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(),
                         "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),
                         '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I don't have any tag")
        self.assertEqual(node.to_html(), 
                         "I don't have any tag")

    def test_leafNode_object(self):
        node = LeafNode("p", "hello world")
        self.assertEqual(node.__repr__(), 
                         "LeafNode(p, hello world, None)")
        
    def test_leafNode_with_props(self):
        node = LeafNode("div", "hello world", {'class':'container', 'id':'main'})
        self.assertEqual(node.to_html(), 
                         '<div class="container" id="main">hello world</div>')


    def test_parentNode_object(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.__repr__(), 
                         f"ParentNode(div, children: [LeafNode(span, child, None)], None)")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), 
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span><b>grandchild</b></span></div>",)
        
    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("b", "child")
        child_node2 = LeafNode("h1", "hello world")
        child_node3 = LeafNode("p", "some paragraph")
        parent_node = ParentNode("div", [child_node1,child_node2,child_node3])
        self.assertEqual(parent_node.to_html(), 
                         "<div><b>child</b><h1>hello world</h1>"
                         "<p>some paragraph</p></div>")
    
    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("b", "hello world")
            parent_node = ParentNode(None, [child_node]).to_html()
    
    def test_to_html_no_chilren(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None).to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parentNode_with_props(self):
        child_node = LeafNode("p", "some paragraph")
        parent_node = ParentNode("div", [child_node], 
                                 {'class':'container', 'id':'main'})
        self.assertEqual(parent_node.to_html(), 
                         '<div class="container" id="main">'
                         '<p>some paragraph</p></div>')
        
    def test_to_html_deep_nesting(self):
        great_great_grandchild = LeafNode("b", "very deep text")
        great_grandchild = ParentNode("p", [great_great_grandchild])
        grandchild = ParentNode("article", [great_grandchild])
        child = ParentNode("section", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(),
                          '<div><section><article><p><b>very deep text</b>'
                          '</p></article></section></div>')


if __name__ == "__main__":
    unittest.main()