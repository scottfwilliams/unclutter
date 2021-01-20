# -*- coding: utf-8 -*-

import click

from unclutter.command.filesystem_analysis import ingest_fs, compare_fs
from unclutter.file_utilities import get_canonical_fp_str


@click.group()
def cli():
    pass


@click.command()
@click.option("--rootdir", default=".", help="ingested filesystem root directory")
@click.argument("name")
def ingest(rootdir, name):
    canonical_rootdir = get_canonical_fp_str(rootdir)
    click.echo("filesystem root directory: {}".format(canonical_rootdir))
    click.echo("filesystem name: {}".format(name))
    ingest_fs()


@click.command()
def compare():
    compare_fs()


cli.add_command(ingest)
cli.add_command(compare)
