import os
import sys


def remove_dirpaths(input_file):
    fileset = set()
    with open(input_file, "r") as img_file:
        for line in img_file:
            pathparts = line.split("/")
            filename = pathparts[-1]
            fileset.add(filename)
    print("Found {} unique files".format(len(fileset)))
    output_filename = "unique_image_files.txt"

    sorted_files = sorted(fileset)
    with open(output_filename, "w") as out_file:
        out_file.writelines(sorted_files)


if __name__ == "__main__":
    start_dir = "."
    if len(sys.argv) > 0:
        image_file = sys.argv[1]
        remove_dirpaths(image_file)
    else:
        print("ERROR: Input file name argumentrequired")
