import sys


_exclude_common = [".git"]
_exclude_aix = []
_exclude_cygwin = []
_exclude_darwin = [".DS_Store", "._.Trashes"]
_exclude_linux = []
_exclude_win32 = []

_system_excludes_dict = {
    "aix" : _exclude_aix,
    "cygwin" : _exclude_cygwin,
    "darwin" : _exclude_darwin,
    "linux" : _exclude_linux,
    "win32" : _exclude_win32
}

_platform = sys.platform
_exclude_list = list()
_exclude_list.extend(_exclude_common)
_exclude_list.extend(_system_excludes_dict[_platform])
