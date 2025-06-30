from shutil import rmtree
from pathlib import Path
from copy_static import copy_static_content
import sys


dir_path_static = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/static")
dir_path_public = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/docs")
dir_path_content = Path("/home/onodac/workspace/github.com/CamilleOnoda/static-site-generator/content")
path_template = "./template.html"
default_basepath = "/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if dir_path_public.exists():
        rmtree(dir_path_public)

    print("--> Creating public directory...")
    dir_path_public.mkdir(parents=True, exist_ok=True)

    print("--> Copying static content to public content...")
    copy_static_content(dir_path_static, dir_path_public, path_template, basepath)

    print("--> Generating content...")
    print("Success!")


main()
