
class HTMLNode():
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str = ""
        if self.props != None:
            for prop in self.props:
                str += f' {prop}="{self.props[prop]}"'
        return str
    
    def __repr__(self):
        return f"HTMLNode{self.tag,self.value,self.children,self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(self)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == "" or self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        prop_string = ""
        if self.props != None:
            for prop in self.props:
                prop_string += f' {prop}="{self.props[prop]}"'
        
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
    
