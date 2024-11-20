from textnode import TextType, TextNode
import re

def text_to_textnodes(text):
    nodes =  [TextNode(text, TextType.TEXT)]
    nodes =  split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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



def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if extract_markdown_images(node.text) == []:
            new_nodes.append(node)
            continue
        else:
            images = extract_markdown_images(node.text)
            remaining_text = ""
            for i in range(len(images)):
                image_alt = images[i][0]
                image_link = images[i][1]
                if remaining_text == "":
                    sections = node.text.split(f"![{image_alt}]({image_link})", 2)
                else:
                    sections = remaining_text.split(f"![{image_alt}]({image_link})", 2)
                if sections[0] != "" and extract_markdown_images(sections[0]) == []:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
            continue
        else:
            images = extract_markdown_links(node.text)
            remaining_text = ""
            for i in range(len(images)):
                link_alt = images[i][0]
                link_url = images[i][1]
                if remaining_text == "":
                    sections = node.text.split(f"[{link_alt}]({link_url})", 2)
                else:
                    sections = remaining_text.split(f"[{link_alt}]({link_url})", 2)
                if sections[0] != "" and extract_markdown_links(sections[0]) == []:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes



