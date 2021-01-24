import os
import sys


def walk_fs(start_dir):
    print("Finding list of unique file extensions under " + start_dir)
    extension_set = set()
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            if "." in filename:
                filenm, file_extension = os.path.splitext(filename)
                extension = file_extension.replace(".", "")
                extension_set.add(extension)
    sorted_extensions = sorted(list(extension_set))
    for ext in sorted_extensions:
        print(ext)


if __name__ == "__main__":
    start_dir_arg = "."
    if len(sys.argv) > 1: 
        start_dir_arg = sys.argv[1]
    walk_fs(start_dir_arg)
