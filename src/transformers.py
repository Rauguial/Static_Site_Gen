import re
from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode instance")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link TextNode must have URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter {delimiter} in text: {node.text}")
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
    

def extract_markdown_images(text):
    find_image = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return find_image

def extract_markdown_links(text):
    find_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return find_link

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #Only split TEXT nodes
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text) #Extract images
        if not images: #If no image, keep node
            new_nodes.append(node)
            continue
        text = node.text
        for alt_text, img_url in images:
            sections = text.split(f"![{alt_text}]({img_url})", 1) #Split once
            if sections[0]: #Add preceding text if not empty
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url)) #Add image
            text = sections[1] if len(sections) > 1 else ""  #Remaining text
        
        if text: #Add remaining text if not emtpy
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #Only split TEXT nodes
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text) #Extract links
        if not links: #If no link, keep node
            new_nodes.append(node)
            continue
        text = node.text
        for title, link_url in links:
            sections = text.split(f"[{title}]({link_url})", 1) #Split once
            if sections[0]: #Add preceding text if not empty
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(title, TextType.LINK, link_url)) #Add links
            text = sections[1] if len(sections) > 1 else ""  #Remaining text
        
        if text: #Add remaining text if not emtpy
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


