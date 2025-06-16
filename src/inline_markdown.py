from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_textnodes(text):
    """Convert a raw string of markdown-flavored text 
    into a list of TextNode objects."""
    
    initial_TextNode = TextNode(text, TextType.TEXT)
    new_TextNode = split_nodes_delimiter([initial_TextNode], "**", TextType.BOLD)
    new_TextNode = split_nodes_delimiter(new_TextNode, "__", TextType.BOLD)

    new_TextNode = split_nodes_delimiter(new_TextNode, "_", TextType.ITALIC)
    new_TextNode = split_nodes_delimiter(new_TextNode, "*", TextType.ITALIC)

    new_TextNode = split_nodes_delimiter(new_TextNode, "`", TextType.CODE)

    new_TextNode = split_nodes_image(new_TextNode)

    new_TextNode = split_nodes_link(new_TextNode)

    return new_TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    It takes a list of "old nodes", a delimiter, and a text type. 
    It should return a new list of nodes, where any "text" type nodes 
    in the input list are (potentially) split into multiple nodes 
    based on the syntax. 
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = (old_node.text).split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError(
                    "Invalid Markdown syntax: " \
                    "check the opening and closing delimiters"
                    )
            else:
                for idx in range(len(sections)):
                    if sections[idx] == "":
                        continue
                    if idx % 2 == 0:
                        new_nodes.append(TextNode(sections[idx], 
                                                  TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(sections[idx], 
                                                  text_type))

    return new_nodes


def extract_markdown_images(text):
    """Takes raw markdown text and returns a list of tuples. 
    
    Each tuple should contain the alt text and the URL of any markdown images.
    
    """

    # Check for invalid markdown syntax
    # Case with "](" without opening "["
    if "](" in text and not re.search(r"!\[.*?\]\(", text):
        raise ValueError("Invalid Markdown image syntax")
    
    # Case with opening "[" without "]("
    if "![" in text and not re.search(r"!\[.*?\]\s*\(.*?\)", text):
        raise ValueError("Invalid Markdown image syntax")
    
    pattern = r"!\[.*?([^\[\]]*)\].*?\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """Extracts markdown images. 
    Return a list of tuples of anchor text and URLs."""

    # Check for invalid markdown syntax
    # Case with "](" without opening "["
    if "](" in text and not re.search(r"\[.*?\]\(", text):
        raise ValueError("Invalid Markdown link syntax")
    
    # Case with opening "[" without "]("
    if "[" in text and not re.search(r"\[.*?\]\s*\(.*?\)", text):
        raise ValueError("Invalid Markdown link syntax") 

    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_link(old_nodes):
    """Split raw markdown text into TextNodes based on links"""
    final_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            final_nodes.append(old_node)
            continue
        new_nodes = []
        extracted_links = extract_markdown_links(old_node.text)
        if not extracted_links:
            final_nodes.append(old_node)
            continue

        current_text = old_node.text
        for link in extracted_links:
            sections = current_text.split(f"[{link[0]}]({link[1]})")
            before_link = TextNode(sections[0], TextType.TEXT)
            new_link = TextNode(link[0], TextType.LINK, link[1])
            if before_link.text != "":
                new_nodes.append(before_link)
            new_nodes.append(new_link)
            current_text = sections[1]

        if current_text != "":
            current_text = TextNode(current_text, TextType.TEXT)
            new_nodes.append(current_text)

        final_nodes.extend(new_nodes)

    return final_nodes


def split_nodes_image(old_nodes):
    """Split raw markdown text into TextNodes based on images"""
    final_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            final_nodes.append(old_node)
            continue
        new_nodes = []
        extracted_images = extract_markdown_images(old_node.text)
        if not extracted_images:
            final_nodes.append(old_node)
            continue

        current_text = old_node.text
        for image in extracted_images:
            sections = current_text.split(f"![{image[0]}]({image[1]})")
            before_image = TextNode(sections[0], TextType.TEXT)
            new_image = TextNode(image[0], TextType.IMAGE, image[1])
            if before_image.text != "":
                new_nodes.append(before_image)
            new_nodes.append(new_image)
            current_text = sections[1]

        if current_text != "":
            current_text = TextNode(current_text, TextType.TEXT)
            new_nodes.append(current_text)

        final_nodes.extend(new_nodes)

    return final_nodes


def markdown_to_blocks(markdown):
    """Takes a raw Markdown string (representing a full document) as input
     
       and returns a list of "block" strings."""
    
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if "\t" in block:
            raise ValueError("Newlines can't be indented")
    if len(split_markdown) == 1:
        raise ValueError(
            "Invalid Markdown input. Each section is separated by a double newline"
            )
    blocks = [block.strip() for block in split_markdown if block != ""]
    return blocks
    

def block_to_block_type(block):
    """Takes a single block of markdown text as input 
    
    and returns the BlockType representing the type of block it is."""

    if re.findall(r"^#{1,6} \S.+", block, re.MULTILINE):
        return BlockType.HEADING
    elif re.findall(r"^```.*?```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.findall(r"^> ?.*", block, re.MULTILINE):
        return BlockType.QUOTE
    elif re.findall(r"^- .+", block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.findall(r"^[0-9]+\. .+", block, re.MULTILINE):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def get_heading_count(block):
    if block.count("#") == 1:
        return HTMLNode("H1",block)
    if block.count("#") == 2:
        return HTMLNode("H2",block)
    if block.count("#") == 3:
        return HTMLNode("H3",block)
    if block.count("#") == 4:
        return HTMLNode("H4",block)
    if block.count("#") == 5:
        return HTMLNode("H5",block)
    if block.count("#") == 6:
        return HTMLNode("H6",block)


def block_to_HTMLNode(blockType, block):
    if blockType == BlockType.PARAGRAPH:
        return HTMLNode("p", block)
    elif blockType == BlockType.HEADING:
        return get_heading_count(block)
    elif blockType == BlockType.CODE:
        return HTMLNode("pre", block)
    elif blockType == BlockType.QUOTE:
        return HTMLNode("blockquote", block)
    elif blockType == BlockType.UNORDERED_LIST:
        return HTMLNode("ul", None, block)
    elif blockType == BlockType.ORDERED_LIST:
        return HTMLNode("ol", None, block)


def text_to_children(text):
    # Break down the text into a list of TextNodes based on inline markdown.
    new_text_nodes = text_to_textnodes(text)
    for node in new_text_nodes:
        pass
    return new_text_nodes


def markdown_to_html_node(markdown):
    blocks_markdown = markdown_to_blocks(markdown)
    for block in blocks_markdown:
        block_type = block_to_block_type(block)
        block_node = block_to_HTMLNode(block_type, block)
        block_to_TextNode = text_to_children(block_node.value)
    


md = """
This is **bold** and _italic_

## This is a title
"""
print(markdown_to_html_node(md))