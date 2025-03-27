import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.Italic)
        node4 = TextNode("This is a text node", TextType.Normal)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a text NODE", TextType.Normal)
        node6 = TextNode("This is a text node", TextType.Normal)
        self.assertNotEqual(node5, node6)
        node7 = TextNode("This is a text NODE", TextType.Normal, "https://www.boot.dev")
        node8 = TextNode("This is a text NODE", TextType.Normal)
        self.assertNotEqual(node7, node8)
if __name__ == "__main__":
    unittest.main()