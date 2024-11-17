
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        str = ""
        if self.props != None:
            for prop in self.props:
                str += f' {prop}="{self.props[prop]}"'
        return str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
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
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(self)
        self.tag = tag
        self.children = children
        self.props = props
        
    ## recursive for practice    
    def to_html(self, num=0, str=""):

        if self.tag is None:
            raise ValueError ("there shall be tag")
        elif self.children is None:
            raise ValueError ("ParentNode must have children")
        prop_string = ""
        if self.props is not None:
            for prop in self.props:
                prop_string += f' {prop}="{self.props[prop]}"'

        child = self.children[num]
        str = str+child.to_html()
        if num+1 >= len(self.children):
            return f"<{self.tag}{prop_string}>{str}</{self.tag}>"
        else:
            return self.to_html(num+1, str)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"