from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os, shutil

def copy_shit(dir, destination):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        print(f"dir:{dir}, file: {file}")
        if os.path.isfile(file_path):
             print(f"copying {file_path}")
             print(f"to: {destination}")
             shutil.copy(file_path, destination)
        if os.path.isdir(file_path):
            os.mkdir(os.path.join(destination, file))
            copy_shit(file_path, os.path.join(destination, file))
    return "shit copied"

def copy_directory_contents(source="../static-site-gen/static", destination="../static-site-gen/public"):
    if not os.path.exists(source):
        raise ValueError("Invalid source path")
    elif not os.path.exists(destination):
        raise ValueError("Invalid destination path")

    shutil.rmtree(destination)
    os.mkdir(destination)
    copy_shit(source, destination)
    return "copying ready"
    

def main():
    print(copy_directory_contents())

if __name__ == "__main__":
    main()

