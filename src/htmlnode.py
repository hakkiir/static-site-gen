
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
        super().__init__(tag, value, None, props)

    def to_html(self):
        print(self.__repr__)
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    '''    
    def to_html(self, num=0, str=""):

        if self.tag is None:
            raise ValueError ("there shall be tag")
        elif self.children is None:
            raise ValueError ("ParentNode must have children")
        prop_string = ""
        if self.props is not None:
            for prop in self.props:
                prop_string += f' {prop}="{self.props[prop]}"'
        print(num)
        child = self.children[num]
        str = str+child.to_html()
        if num+1 >= len(self.children):
            return f"<{self.tag}{prop_string}>{str}</{self.tag}>"
        else:
            return self.to_html(num+1, str)'''
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"