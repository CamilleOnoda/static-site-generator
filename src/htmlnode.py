class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Ensure all subclasses implement their own to_html()
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        """Returns a string that represents the HTML attributes of the node."""
        if self.props is None:
            return ""       
        string_attributes = ""
        for key, value in self.props.items():
            string_attributes += f" {key}" + "=" + f'"{value}"'
        return string_attributes
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("The LeafNode subclass requires a value.")
        super().__init__(tag=tag, value=value, props=props, children=[])

    def add_child(self, child):
        raise Exception("LeafNode can not have children!")
    
    def add_children(self, children):
        raise Exception("LeafNode can not have children!")
    
    def to_html(self):
        """Returns a leaf node as an html string"""
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        """ Returns a string representing the HTML tag of the node and its children."""
        if self.tag is None:
            raise ValueError("The ParentNode subclass requires a tag.")
        if self.children is None:
            raise ValueError("The ParentNode subclass must have children.")

        concat_str = ""       
        for child in self.children:
            concat_str += child.to_html()
        if self.props:
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{concat_str}</{self.tag}>'
        return f'<{self.tag}>{concat_str}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode({self.tag}, children: {self.children}, {self.props})'

        
       

        
