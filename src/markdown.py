from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    It takes a list of "old nodes", a delimiter, and a text type. 
    It should return a new list of nodes, where any "text" type nodes 
    in the input list are (potentially) split into multiple nodes 
    based on the syntax. 

    --For example:
    
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    --new_nodes becomes:
    
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_old_node = (old_node.text).split(delimiter)
            if len(split_old_node) % 2 == 0:
                raise Exception(
                    "Invalid Markdown syntax: " \
                    "check the opening and closing delimiters"
                    )
            else:
                for idx in range(len(split_old_node)):
                    if split_old_node[idx] == "":
                        continue
                    if idx % 2 == 0:
                        new_nodes.append(TextNode(split_old_node[idx], 
                                                  TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_old_node[idx], 
                                                  text_type))

    return new_nodes

