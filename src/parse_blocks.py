import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    splitted_md = markdown.split("\n\n")
    return_list = []
    for str in splitted_md:
        if str != "":
            return_list.append(str.strip())
    return return_list

## used regex before figured out about .startswith()
def block_to_block_type(block):
    if re.match(r"(^#{1,6} )", block[0:5]):
        return block_type_heading
    if block[0:3] == "```" and block[-3:] == "```":
        return block_type_code
    quotes = 0
    unlist = 0
    orlist = 0
    split_block = block.split("\n")
    for i in range(len(split_block)):
        if split_block[i][0] == ">":
            quotes += 1
            if quotes == len(split_block):
                return block_type_quote
        elif split_block[i][0:2] == "* " or split_block[i][0:12] == "- ":
            unlist += 1
            if unlist == len(split_block):
                return block_type_ulist
        elif re.match(r"(^\d{1,6}. )",split_block[i]):
            orlist += 1
            if orlist == len(split_block):
                return block_type_olist
        else:
            return block_type_paragraph
    return block_type_paragraph