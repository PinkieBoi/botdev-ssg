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
