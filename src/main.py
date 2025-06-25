from shutil import rmtree, copy2
from pathlib import Path


def main():
    copy_static_to_public()


def copy_static_to_public():
    source = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/static")
    destination = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/public")

    if destination.exists():
        rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    copy_directory_contents(source, destination)


def copy_directory_contents(src_dir, dest_dir):
    for src_item in src_dir.iterdir():
        dest_item = dest_dir / src_item.name

        try:
            if src_item.is_dir():
                dest_item.mkdir(exist_ok=True)
                copy_directory_contents(src_item, dest_item)
            else:
                copy2(src_item, dest_item)

        except PermissionError:
            print(f"Permission denied for {src_item}")
        except FileNotFoundError:
            print(f"file not found: {src_item}")
        except Exception as e:
            print(f"Error with {src_item}: {e}")


main()
