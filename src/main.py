from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    test_node = TextNode("testi teksti", 'bold', "https://www.boot.dev")

    print(test_node)

if __name__ == "__main__":
    main()


