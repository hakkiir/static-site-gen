import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, extract_markdown_links, extract_markdown_images


class TestSplitNode(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE),
                         [TextNode('This is text with a ', 'text', None), 
                          TextNode('code block', 'code', None), 
                          TextNode(' word', 'text', None)])
        
    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                         [TextNode('This is text with a ', 'text', None), 
                          TextNode('bold block', 'bold', None), 
                          TextNode(' word', 'text', None)])
        
    def test_split_node_italic(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC),
                         [TextNode('This is text with a ', 'text', None), 
                          TextNode('italic block', 'italic', None), 
                          TextNode(' word', 'text', None)])
        
    def test_split_node_multiple_nodes(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        node2 = TextNode("This is text with a *itaalian block* word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2], "*", TextType.ITALIC),
                         [TextNode('This is text with a ', 'text', None), 
                          TextNode('italic block', 'italic', None), 
                          TextNode(' word', 'text', None),
                          TextNode('This is text with a ', 'text', None), 
                          TextNode('itaalian block', 'italic', None), 
                          TextNode(' word', 'text', None)
                          ],)


    def test_split_node_wrong_syntax(self):
        node = TextNode("This is text with a **bold block* word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_output = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        link = extract_markdown_links(text)
        self.assertEqual(link, expected_output)
    
    def test_extract_one_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected_output = [("to boot dev", "https://www.boot.dev")]
        link = extract_markdown_links(text)
        self.assertEqual(link, expected_output)
    
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        link = extract_markdown_images(text)
        self.assertEqual(link, expected_output)
    
    def test_extract_one_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and"
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        link = extract_markdown_images(text)
        self.assertEqual(link, expected_output)

    def test_extract_one_links(self):
        text = "This is text with a image ![to boot dev](https://www.boot.dev)"
        expected_output = []
        link = extract_markdown_links(text)
        self.assertEqual(link, expected_output)

    def test_extract_images_wrong_syntax(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) link"
        expected_output = []
        link = extract_markdown_images(text)
        self.assertEqual(link, expected_output)
if __name__ == "__main__":
    unittest.main()
