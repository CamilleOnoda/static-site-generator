from inline_markdown import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            text = markdown.split("# ")
            title = text[1].split("\n\n")
            return title[0].strip()
    raise ValueError("No title found.")


def generate_pages(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print()
    
    with open(from_path) as file:
        markdown_content = file.read()
        
    with open(template_path) as file:
        template_content = file.read()

    title = extract_title(markdown_content)
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    new_template = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html)

    final_template = new_template.replace('href="/', f'href="{basepath}').replace(
        'src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(final_template)