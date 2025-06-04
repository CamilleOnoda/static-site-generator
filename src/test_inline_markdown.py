import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestMarkdownToTextNode(unittest.TestCase):
    def test_markdown_delimiter_bold_two_asterisks(self):
        node = TextNode("This is a text with a **word** in bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
            TextNode(" in bold", TextType.TEXT)]
            )
        
    def test_markdown_delimiter_bold_two_underscores(self):
        node = TextNode("This is a text with a __word__ in bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
            TextNode(" in bold", TextType.TEXT)]
            )
        
    def test_markdown_delimiter_italic_underscore(self):
        node = TextNode("This is a text with a _word_ in italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" in italic", TextType.TEXT)]
            )
        
    def test_markdown_delimiter_italic_asterisk(self):
        node = TextNode("This is a text with a *word* in italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" in italic", TextType.TEXT)]
            )
                
    def test_markdown_delimiter_code(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)]
            )
        
    def test_invalid_Markdown(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a text with a `missing delimiter", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)