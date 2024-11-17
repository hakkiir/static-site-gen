from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    test_node = TextNode("testi teksti", 'bold', "https://www.boot.dev")

    print(test_node)

if __name__ == "__main__":
    main()


def text_node_to_html_node(text_node):

    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(None, text_node.text)  
        case(TextType.BOLD):
            return LeafNode("b", text_node.text)
        case(TextType.ITALIC):
            return LeafNode("i", text_node.text)
        case(TextType.CODE):
            return LeafNode("code", text_node.text)
        case(TextType.LINK):
            return LeafNode("a", text_node.text, {"href" : {text_node.url}})
        case(TextType.IMAGE):
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node})
        case _:
            raise ValueError ("Invalid text type")