# -*- coding: utf-8 -*-

import os
import hashlib
import pathlib

from unclutter.file_utilities import valid_dirpath
from unclutter.command import _exclude_list as excludes, _platform as platform

BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files
ENTRY_HDR = "filename|file size|SHA1 hash|full filepath"


def walk_target_fs(start_dir):
    print("walk_target_fs start_dir: {}".format(start_dir))

    # Each record in entries is a tuple containing the filename, SHA1 hash, file size, and the
    # fully qualified filepath
    entries = set()
    # TODO: Fix the ignore list handling
    for root, dirs, files in os.walk(start_dir):
        print("Processing {} directory...".format(root))
        for filename in files:
            if os.path.isdir(filename):
                continue
            if filename in excludes:
                continue
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


def import_entries_from_file(import_filename):
    entries = set()
    with open(import_filename, "r") as import_f:
        for input_record in import_f:
            input_record = input_record.rstrip()
            if input_record != ENTRY_HDR:
                entries.add(tuple(input_record.split("|")))
    return entries


def ingest_fs(fs_name, fs_path):
    print("fs_path: {}".format(fs_path))   # TODO - get rid of this log statement
    print("Processing new filesystem \"{}\"".format(fs_name))
    rootdir_name = os.path.split(fs_path)[1]
    if not valid_dirpath(fs_path):
        print("{} is not a directory".format(fs_path))
    elif rootdir_name in excludes:
        print("Processing skipped: Root directory '{}' is in exclude list".format(rootdir_name))
    else:
        print("Analyzing files in '{}'".format(fs_path))
        fs_entries = walk_target_fs(fs_path)
        display_fs_entries(fs_entries, fs_name)
        export_entries_to_file(fs_entries, fs_name)
    print("Finished")


def identify_duplicates(*entry_sets):
    for idx in range(len(entry_sets)):
        print("{} : {}".format(entry_sets[idx], entry_sets[idx+1:]))


def show_ignored_files():
    print("Platform: {}".format(platform))
    print("ignore_list: {}".format(excludes))


def compare_fs():
    print("compare filesystems")
