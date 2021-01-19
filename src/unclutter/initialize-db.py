import sqlite3


def main():
    initialize_database("file.db")


def initialize_database(db_file_name):
    # Set up the sqlite DB instance
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    # Create table for file output results
    c.execute("""CREATE TABLE files (sha_hash text, file_size real, filepath text)""")
    print("Initialized new sqlite database file {}".format(db_file_name))
    conn.close()


if __name__ == "__main__":
    main()
