import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    ##  LeafNodes

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


    ##  ParentNodes

    def test_parent_node_repr(self):
        lnode1 = LeafNode("p", "Hello, world!")
        lnode2 = LeafNode(None, "Hello again, world!")
        parent = ParentNode("h1", [lnode1, lnode2], {"class": "primary"})

        self.assertEqual(
            parent.__repr__(),
            "ParentNode(h1, children: [LeafNode(p, Hello, world!, None), LeafNode(None, Hello again, world!, None)], {'class': 'primary'})"
        )

    def test_parent_tohtml_no_child(self):
        parent = ParentNode('p', None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_tohtml_with_child_no_props(self):
        lnode1 = LeafNode("p", "Hello, world!")
        lnode2 = LeafNode(None, "Hello again, world!")
        parent = ParentNode("h1", [lnode1, lnode2])

        self.assertEqual(parent.to_html(), f"<h1>{lnode1.to_html()}{lnode2.to_html()}</h1>")

    def test_parent_with_nested_parent(self):
        lnode1 = LeafNode("p", "Hello, world!")
        lnode2 = LeafNode(None, "Hello again, world!")
        parent = ParentNode("h2", [lnode1, lnode2])

        parent2 = ParentNode('p', [parent, lnode1, lnode2], {"class": "primary", "color" : "red"})
        self.assertEqual(parent2.to_html(),'<p class="primary" color="red"><h2><p>Hello, world!</p>Hello again, world!</h2><p>Hello, world!</p>Hello again, world!</p>')

    ### bootdev solution tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



if __name__ == "__main__":
    unittest.main()
