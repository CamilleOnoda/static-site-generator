from shutil import rmtree, copy2
from pathlib import Path
from inline_markdown import markdown_to_html_node
import os


def main():
    copy_static_to_public()
    copy_content_to_public()
    generate_pages("content/index.md", "template.html", "public/index.html")


def copy_static_to_public():
    source = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/static")
    destination = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/public")

    if destination.exists():
        rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    copy_directory_contents(source, destination)


def copy_content_to_public():
    source = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/content")
    destination = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/public")

    copy_directory_contents(source, destination)


def copy_directory_contents(src_dir, dest_dir):
    for src_item in src_dir.iterdir():
        print(src_item.name)
        dest_item = dest_dir / src_item.name

        try:
            if src_item.is_dir():
                dest_item.mkdir(exist_ok=True)
                copy_directory_contents(src_item, dest_item)
            elif src_item.suffix.lower() == ".md":
                new_extension = ".html"
                new_html = dest_item.with_suffix(new_extension)
                generate_pages(src_item, "template.html", new_html)
            else:
                copy2(src_item, dest_item)

        except PermissionError:
            print(f"Permission denied for {src_item}")
        except FileNotFoundError:
            print(f"file not found: {src_item}")
        except Exception as e:
            print(f"Error with {src_item}: {e}")


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            text = markdown.split("# ")
            title = text[1].split("\n\n")
            return title[0].strip()


def generate_pages(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        markdown_content = file.read()
        
    with open(template_path) as file:
        template_content = file.read()

    title = extract_title(markdown_content)
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    final_template = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(final_template)


main()
