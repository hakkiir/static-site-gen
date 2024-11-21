from htmlnode import *
from textnode import *
from parse_inline_text import *
from parse_blocks import *


# converts a full markdown document into a single HTMLNode.
# single HTMLNode should contain many child HTMLNode objects representing the nested elements.

# Split the markdown into blocks
# Loop over each block:
#   Determine the type of block (you already have a function for this)
#   Based on the type of block, create a new HTMLNode with the proper data
#   Assign the proper child HTMLNode objects to the block node. 
#       I created a shared text_to_children(text) function that works for all block types. 
#       It takes a string of text and returns a list of HTMLNodes
#        that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
# 
# Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.


#  Quote blocks should be surrounded by a <blockquote> tag.
#  Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
#  Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
#  Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
#  Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
#  Paragraphs should be surrounded by a <p> tag.

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in md_blocks:
        html_nodes.append(block_to_html_node(block))
    grandparent = ParentNode("div", html_nodes)
    return grandparent


def block_to_html_node(block):

    block_type = block_to_block_type(block)

    if block_type == block_type_paragraph:
        return text_to_html(block)
    elif block_type == block_type_heading:
        return heading_to_html(block)
    elif block_type == block_type_code:
            return code_to_html(block)
    elif block_type == block_type_quote:
        return quote_to_html(block)
    elif block_type == block_type_olist:
        return olist_to_html(block)
    elif block_type == block_type_ulist:
        return ulist_to_html(block)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def text_to_html(block):
    text = block.split("\n")
    p = " ".join(text)
    child = text_to_children(p)
    parent = ParentNode("p", child)
    return parent

def heading_to_html(block):
    count = 0
    for i in range(len(block)):
        if block[i] == '#':
            count += 1
        if block[i] != '#' or count == 6:
            break
    text = block[i + 1:]
    child = text_to_children(text)
    parent = ParentNode(f"h{i}", child)
    return parent

def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid codeblock syntax")
    text = block[4:-3]
    child = text_to_children(text)
    code = ParentNode("code", child)
    return ParentNode("pre", [code])

def quote_to_html(block):
    text = block.split("\n")
    lines = []
    for line in text:
        if not line.startswith(">"):
            raise ValueError("invalid quote syntax")
        else:
            lines.append(line.lstrip(">").strip())
    text = " ".join(lines)
    child = text_to_children(text)
    return ParentNode("blockquote", child)

def olist_to_html(block):
    lines = block.split("\n")
    li_parents = []
    for item in lines:
        text = item[3:]
        li_parents.append(ParentNode("li",text_to_children(text)))
    return ParentNode("ol", li_parents)

def ulist_to_html(block):
    lines = block.split("\n")
    li_parents = []
    for item in lines:
        text = item[2:]
        li_parents.append(ParentNode("li",text_to_children(text)))
    return ParentNode("ul", li_parents)