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
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    """Extracts markdown links.
    It should return tuples of anchor text and URLs."""
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

