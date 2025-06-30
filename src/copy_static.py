from shutil import copy2
from generate_content import generate_pages

def copy_static_content(src_dir, dest_dir, path_template, basepath):
    for src_item in src_dir.iterdir():
        dest_item = dest_dir / src_item.name

        try:
            if src_item.is_dir():
                dest_item.mkdir(exist_ok=True)
                copy_static_content(src_item, dest_item, path_template, basepath)
            elif src_item.suffix.lower() == ".md":
                new_extension = ".html"
                new_html = dest_item.with_suffix(new_extension)
                generate_pages(src_item, path_template, new_html, basepath)
            else:
                copy2(src_item, dest_item)

        except PermissionError:
            print(f"Permission denied for {src_item}")
        except FileNotFoundError:
            print(f"file not found: {src_item}")
        except Exception as e:
            print(f"Error with {src_item}: {e}")