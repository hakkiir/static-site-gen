from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        nodes_to_extend = []
        strings = node.text.split(delimeter)
        if len(strings) % 2 == 0:
            raise ValueError ("Invalid MD syntax, section not closed")
        for i in range(len(strings)):
            if strings[i] == "":
                continue
            if i % 2 == 0:
                nodes_to_extend.append(TextNode(strings[i], TextType.TEXT))
            else:
                nodes_to_extend.append(TextNode(strings[i], text_type))
        new_nodes.extend(nodes_to_extend)
    return new_nodes



def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 
    return matches
