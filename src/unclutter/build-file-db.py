import os
import sys
import hashlib
import pathlib
import sqlite3


BUF_SIZE = 65536  # read files in 64kb chunks to avoid consuming excess memory on large files


def walk_fs(start_dir):
    # Set up the sqlite DB instance
    conn = sqlite3.connect("file.db")
    c = conn.cursor()

    # Create table for file output results
    c.execute('''CREATE TABLE files (sha_hash text, file_size real, filepath text)''')

    print("Recursively searching contents of {0} for duplicate files".format(start_dir))
    with open("file-db.csv", "w") as out_f:
        for root, dirs, files in os.walk(start_dir):
            for filename in files:
                sha1 = hashlib.sha1()
                full_filepath = os.path.join(root, filename)
                with open(full_filepath, "rb") as in_f:
                    while True:
                        data = in_f.read(BUF_SIZE)
                        if not data:
                            break
                        sha1.update(data)
                filesize = pathlib.Path(full_filepath).stat().st_size
                digest = sha1.hexdigest()
                # Insert a row of data
                # insert_stmt = "INSERT INTO files VALUES ('{0}',{1},'{2}')".format(
                #    sha1.hexdigest(), filesize, full_filepath)
                # c.execute(insert_stmt)
                c.execute("INSERT INTO files VALUES (?,?,?)", (digest, filesize, full_filepath))

                out_f.write("{0},{1},{2}\n".format(digest, filesize, full_filepath))
    # Save (commit) the changes
    conn.commit()
    c.execute("SELECT count(*) FROM files")
    count = c.fetchone()
    print("Total of {} files processed".format(count[0]))

    c.execute("SELECT count(*) AS qty, sha_hash FROM files GROUP BY sha_hash HAVING count(*) > 1")
    duplicates = c.fetchall()
    print("There are {} sets of duplicated files".format(len(duplicates)))
    list_duplicate_sets(duplicates, c)
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
