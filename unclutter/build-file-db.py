import os
import sys
import hashlib
import pathlib
import sqlite3
from pathlib import Path


BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files
DB_FILENAME = "file.db"


def clean_filepath_str(relative_path_str):
    return str(clean_filepath(relative_path_str))


def clean_filepath(relative_path_str):
    relative_path = Path(relative_path_str)
    return relative_path.absolute()  # absolute is a Path object


def walk_fs(start_dir):
    # Set up the sqlite DB instance
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    # Get absolute path of start directory
    start_dir_abslt = clean_filepath_str(start_dir)

    print("Recursively searching contents of {0} for duplicate files".format(start_dir_abslt))
    with open("file-db.csv", "w") as out_f:
        for root, dirs, files in os.walk(start_dir_abslt):
            for filename in files:
                sha1 = hashlib.sha1()
                full_filepath = os.path.join(root, filename)
                try:
                    with open(full_filepath, "rb") as in_f:
                        while True:
                            data = in_f.read(BUF_SIZE)
                            if not data:
                                break
                            sha1.update(data)
                    filesize = pathlib.Path(full_filepath).stat().st_size
                    digest = sha1.hexdigest()
                    c.execute("INSERT INTO files VALUES (?,?,?)", (digest, filesize, full_filepath))
                    out_f.write("{0},{1},{2}\n".format(digest, filesize, full_filepath))
                except:
                    c.execute("INSERT INTO files VALUES (?,?,?)", ("FAILED", 0, full_filepath))

    # Save (commit) the changes
    conn.commit()
    c.execute("SELECT count(*) FROM files")
    count = c.fetchone()
    print("Total of {} files processed".format(count[0]))

    c.execute("SELECT count(*) AS qty, sha_hash FROM files GROUP BY sha_hash HAVING count(*) > 1")
    duplicates = c.fetchall()
    print("There are {} sets of duplicated files".format(len(duplicates)))
    # list_duplicate_sets(duplicates, c)
    conn.close()


def list_duplicate_sets(duplicates, c):
    for duplicate in duplicates:
        print("These {0} files have identical content".format(duplicate[0]))
        c.execute("SELECT filepath FROM files WHERE sha_hash = ?", (duplicate[1], ))
        for dupe_file in c.fetchall():
            print("  {0}".format(dupe_file[0]))


if __name__ == "__main__":
    start_dir_arg = "."
    if len(sys.argv) > 1:
        start_dir_arg = sys.argv[1]
    walk_fs(start_dir_arg)
