import unittest
from transformers import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import *

class Test_transformer(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes(self):
        input_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)

        self.assertEqual(result, expected_output)


        input_node1 = TextNode("This **bold** word", TextType.TEXT)
        
        expected_output1 = [
            TextNode("This ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        
        result1 = split_nodes_delimiter([input_node1], "**", TextType.BOLD)

        self.assertEqual(result1, expected_output1)


        input_node2 = TextNode("This is text with a `code block` and a **bold** word", TextType.TEXT)
        
        expected_output2 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        
        result2 = split_nodes_delimiter([input_node2], "`", TextType.CODE)
        result2 = split_nodes_delimiter(result2, "**", TextType.BOLD)

        self.assertEqual(result2, expected_output2)

if __name__ == "__main__":
    unittest.main()