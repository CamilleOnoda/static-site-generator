from tracemalloc import start
from numpy import extract
from textnode import TextNode, TextType
import re


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


def text_to_textnodes(text):
    """Convert a raw string of markdown-flavored text 
    into a list of TextNode objects."""
    # Split by bold text
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "__", TextType.BOLD)

    # Split by italic text
    text = split_nodes_delimiter(text, "_", TextType.ITALIC)
    text = split_nodes_delimiter(text, "*", TextType.ITALIC)

    # Split by code block
    text = split_nodes_delimiter(text, "`", TextType.CODE)

    # Split by image
    text = split_nodes_image(text)

    # Split by link
    text = split_nodes_link(text)


    return text
