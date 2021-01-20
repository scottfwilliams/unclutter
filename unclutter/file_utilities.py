# -*- coding: utf-8 -*-

from pathlib import Path


"""
    Converts relative filepath to canonical filepath for clarity
    :param relative_fp_str: string representation of relative filepath
    :return: Path object for absolute filepath
"""
def get_canonical_fp(relative_fp_str):
    relative_path = Path(relative_fp_str)
    return relative_path.absolute()


def get_canonical_fp_str(relative_fp_str):
    return str(get_canonical_fp(relative_fp_str))


def valid_dirpath(dirpath_str):
    dirpath = Path(dirpath_str)
    return dirpath.is_dir()
