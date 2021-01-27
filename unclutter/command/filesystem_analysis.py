# -*- coding: utf-8 -*-
import os
import hashlib
import pathlib

from collections import defaultdict

from unclutter.file_utilities import valid_dirpath
from unclutter.command import _exclude_list as excludes, _platform as platform

BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files
ENTRY_HDR = "filesystem name|filename|file size|SHA1 hash|full filepath"


def walk_target_fs(start_dir, fs_name):
    # Each record in entries is a tuple containing the filename, SHA1 hash, file size, and the
    # fully qualified filepath
    entries = set()
    for root, dirs, files in os.walk(start_dir, topdown=True):
        print("Processing {} directory...".format(root))
        # print("dirs BEFORE: {}".format(dirs))
        dirs[:] = [d for d in dirs if d not in excludes]
        # print("dirs AFTER:  {}".format(dirs))
        for filename in files:
            if filename in excludes:
                continue
            if os.path.isdir(filename):
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
            entries.add((fs_name, filename, str(filesize), str(sha1digest), full_filepath))
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
    print("Processing new filesystem \"{}\"".format(fs_name))
    rootdir_name = os.path.split(fs_path)[1]
    if not valid_dirpath(fs_path):
        print("{} is not a directory".format(fs_path))
    elif rootdir_name in excludes:
        print("Processing skipped: Root directory '{}' is in exclude list".format(rootdir_name))
    else:
        print("Analyzing files in '{}'".format(fs_path))
        fs_entries = walk_target_fs(fs_path, fs_name)
        display_fs_entries(fs_entries, fs_name)
        export_entries_to_file(fs_entries, fs_name)
    print("Finished")


def show_excluded_files():
    print("Platform: {}".format(platform))
    print("Excuded file/directory list: {}".format(excludes))


def identify_duplicates(*entry_sets):
    for idx in range(len(entry_sets)):
        print("{} : {}".format(entry_sets[idx], entry_sets[idx+1:]))


def validate_input_result_files(filesystem_results):
    print("Compare file sets for duplicate files in")
    for result_file in filesystem_results:
        if not os.path.isfile(result_file):
            print("Error: {} file not found".format(result_file))
            print("Exiting...")
            return False
        print("-> {}".format(result_file))
    return True


def compare_fs(filesystem_results):
    if validate_input_result_files(filesystem_results):
        fs_name_to_resultset_dict = {}
        filehash_to_fs_names_list_dict = defaultdict(list)
        hash_and_fs_name_to_result_dict = {}
        for result_fn in filesystem_results:
            result_set = import_entries_from_file(result_fn)
            random_element = next(iter(result_set))
            filesystem_name = random_element[0]
            fs_name_to_resultset_dict[filesystem_name] = result_set
            for file_result_tuple in iter(result_set):
                file_hash = file_result_tuple[3]
                filehash_to_fs_names_list_dict[file_hash].append(filesystem_name)
                hash_fs_name_tuple = (file_hash, filesystem_name)
                hash_and_fs_name_to_result_dict[hash_fs_name_tuple] = file_result_tuple
        print("Duplicate files: ")
        for dupe_file_hash, list_of_filesystems in filehash_to_fs_names_list_dict.items():
            if len(list_of_filesystems) > 1:
                print("File hash {}".format(dupe_file_hash))
                for fs_name in list_of_filesystems:
                    dupe_tuple = hash_and_fs_name_to_result_dict[(dupe_file_hash, fs_name)]
                    print("  File system: {}, File name: {}".format(fs_name, dupe_tuple[4]))
