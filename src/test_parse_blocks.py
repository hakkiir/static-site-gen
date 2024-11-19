import unittest
from parse_blocks import (
    markdown_to_blocks, 
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)

class TestParseBlocks(unittest.TestCase):

    def test_parse_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item """
        self.assertEqual(markdown_to_blocks(md),
                         ['# This is a heading','This is a paragraph of text. It has some **bold** and *italic* words inside of it.','* This is the first list item in a list block\n* This is a list item\n* This is another list item']
                         )

    def test_parse_blocks2(self):
        md = """
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item 


# another heading
"""


        self.assertEqual(markdown_to_blocks(md),
                         ['# This is a heading','This is a paragraph of text. It has some **bold** and *italic* words inside of it.','* This is the first list item in a list block\n* This is a list item\n* This is another list item','# another heading']
                         )
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_block_to_type(self):

        block1 = "* This is a list\n* with items"
        block2 = "This is **bolded** paragraph"
        block3 = "This is another paragraph with *italic* text and `code` here"
        block4 = "# This is a heading"
        block5 = "```this is code```"
        block6 = "1. This is ordered list\n2. with items\n3. and more items"


        self.assertEqual(block_to_block_type(block1),
                         block_type_ulist)
        self.assertEqual(block_to_block_type(block2),
                         block_type_paragraph)
        self.assertEqual(block_to_block_type(block3),
                         block_type_paragraph)
        self.assertEqual(block_to_block_type(block4),
                         block_type_heading)
        self.assertEqual(block_to_block_type(block5),
                         block_type_code)
        self.assertEqual(block_to_block_type(block6),
                         block_type_olist)
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

if __name__ == "__main__":
    unittest.main()