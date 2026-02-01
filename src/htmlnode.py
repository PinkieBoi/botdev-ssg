class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = self.props_to_html(props)

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self, value):
        if value is None:
            return None
        return {prop.split("=")[0]: prop.split("=")[1] for prop in value.split(" ")}

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(self)
        self.children = None
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        html_props = ""
        if self.props is not None:
            html_props = " " + self.props
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(LeafNode):
    def __init__(self, tag, children, props=None):
        super().__init__(self)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag must not be None")
        if self.children is None:
            raise ValueError("ParentNode object must have children")
        children_str = "".join([child.to_html() for child in self.children])
        html_props = ""
        if self.props is not None:
            html_props = " " + self.props
        return f"<{self.tag}{html_props}>{children_str}</{self.tag}>"
