from enum import Enum

class TextType(Enum):
    Normal = "Normal text"
    BOLD = "**bold text**"
    Italic = "_italized text_"
    Code = "`code`"
    link = "[anchor text](url)"
    image = "![alt text](url)"

class TextNode:
    def __init__(self, text, TextType, url = None):
        self.text = text
        self.text_type = TextType
        self.url = url
    
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return vars(self) == vars(other)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
