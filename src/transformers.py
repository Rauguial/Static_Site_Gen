import re
import os
import shutil
from pathlib import Path
from textnode import *
from htmlnode import *
from blocktype import BlockType


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
        case TextType.IMAGE:
            return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text})
        case TextType.LINK:
            if not text_node.url or not text_node.text:
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


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block:
            cleaned_lines = [line.strip() for line in block.split("\n")]
            blocks.append("\n".join(cleaned_lines))
    return blocks
    

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    lines = block.split("\n")
    if all(re.match(rf"^{i+1}\. ", line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                level = block.count("#") #Count number of #
                text = block[level + 1:].strip() #Remove the # and space
                children.append(ParentNode(tag=f"h{level}", children=text_to_children(text)))

            case BlockType.CODE:
                code_lines = block.split("\n")[1:-1]
                code_text = "\n".join(code_lines) + "\n"
                code_node = ParentNode(tag="code", children=[LeafNode(None, code_text)])
                pre_node = ParentNode(tag="pre", children=[code_node])
                children.append(pre_node)
            
            case BlockType.QUOTE:
                quote_text = "\n".join(line[2:] for line in block.split("\n"))
                children.append(ParentNode(tag="blockquote", children=text_to_children(quote_text)))

            case BlockType.UNORDERED_LIST:
                list_items = [ParentNode(tag="li", children=text_to_children(line[2:])) for line in block.split("\n")]
                children.append(ParentNode(tag="ul", children=list_items))

            case BlockType.ORDERED_LIST:
                list_items = [ParentNode(tag="li", children=text_to_children(line[3:])) for line in block.split("\n")]
                children.append(ParentNode(tag="ol", children=list_items))

            case BlockType.PARAGRAPH:
                cleaned_text = " ".join(line.strip() for line in block.split())
                children.append(ParentNode(tag="p", children=text_to_children(cleaned_text)))
        
    return ParentNode(tag="div", children=children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]



def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match(r"^#{1} ", block):
            return block[1:].strip()
        else:
            raise Exception("No h1 header.")
        


def generate_page(from_path, template_path, dest_path, base_path="/"): #added base_path
    print(f"DEBUG - Destination path: {dest_path}")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    # Convert paths to strings if they're Path objects
    from_path = str(from_path)
    template_path = str(template_path)
    dest_path = str(dest_path)
    #new above


    with open(from_path, "r") as md_file:
        markdown = md_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()
    
    html_content = markdown_to_html_node(markdown).to_html()



    # Handle paths based on destination
    if "blog/" in dest_path:
        # Blog posts need different relative paths
        html_content = html_content.replace('src="/Static_Site_Gen/images/', 'src="../../images/')
        html_content = html_content.replace('href="/Static_Site_Gen/"', 'href="../../index.html"')
    else:
        # Root-level pages
        html_content = html_content.replace('src="/Static_Site_Gen/images/', 'src="images/')
        html_content = html_content.replace('href="/Static_Site_Gen/"', 'href="index.html"')
    
    # Convert .md links to .html
    html_content = html_content.replace('.md"', '.html"')



    title = extract_title(markdown) 
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content) 
    
   

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as html_file:
        html_file.write(full_html)
    print(f"DEBUG - Wrote HTML to: {os.path.abspath(dest_path)}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"): #added base_path
    content_dir = Path(dir_path_content)
    dest_dir = Path(dest_dir_path)

    for item in content_dir.iterdir():
        if item.is_dir():
            new_dest = dest_dir / item.name
            new_dest.mkdir(exist_ok=True)
            generate_pages_recursive(item, template_path, new_dest, base_path) #added base_path
        
        elif item.suffix == ".md":
            dest_path = dest_dir / f"{item.stem}.html"
            generate_page(item, template_path, dest_path, base_path) #added base_path