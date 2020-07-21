import os
import sys


def walk_fs(start_dir):
    print("Extension finder")
    print("Starting directory is " + start_dir)
    extension_set = set()
    for root, dirs, files in os.walk(start_dir):
        for filename in files: 
            filenm, file_extension = os.path.splitext(filename)
            extension = file_extension.replace(".", "") 
            # print(extension)
            extension_set.add(extension) 
    for ext in extension_set:
        print(ext)


if __name__ == "__main__":
    start_dir = "."
    if len(sys.argv) > 1: 
        start_dir = sys.argv[1] 
    walk_fs(start_dir)

