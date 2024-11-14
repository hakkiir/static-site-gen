import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_is_instance(self):
        node = TextNode("testing", TextType.NORMAL, "https://www.urlit-tulille.com")
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
        node2 = TextNode("testing", TextType.NORMAL, "https://www.urlit-tulille.com")
        self.assertIsNot(node, node2)

if __name__ == "__main__":
    unittest.main()
