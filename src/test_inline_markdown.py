import unittest
from textnode import TextNode, TextType
from inline_markdown import (split_nodes_delimiter, 
                            extract_markdown_images,
                            extract_markdown_links,
                            split_nodes_link,
                            split_nodes_image)


class TestMarkdownToTextNode(unittest.TestCase):
    def test_markdown_delimiter_bold_two_asterisks(self):
        node = TextNode("This is a text with a **word** in bold",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
            TextNode(" in bold", TextType.TEXT)]
            )
        

    def test_markdown_delimiter_bold_two_underscores(self):
        node = TextNode("This is a text with a __word__ in bold",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
            TextNode(" in bold", TextType.TEXT)]
            )
        

    def test_markdown_delimiter_bold_asterisks_multiple(self):
        node = TextNode("This is a text with a **bold word** and **another**",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD)]
            )


    def test_markdown_delimiter_bold_underscores_multiple(self):
        node = TextNode("This is a text with a __bold word__ and __another__",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD)]
            )


    def test_markdown_delimiter_italic_underscore(self):
        node = TextNode("This is a text with a _word_ in italic",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" in italic", TextType.TEXT)]
            )
        

    def test_markdown_delimiter_italic_asterisk(self):
        node = TextNode("This is a text with a *word* in italic",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" in italic", TextType.TEXT)]
            )
        

    def test_markdown_delimiter_italic_underscore_multiple(self):
        node = TextNode("This is a text with an _italic word_ and _another_",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with an ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.ITALIC)]
            )
                

    def test_markdown_delimiter_italic_asterisk_multiple(self):
        node = TextNode("This is a text with an *italic word* and *another*",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with an ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.ITALIC)]
            )


    def test_markdown_delimiter_code(self):
        node = TextNode("This is a text with a `code block` word",
                        TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)]
            )
        

    def test_invalid_Markdown(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a text with a `missing delimiter",
                            TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, 
                    "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )


class TestExtractMarkdownLinksAndImages(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")],
                              matches)
        

    def test_extract_images_extra_characters_excluded(self):
        matches = extract_markdown_images(
            "This is a text with an ![[image] (https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")],
                             matches)


    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), 
                              ("to youtube", 
                               "https://www.youtube.com/@bootdotdev")],
                                matches)


    def test_extract_links_extra_characters_excluded(self):
        matches = extract_markdown_links(
            "This is a text with a link [[to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")],
                             matches)


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, 
                         "https://www.youtube.com/@bootdotdev"
                         )
            ],
            new_nodes
        )


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
        "and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, 
                     "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, 
                "https://i.imgur.com/3elNhQu.png"
                    )
            ],
            new_nodes
        )


    def test_split_images_multiple_nodes(self):
        node = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
                "and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT), 
            TextNode(
                "This is a second textnode with an ![image](https://www.example.com)", 
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, 
                         "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is a second textnode with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.example.com")

            ],
            new_nodes
        )       


    def test_split_links_multiple_nodes(self):
        node = [
            TextNode(
                "This is text with a link [to boot dev](https://www.bootdev.com) "
                "and another link [to youtube](https://www.youtube.com)",
                TextType.TEXT), 
            TextNode(
                "This is a second textnode with a link [Example](https://www.example.com)", 
                TextType.TEXT)
        ]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.bootdev.com"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, 
                         "https://www.youtube.com"),
                TextNode("This is a second textnode with a link ", TextType.TEXT),
                TextNode("Example", TextType.LINK, "https://www.example.com")

            ],
            new_nodes
        )       


    def test_split_nodes_link_empty_text(self):
        node = TextNode(
            "[to boot dev](https://www.bootdev.com)!",
                     TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.bootdev.com"),
                TextNode("!", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_nodes_image_empty_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)!",
                     TextType.TEXT)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("!", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_nodes_link_NoLink(self):
        node = TextNode("This is a text without a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text without a link", TextType.TEXT)
            ],
            new_nodes
        )


    def test_split_nodes_link_NoImage(self):
        node = TextNode("This is a text without an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text without an image", TextType.TEXT)
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()