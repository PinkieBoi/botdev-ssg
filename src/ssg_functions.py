import re
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
    delimiters = {"*": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    delimiter_found = False
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(TextNode(n.text, n.text_type))
        if delimiter in n.text:
            delimiter_found = True
            node_text = n.text.split(f" {delimiter}")
            new_nodes.append(TextNode(f"{node_text[0]} ", TextType.TEXT))
            second_split = node_text[1].split(delimiter)
            new_nodes.append(TextNode(second_split[0], delimiters[delimiter]))
            new_nodes.append(TextNode(second_split[1], TextType.TEXT))
    if not delimiter_found:
        raise ValueError(f"{delimiter} not present in {n.text}")
    return new_nodes


def extract_md_images(old_node):
    image_data = re.findall(
        r'\!\[([a-zA-Z ]+)\]\(([\w]+?\:?\/?\/?[\w+]+?\.\w+\.\w+\/?.+?)\)',
        old_node
    )
    return image_data


def extract_md_links(old_node):
    link_data = re.findall(
        r'\[([a-zA-Z ]+)\]\(([\w]+?\:?\/?\/?[\w+]+?\.\w+\.\w+\/?.+?)\)',
        old_node
    )
    return link_data


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        image_data = extract_md_images(n.text)
        for d in image_data:
            new_nodes.append(TextNode(n.text.split(f"![{d[0]}]")[0], TextType.TEXT))
            new_nodes.append(TextNode(d[0].split(f"{new_nodes[-1][-1]})"), TextType.IMAGE, d[1]))
        new_nodes.append(TextNode(n.text.split(f"{image_data[-1][1]})")[1], TextType.TEXT))
    print(new_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        image_data = extract_md_images(n.text)
        for d in image_data:
            new_nodes.append(TextNode(f"{n.text.split(f" [{d[0]}]")[0]} ", TextType.TEXT))
            new_nodes.append(TextNode(d[0], TextType.LINK, d[1]))
        new_nodes.append(TextNode(n.text.split(f"{image_data[-1][1]})")[1], TextType.TEXT))
    return new_nodes
