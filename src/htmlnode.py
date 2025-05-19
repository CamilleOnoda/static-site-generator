class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        """Return a string that represents the HTML attributes of the node.
        
        If self.props:
        
        {
            "href": "website link",
            "target": "_blank",
        }
        
        Then self.props_to_html() should return:
         href="website link" target="_blank"

        Notice the leading space character before href and before target.
        """

        string_attributes = ""
        for key, value in self.props.items():
            string_attributes += f" {key}" + "=" + f'"{value}"'
        return string_attributes
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("The LeafNode subclass requires a value.")
        super().__init__(tag=tag, value=value, props=props, children=[])

    def add_child(self,child):
        raise Exception("LeafNode can not have children!")
    
    def add_children(self,children):
        raise Exception("LeafNode can not have children!")
        
       

        
