import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_is_instance(self):
        node = TextNode("testing", TextType.TEXT, "https://www.urlit-tulille.com")
        self.assertIsInstance(node, TextNode)

    def test_eq2(self):
        node = TextNode("This is a text node aaaa!!!!", TextType.ITALIC, "https://www.urlit-tulille.com")
        node2 = TextNode("This is a text node aaaa!!!!", TextType.ITALIC, "https://www.urlit-tulille.com") 
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("1234", TextType.ITALIC, "https://www.tulille.com")
        node2 = TextNode("1234", TextType.ITALIC, "https://www.tulille.com") 
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("12345", TextType.ITALIC, None)
        node2 = TextNode("12345", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a text node aaaa!!!!", TextType.ITALIC, "https://www.urlit-tulille.com")
        node2 = TextNode("testing", TextType.TEXT, "https://www.urlit-tulille.com")
        self.assertIsNot(node, node2)


    def test_text_node_to_leaf(self):
        node = TextNode("12345", TextType.ITALIC, None)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    ##bootdev tests:
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()
