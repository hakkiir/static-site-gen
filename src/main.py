from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os, shutil
from markdown_to_html import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for entry in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content,entry)
        print(entry)
        print(f"path: {path}")
        print(dir_path_content)
        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, dest_dir_path)
        if os.path.isfile(path):
            tail = os.path.split(path)[1]
            head = os.path.split(path)[0]
            headless = head.lstrip("content/")
            pub_path = dest_dir_path+headless+"/"
            if entry.endswith(".md"):
                if not os.path.isdir(pub_path):
                    os.mkdir(pub_path)
                print(f"dest dir path : {dest_dir_path}")
                print(f"tail : {tail}")
                print(f"pubpath : {pub_path}")
                generate_page(path, "template.html", f"{pub_path}{tail.rstrip(".md")}.html")
    return "pages generated"


def copy_recursevily(dir, destination):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        print(f"dir:{dir}, file: {file}")
        if os.path.isfile(file_path):
             print(f"copying {file_path}")
             print(f"to: {destination}")
             shutil.copy(file_path, destination)
        if os.path.isdir(file_path):
            os.mkdir(os.path.join(destination, file))
            copy_recursevily(file_path, os.path.join(destination, file))
    return "shit copied"

def copy_directory_contents(source="../static-site-gen/static", destination="../static-site-gen/public"):
    if not os.path.exists(source):
        raise ValueError("Invalid source path")
    elif not os.path.exists(destination):
        raise ValueError("Invalid destination path")

    shutil.rmtree(destination)
    os.mkdir(destination)
    copy_recursevily(source, destination)
    return "copying ready"
    
def exctract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        print(f"extract_title: {line}")
        if line.startswith("# "):
            return line[2:]
    raise ValueError ("h1 header not found")    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} from {template_path} ")
    md_file = open(from_path, "r")
    md_file = md_file.read()
    template = open(template_path, "r").read()
    html_node = markdown_to_html_node(md_file)
    html = html_node.to_html()
    title = exctract_title(md_file)
    template_w_header = template.replace("{{ Title }}", title)
    template_w_content = template_w_header.replace("{{ Content }}", html)
    head = os.path.split(dest_path)[0]
    if os.path.isdir(head):
        file = open(dest_path, "w")
        file.write(template_w_content)
    else:
        for dir in os.listdir(head):
            if not os.path.isdir(dir):
                os.mkdir(dir)
        file = open(dest_path, "w")
        file.write(template_w_content)
    return "something happened"


def main():
    copy_directory_contents()
    generate_pages_recursive("content/", "template.html", "public/" )
    #generate_page("content/index.md", "template.html", "public/")
    #generate_page("content/majesty/index.md", "template.html", "public/")

if __name__ == "__main__":
    main()

