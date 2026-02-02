import unittest
from ssg_functions import extract_md_images, extract_md_links
from htmlnode import LeafNode


class test_extract_md_images(unittest.TestCase):

    def test_extract_images(self):
        first_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        second_text = "I'm prbably not your father! ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_md_images(first_text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])
        self.assertListEqual(extract_md_images(second_text), [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


class test_extract_md_link(unittest.TestCase):

    def test_extract_links(self):
        matches = extract_md_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
