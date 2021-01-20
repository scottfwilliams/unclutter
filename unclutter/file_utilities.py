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
