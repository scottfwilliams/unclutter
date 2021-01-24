import os
import sys


def walk_fs(starting_dir):
    # print("Picture finder")
    # print("Starting directory is " + starting_dir)

    extensions = {"jpg", "mp4", "gif", "mov", "JPEG", "jpeg", "MP4", "MOV", "JPG", "PNG"}
    """
    extensions = {
        "BMP",
        "GIF",
        "JPEG",
        "JPG",
        "M4A",
        "MOV",
        "PNG",
        "SVG",
        "TIF",
        "TIFF",
        "bmp",
        "gif",
        "jpeg",
        "jpg",
        "m4a",
        "mov",
        "png",
        "svg",
        "tif",
        "tiff"
    }
    # print(extensions)
    """

    for root, dirs, files in os.walk(starting_dir):
        for filename in files: 
            filenm, file_extension = os.path.splitext(filename)
            extension = file_extension.replace(".", "") 
            if extension in extensions:
                print(root + filename)            


if __name__ == "__main__":
    start_dir = "."
    if len(sys.argv) > 1: 
        start_dir = sys.argv[1] 
    walk_fs(start_dir)

