class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Act as a safeguard, ensuring all subclasses implement their own to_html()
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

    def add_child(self,child):
        raise Exception("LeafNode can not have children!")
    
    def add_children(self,children):
        raise Exception("LeafNode can not have children!")
    
    def to_html(self):
        """Returns a leaf node as an html string"""
        if self.tag is None:
            return self.value
        if self.props:
            props_string = self.props_to_html()
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
        
       

        
