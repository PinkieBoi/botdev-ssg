import unittest
from htmlnode import HTMLNode, LeafNode


class TestHtmlNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode('p', 'This is a line of text')
        node2 = HTMLNode('p', 'This is a line of text', None, None)
        self.assertEqual(print(node), print(node2))

    def test_props_to_html(self):
        node5 = HTMLNode('a', 'link', props='href="https://www.google.com" target="_blank"')
        node5_html_props = {'href': '"https://www.google.com"', 'target': '"_blank"'}
        self.assertEqual(node5.props, node5_html_props)

    def test_to_heml(self):
        node6 = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node6.to_html()

    def test_leaf_eq(self):
        node7 = LeafNode('p', 'This is another line of text')
        self.assertEqual(node7.to_html(), "<p>This is another line of text</p>")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node8 = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node8.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node9 = LeafNode(
            tag='a',
            value='Click Me!',
            props='href="https://www.google.com" target="_blank"'
        )
        self.assertEqual(
            node9.to_html(),
            '<a href="https://www.google.com" target="_blank">Click Me!</a>'
        )
