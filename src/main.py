from shutil import rmtree, copy2
from pathlib import Path
from inline_markdown import markdown_to_html_node
import os, sys


def main():
    if not sys.argv[1]:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    copy_static_to_docs(basepath)
    copy_content_to_docs(basepath)
    generate_pages("content/index.md", "template.html", "docs/index.html", basepath)


def copy_static_to_docs(basepath):
    source = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/static")
    destination = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/docs")

    if destination.exists():
        rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    copy_directory_contents(source, destination, basepath)


def copy_content_to_docs(basepath):
    source = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/content")
    destination = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/docs")

    copy_directory_contents(source, destination, basepath)


def copy_directory_contents(src_dir, dest_dir, basepath):
    for src_item in src_dir.iterdir():
        dest_item = dest_dir / src_item.name

        try:
            if src_item.is_dir():
                dest_item.mkdir(exist_ok=True)
                copy_directory_contents(src_item, dest_item, basepath)
            elif src_item.suffix.lower() == ".md":
                new_extension = ".html"
                new_html = dest_item.with_suffix(new_extension)
                generate_pages(src_item, "template.html", new_html, basepath)
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


def generate_pages(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        markdown_content = file.read()
        
    with open(template_path) as file:
        template_content = file.read()

    title = extract_title(markdown_content)
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    new_template = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html)

    final_template = new_template.replace('href="/"', 'href="{basepath}').replace(
        'src="/', 'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(final_template)


main()
