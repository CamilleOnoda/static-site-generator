from enum import Enum

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_textnodes(text):
    """
    Converts a raw string of markdown-flavored text 
    into a list of TextNode objects.
    """
    initial_TextNode = TextNode(text, TextType.TEXT)
    new_TextNode = split_nodes_delimiter([initial_TextNode], "**", TextType.BOLD)
    new_TextNode = split_nodes_delimiter(new_TextNode, "_", TextType.ITALIC)
    new_TextNode = split_nodes_delimiter(new_TextNode, "`", TextType.CODE)

    for node in new_TextNode:
        if "![" in node.text:
            new_TextNode = split_nodes_image(new_TextNode)

        else:
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
    """
    Takes raw markdown text and returns a list of tuples. 
    
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
    """
    Extracts markdown images. 
    Return a list of tuples of anchor text and URLs.
    """

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
    """
    Split raw markdown text into TextNodes based on links
    """
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
    """
    Split raw markdown text into TextNodes based on images
    """
    final_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            final_nodes.append(old_node)
            continue
#        if not re.search(r"!\[.*?\]\s*\(.*?\)", old_node.text):

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
    """
    Takes a raw Markdown string (representing a full document) as input
     
    and returns a list of "block" strings.
    """
    
    split_markdown = markdown.split("\n\n")
    blocks = [block.strip() for block in split_markdown if block != ""]
    return blocks
    

def block_to_block_type(block):
    """
    Takes a single block of markdown text as input 
    
    and returns the BlockType representing the type of block it is.
    """

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


def text_to_children(text):
    """
    Creates a list of children based on the inline markdown syntax
    """
    new_text_nodes = text_to_textnodes(text)
    list_children = []
    for node in new_text_nodes:
        new_child = text_node_to_html_node(node)
        list_children.append(new_child)
    return list_children


def get_heading_html(heading):
    if heading.startswith("# "):
        return "h1"
    elif heading.startswith("## "):
        return "h2"
    elif heading.startswith("### "):
        return "h3"
    elif heading.startswith("#### "):
        return "h4"
    elif heading.startswith("##### "):
        return "h5"
    elif heading.startswith("###### "):
        return "h6"


def get_content(blockType, block):
    """
    Extracts the content of a block based on the block type
    """
    if blockType == BlockType.PARAGRAPH:
        return block.replace("\n", " ")
    elif blockType == BlockType.HEADING:
        return re.findall(r"^#{1,6} +(.+)", block, re.MULTILINE)
    elif blockType == BlockType.CODE:
        content = re.findall(r"^```(.*?)```$", block, re.DOTALL)
        raw_content = content[0]
        return raw_content.lstrip()
    elif blockType == BlockType.QUOTE:
        return re.findall(r"^> (.*)", block, re.MULTILINE)
    elif blockType == BlockType.UNORDERED_LIST:
        return re.findall(r"^- (.*)", block, re.MULTILINE)
    elif blockType == BlockType.ORDERED_LIST:
        return re.findall(r"^[0-9]+\. (.+)", block, re.MULTILINE)


def block_to_ParentNode(blockType, block):
    """
    Takes a block of markdown and its block type, 
    extracts the content and returns a ParentNode
    """

    if blockType == BlockType.PARAGRAPH:
        text = get_content(blockType, block)
        children = text_to_children(text)
        return ParentNode("p", children)
    
    elif blockType == BlockType.HEADING:
        new_block = [block]
        children_list = [] 
        for element in new_block:
            headings = element.split("\n")
        for heading in headings:
            tag = get_heading_html(heading)
            heading_text = get_content(blockType, heading)
            child = text_to_children(heading_text[0])
            child[0].tag = tag
            children_list.append(child[0])
        return children_list
    
    elif blockType == BlockType.CODE:
        children_list = []
        cleaned_text = get_content(blockType, block)
        node = TextNode(cleaned_text, TextType.CODE)
        children = text_node_to_html_node(node)
        children_list.append(children)
        return ParentNode("pre", children_list)
    
    elif blockType == BlockType.QUOTE:
        content = get_content(blockType, block)
        for i in range(len(content) - 1):
            content[i] = content[i] + " "
        children_list = []
        for element in content:
            nodes = text_to_children(element)
            for node in nodes:
                children_list.append(node)
        return ParentNode("blockquote", children_list)
    
    elif blockType == BlockType.UNORDERED_LIST:
        content = get_content(blockType, block)
        children_list = []
        for item in content:
            child = text_to_children(item)
            nested_parent = ParentNode("li", child)
            children_list.append(nested_parent)
        return ParentNode("ul", children_list)
    
    elif blockType == BlockType.ORDERED_LIST:
        content = get_content(blockType, block)
        children_list = []
        for item in content:
            child = text_to_children(item)
            nested_parent = ParentNode("li", child)
            children_list.append(nested_parent)
        return ParentNode("ol", children_list)

        
def markdown_to_html_node(markdown):
    """ 
    Converts a full markdown document into a single parent HTMLNode
    """
    blocks_markdown = markdown_to_blocks(markdown)
    children_list = []
    for block in blocks_markdown:
        if block != "":
            block_type = block_to_block_type(block) 
            parent = block_to_ParentNode(block_type, block)
            if isinstance(parent, list):
                children_list.extend(parent)
            else:
                children_list.append(parent)
    return ParentNode("div", children_list)

