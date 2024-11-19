import unittest
from textnode import TextNode, TextType
from parse_inline_md import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link


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


    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,[
                           TextNode("This is text with a link ", TextType.TEXT),
                           TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                           TextNode(" and ", TextType.TEXT),
                           TextNode( "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                           ])

    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with a image ![to boot dev](https://www.boot.dev) and another image ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,[
                        TextNode("This is text with a image ", TextType.TEXT),
                        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                        TextNode(" and another image ", TextType.TEXT),
                        TextNode( "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
                        ])
    

    def test_split_nodes_link2(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        node2 = TextNode(
        "This is text with no link and image ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)

        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(new_nodes,[
                           TextNode("This is text with a link ", TextType.TEXT),
                           TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                           TextNode(" and ", TextType.TEXT),
                           TextNode( "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                           
                           TextNode("This is text with no link and image ![to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT,)],
                           )
    def test_split_nodes_image2(self):
        node = TextNode(
        "This is text with a img ![to boot dev](https://www.boot.dev)![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        node2 = TextNode(
        "This is text with link [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)

        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(new_nodes,[
                           TextNode("This is text with a img ", TextType.TEXT),
                           TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                           TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
                           TextNode("This is text with link [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT,)],
                           )
        
    def test_split_nodes_image3(self):
        node = TextNode("",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,[
                           TextNode("", TextType.TEXT),],
                            )


##bootdev test

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()