import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        node2 = TextNode("This is a italic text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        node2 = TextNode("This is a code text node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "url")
        node2 = TextNode("This is a link text node", TextType.LINK, "url")
        self.assertEqual(node, node2)

    def test_eq_image(self):
        node = TextNode("This is an image node", TextType.IMAGE)
        node2 = TextNode("This is an image node", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        # Test that the default value is None when no URL is provided.
        node = TextNode("This is a link text node", TextType.LINK)
        self.assertEqual(node.url,None)

    def test_not_eq_url(self):
        # Catch potential bugs where the URL might not be properly handled or transferred
        # Verify that the equality comparison works for nodes with different
        # URL values.
        node = TextNode("This is a link text node", TextType.LINK, "url")
        node2 = TextNode("This is a link text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_invalid_text_type(self):
        # Try to create a TextNode with something that's not a TextType instance
        # and expect a TypeError to be raised
        with self.assertRaises(TypeError):
            node = TextNode("this is a text node", "Not a valid TextType")

    def test_case_sensitivity(self):
        node = TextNode("This is a text", TextType.TEXT)
        node2 = TextNode("this is a text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url_normalization(self):
        node = TextNode("This a link node", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This a link node", TextType.LINK, "http://www.example.com")
        self.assertNotEqual(node,node2)

    def test_type_consistency(self):
        node = TextNode("This is a text node", TextType.TEXT)
        not_a_node = "not a node"
        self.assertNotEqual(node, not_a_node)

    def test_textnode_object(self):
        node = TextNode("This a link node", TextType.LINK)
        self.assertEqual(node.__repr__(), "TextNode(This a link node, link, None)")

if __name__ == "__main__":
    unittest.main()