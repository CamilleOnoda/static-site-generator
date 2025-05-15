

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
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
