import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def textnode_to_htmlnode(text_node, children=None):
    p = None
    if text_node.text_type == TextType.LINK and text_node.url is None:
        raise ValueError("anchor tag requires href property")
    if text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("image tag requires URI property")
        if text_node.value is None:
            raise ValueError("image requires a description")
    if text_node.text_type == TextType.TEXT:
        tag = None
    else:
        tag = text_node.text_type
    if text_node.url:
        if text_node.text_type == TextType.LINK:
            p["href"] = text_node.url
        if text_node.text_type == TextNode.IMAGE:
            p["src"] = text_node.url
    if children:
        return ParentNode(tag, value=text_node.text, children=children, props=p)
    return LeafNode(tag, value=text_node.text, props=p)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not any(delimiter in n.text for n in old_nodes):
        return old_nodes
    for n in old_nodes:
        special_text = re.findall(f"{delimiter}(.*?){delimiter}", n.text)
        node_text = n.text.split(delimiter)
        for split_text in node_text:
            if split_text in special_text:
                new_nodes.append(TextNode(split_text, text_type))
            else:
                new_nodes.append(TextNode(split_text, TextType.TEXT))
    return new_nodes


def extract_md_images(old_node_text: str):
    image_data = re.findall(
        r"\!\[([a-zA-Z ]+)\]\(([\w]+?\:?\/?\/?[\w+]+?\.\w+\.\w+\/?.+?)\)", old_node_text
    )
    return image_data


def extract_md_links(old_node_text: str):
    link_data = re.findall(
        r"\[([a-zA-Z ]+)\]\(([\w]+?\:?\/?\/?[\w+]+?\.\w+\.\w+\/?.+?)\)", old_node_text
    )
    return link_data


def split_nodes_image(old_nodes: list):
    # for node in old_nodes:
        # print(len(re.findall(r'\!\[([a-zA-Z ]+)\]\(([\w]+?\:?\/?\/?[\w+]+?\.\w+\.\w+\/?.+?)\)', node.text)))

    new_nodes = []
    images_data = []
    for n in old_nodes:
        images_data.extend(extract_md_images(n.text))
    if len(images_data) == 0:
        return old_nodes
    for node in old_nodes:
        if type(node) != TextNode:
            raise ValueError("arg must be list of TextNode objects")
        image_data = extract_md_images(node.text)
        for d in image_data:
            if image_data.index(d) == 0:
                new_nodes.append(
                    TextNode(node.text.split(f"![{d[0]}]({d[1]})")[0], TextType.TEXT)
                )
            else:
                new_nodes.append(
                    TextNode(
                        node.text.split(f"![{d[0]}]({d[1]})")[0].split(
                            f"{image_data[image_data.index(d) - 1][1]})"
                        )[1],
                        TextType.TEXT,
                    )
                )
            new_nodes.append(TextNode(d[0], TextType.IMAGE, d[1]))
            if len(image_data) == 1 or image_data.index(d) == len(image_data) - 1:
                if len(node.text.split(f"{image_data[-1][1]})")[1]) > 0:
                    new_nodes.append(
                        TextNode(
                            node.text.split(f"{image_data[-1][1]})")[1], TextType.TEXT
                        )
                    )
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        link_data = extract_md_links(n.text)
        for d in link_data:
            if link_data.index(d) == 0:
                new_nodes.append(
                    TextNode(n.text.split(f"[{d[0]}]({d[1]})")[0], TextType.TEXT)
                )
            else:
                new_nodes.append(
                    TextNode(
                        n.text.split(f"[{d[0]}]({d[1]})")[0].split(
                            f"{link_data[link_data.index(d) - 1][1]})"
                        )[1],
                        TextType.TEXT,
                    )
                )
            new_nodes.append(TextNode(d[0], TextType.LINK, d[1]))
            if len(link_data) == 1 or link_data.index(d) == len(link_data) - 1:
                if len(n.text.split(f"{link_data[-1][1]})")[1]) > 0:
                    new_nodes.append(
                        TextNode(n.text.split(f"{link_data[-1][1]})")[1], TextType.TEXT)
                    )
    return new_nodes


def text_to_textnodes(text):
    text_nodes = []
    delims = []
    for d in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        if d.value[0] in text:
            delims.append(d)
    text_img = split_nodes_image([TextNode(text, TextType.TEXT)])
    # text_nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
    # for t in delims:
    #     text_nodes = split_nodes_delimiter(text_nodes, t.value[0], t)
    # if text_nodes[-1].text == "":
        # text_nodes.pop(-1)
    return text_img
