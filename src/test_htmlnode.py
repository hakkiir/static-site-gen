import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
        
        def test_not_eq(self):
            node = HTMLNode("p", "lorem ipsum dolor sit amet",None, {"href": "https://wwww.google.com","target" : "_blank"})
            node2 = HTMLNode("p", "aaaa vvvv ssss rr amewat",node, {"href": "https://wwww.yahoo.com","target" : "_blank"})
            self.assertNotEqual(node, node2)

        def test_HTMLNode_repr(self):
            node = HTMLNode("p", "lorem ipsum dolor sit amet",None, {"href": "https://wwww.google.com","target" : "_blank"})
            node2 = HTMLNode("p", "aaaa vvvv ssss rr amewat",node, {"href": "https://wwww.yahoo.com","target" : "_blank"})
            print("repr:")
            print(node.__repr__)
            print()
            print("node2 repr:")
            print(node2.__repr__)
            self.assertIsInstance(node, HTMLNode)
            self.assertIsInstance(node2, HTMLNode)

        def test_props_to_html(self):
            node = HTMLNode("p", "lorem ipsum dolor sit amet",None, {"href": "https://wwww.google.com","target" : "_blank"})
            print("props_to_html")
            print(node.props_to_html())

        
        def test_LeafNode(self):
            l1 = LeafNode("p", "This is a paragraph of text.")
            l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            
            print(l1.__repr__)
            print()
            print(l2.__repr__)
            print()
            print("To_html:")
            print(l1.to_html())
            print()
            print(l2.to_html())
        
        
if __name__ == "__main__":

    unittest.main()
