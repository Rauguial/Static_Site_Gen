import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a text NODE", TextType.TEXT)
        node6 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node5, node6)
        node7 = TextNode("This is a text NODE", TextType.TEXT, "https://www.boot.dev")
        node8 = TextNode("This is a text NODE", TextType.TEXT)
        self.assertNotEqual(node7, node8)
if __name__ == "__main__":
    unittest.main()