from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def textnode_to_htmlnode(text_node, children=None):
    p = None
    if text_node.text_type == TextType.LINK and self.url is None:
        raise ValueError("anchor tag requires href property")
    if text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("image tag requires URI property")
        if self.value is None:
            raise ValueError("image requires a description")
    if text_node.text_type == TextType.TEXT:
        tag = None
    else:
        tag = text_node.text_type
    if text_node.url:
        if text_node.text_type == TextType.LINK:
            p['href'] = text_node.url
        if text_node.text_type == TextNode.IMAGE:
            p['src'] = text_node.url
    if children:
        return ParentNode(tag, value=text_node.text, children=children, props=p)
    return LeafNode(tag, value=text_node.text, props=p)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    pass
