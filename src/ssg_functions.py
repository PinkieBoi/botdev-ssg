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
    if not any(delimiter in n.text for n in old_nodes):
        raise ValueError(f"{delimiter} not present in nodes provided")
    new_nodes = []
    for n in old_nodes:
        special_text = re.findall(f"{delimiter}(.*?){delimiter}", n.text)
        node_text = n.text.split(delimiter)
        for split_text in node_text:
            if split_text in special_text:
                new_nodes.append(TextNode(split_text, text_type))
            else:
                new_nodes.append(TextNode(split_text, TextType.TEXT))
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
            txt = n.text.split(f"![{d[0]}]")
            if image_data.index(d) == 0:
                new_nodes.append(TextNode(n.text.split(f"![{d[0]}]({d[1]})")[0], TextType.TEXT))
            else:
                new_nodes.append(TextNode(n.text.split(f"![{d[0]}]({d[1]})")[0].split(f"{image_data[image_data.index(d) - 1][1]})")[1], TextType.TEXT))
            new_nodes.append(TextNode(d[0], TextType.IMAGE, d[1]))
            if len(image_data) == 1 or image_data.index(d) == len(image_data) - 1:
                if len(n.text.split(f"{image_data[-1][1]})")[1]) > 0:
                    new_nodes.append(TextNode(n.text.split(f"{image_data[-1][1]})")[1], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        link_data = extract_md_links(n.text)
        for d in link_data:
            txt = n.text.split(f"[{d[0]}]")
            if link_data.index(d) == 0:
                new_nodes.append(TextNode(n.text.split(f"[{d[0]}]({d[1]})")[0], TextType.TEXT))
            else:
                new_nodes.append(TextNode(n.text.split(f"[{d[0]}]({d[1]})")[0].split(f"{link_data[link_data.index(d) - 1][1]})")[1], TextType.TEXT))
            new_nodes.append(TextNode(d[0], TextType.LINK, d[1]))
            if len(link_data) == 1 or link_data.index(d) == len(link_data) - 1:
                if len(n.text.split(f"{link_data[-1][1]})")[1]) > 0:
                    new_nodes.append(TextNode(n.text.split(f"{link_data[-1][1]})")[1], TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    pass
