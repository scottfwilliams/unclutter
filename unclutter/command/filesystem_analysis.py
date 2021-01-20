# -*- coding: utf-8 -*-

import os
import hashlib
import pathlib


from unclutter.file_utilities import valid_dirpath


BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files
ENTRY_HDR = "filename|file size|SHA1 hash|full filepath"


def walk_target_fs(start_dir):
    # Each record in entries is a tuple containing the filename, SHA1 hash, file size, and the
    # fully qualified filepath
    entries = set()
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            sha1hash = hashlib.sha1()
            full_filepath = os.path.join(root, filename)
            with open(full_filepath, "rb") as in_f:
                while True:
                    data = in_f.read(BUF_SIZE)
                    if not data:
                        break
                    sha1hash.update(data)
            filesize = pathlib.Path(full_filepath).stat().st_size
            sha1digest = sha1hash.hexdigest()
            entries.add((filename, str(filesize), str(sha1digest), full_filepath))
    return entries


def display_fs_entries(entries, fs_name):
    print()
    print("Summary of files from {}".format(fs_name))
    print(ENTRY_HDR)
    for record in entries:
        print("|".join(record))


def export_entries_to_file(entries, fs_name):
    export_fn = "{}-export.csv".format(fs_name)
    with open(export_fn, "w") as export_f:
        export_f.write("{}\n".format(ENTRY_HDR))
        for input_record in entries:
            output_record = "|".join(input_record)
            export_f.write("{}\n".format(output_record))


def ingest_fs(fs_name, fs_path):
    print("Processing new filesystem \"{}\"".format(fs_name))
    if not valid_dirpath(fs_path):
        print("{} is not a directory".format(fs_path))
        return
    print("Analyzing files in {}...".format(fs_path))
    fs_entries = walk_target_fs(fs_path)
    display_fs_entries(fs_entries, fs_name)
    export_entries_to_file(fs_entries, fs_name)


def compare_fs():
    print("compare filesystems")
