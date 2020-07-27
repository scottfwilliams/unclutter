import os
import sys
import hashlib
import pathlib


BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files


def walk_fs(start_dir):
    print("Recursively searching contents of {0} for duplicate files".format(start_dir))

    with open("file-db.csv", "w") as out_f:
        for root, dirs, files in os.walk(start_dir):
            for filename in files:
                sha1 = hashlib.sha1()
                full_filepath = os.path.join(root, filename)
                with open(full_filepath, 'rb') as in_f:
                    while True:
                        data = in_f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                filesize = pathlib.Path(full_filepath).stat().st_size
                out_f.write("{0},{1},{2}\n".format(sha1.hexdigest(), filesize, full_filepath))


if __name__ == "__main__":
    start_dir_arg = "."
    if len(sys.argv) > 1: 
        start_dir_arg = sys.argv[1]
    walk_fs(start_dir_arg)
