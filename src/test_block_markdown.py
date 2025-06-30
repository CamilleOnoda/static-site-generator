import unittest
from inline_markdown import (BlockType,
                             markdown_to_blocks,
                             block_to_block_type,
                             markdown_to_html_node)





class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_type_Paragraph(self):
        block = "This is **bolded** paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_block_to_block_type_Heading(self):
        block = "## I am a title"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)


    def test_block_to_block_type_Code(self):
        block = "```I am a code block\n and another code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)


    def test_block_to_block_type_UnorderedList(self):
        block = "- First item\n - Second item\n - Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)


    def test_block_to_block_type_OrderedList(self):
        block = "1. First item\n 2. Second item\n 3. Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_markdown_to_html_node_orderedList(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )


    def test_markdown_to_html_node_unorderedList(self):
        md = """
- First item
- Second item
- Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )


    def test_markdown_to_html_node_quote(self):
        md = """
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Dorothy followed her through many of the beautiful rooms in her castle. The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</blockquote></div>"
        )


    def test_markdown_to_html_node_heading(self):
        md = """
# Heading **level** 1

## Heading level 2

### Heading level 3

#### Heading level 4

##### Heading level 5

###### Heading level 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading <b>level</b> 1</h1><h2>Heading level 2</h2><h3>Heading level 3</h3><h4>Heading level 4</h4><h5>Heading level 5</h5><h6>Heading level 6</h6></div>"
        )


    def test_markdown_to_html_node_multipleBlocks(self):
        md = """
I am a paragraph with an **important word** and a [link](https://www.example.com)!

# I am a level 1 heading

```
Here is some code and
a _word_ in italic
```

1. First item
2. Second item
3. Third item

> I am a quote.
>
> I am another quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>I am a paragraph with an <b>important word</b> and a <a href="https://www.example.com">link</a>!</p><h1>I am a level 1 heading</h1><pre><code>Here is some code and\na _word_ in italic\n</code></pre><ol><li>First item</li><li>Second item</li><li>Third item</li></ol><blockquote>I am a quote. I am another quote.</blockquote></div>'
            )


    def test_markdown_to_html_empty(self):
        md = """

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>"
        )