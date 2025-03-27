from enum import Enum

class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**bold text**"
    ITALIC = "_italized text_"
    CODE = "`code`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

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
    
    

    
