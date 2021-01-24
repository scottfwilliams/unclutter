# -*- coding: utf-8 -*-

import click

from unclutter.command.filesystem_analysis import ingest_fs, compare_fs, import_entries_from_file
from unclutter.command.filesystem_analysis import show_excluded_files
from unclutter.file_utilities import get_canonical_fp_str


@click.group()
def cli():
    pass


@click.command()
@click.option("--rootdir", default=".", help="ingested filesystem root directory")
@click.argument("name")
def ingest(rootdir, name):
    canonical_rootdir = get_canonical_fp_str(rootdir)
    click.echo("Filesystem root directory: {}".format(canonical_rootdir))
    click.echo("Filesystem name: {}".format(name))
    ingest_fs(name, canonical_rootdir)


@click.command()
@click.argument("result-filepath")
def load(result_filepath):
    entries = import_entries_from_file(result_filepath)
    for entry_record in entries:
        print(entry_record)


@click.command()
def show_excluded():
    show_excluded_files()


@click.command()
def compare():
    compare_fs()


cli.add_command(ingest)
cli.add_command(compare)
cli.add_command(load)
cli.add_command(show_excluded)
