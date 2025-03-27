import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

        node1 = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node1.props_to_html(), "")

        node2 = HTMLNode("h1", "Titel", None, None)
        self.assertEqual(node2.props_to_html(), "")

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node1 = LeafNode("a", "click me", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node1.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    

if __name__ == "__main__":
    unittest.main()