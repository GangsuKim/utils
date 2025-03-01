# Copyright (c) 2025 Gangsu Kim
# Licensed under The MIT License [see LICENSE for details]

from pickle import Unpickler

import os
from tqdm import tqdm

__all__ = ["load_pickle"]

'''
Original code from humanize lib.
https://github.com/python-humanize/humanize

modified for simplified
'''
suffix = ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

def readable_size(
        value,
        fmt: str = "%.2f",
) -> (str, str):

    base = 1000
    bytes_ = float(value)
    abs_bytes = abs(bytes_)

    if abs_bytes < base:
        return str(bytes_), 'B'

    unit, s = None, None
    for i, s in enumerate(suffix):
        unit = base ** (i + 2)

        if abs_bytes < unit:
            break

    ret = fmt % (base * bytes_ / unit)
    return ret, s

'''
Original code by technomage at stackoverflow.
https://stackoverflow.com/a/62236766

Modified for file size conversion.
'''
class TQDMBytesReader(object):
    def __init__(self, fd, total, **kwargs):
        self.fd = fd
        self.total = readable_size(total)[0]
        self.unit = readable_size(total)[1].strip()
        self.load_state = 0

        self.tqdm = tqdm(total=total, bar_format='{l_bar}{bar}| {unit} [{elapsed}<{remaining}]',unit=f'0.00/{self.total}{self.unit}', **kwargs)

        self._rank_map = {}
        for i, _s in enumerate(suffix):
            self._rank_map[_s] = i

    def read(self, size=-1):
        bytes = self.fd.read(size)
        self.load_state += len(bytes)
        self.tqdm.unit = f'{self._get_local_size()}/{self.total}{self.unit}'
        self.tqdm.update(len(bytes))
        return bytes

    def readline(self):
        bytes = self.fd.readline()
        self.load_state += len(bytes)
        self.tqdm.unit = f'{self._get_local_size()}/{self.total}{self.unit}'
        self.tqdm.update(len(bytes))
        return bytes

    def __enter__(self):
        self.tqdm.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        return self.tqdm.__exit__(*args, **kwargs)

    def _get_local_size(self):
        _current = readable_size(self.load_state)
        _current_unit = _current[1].strip()
        _current_size = float(_current[0].strip())

        if _current_unit == 'B':
            return str(0.00)

        # Get rank
        _global = self._rank_map[self.unit]
        _local = self._rank_map[_current_unit]

        if _global == _local:
            return "%.2f" % _current_size

        _rank_distance = _global - _local
        _current_size /= (1024 ** _rank_distance)
        _current_size = "%.2f" % _current_size
        return _current_size


def load_pickle(
        path_to_file: str,
        desc: str = None
):
    """
    Load pickle file with tqdm bar
    :param path_to_file: file path to pickle file
    :param desc: description of tqdm bar
    :return: loaded data
    """

    if desc is None:
        desc = 'Loading pickle'

    with open(path_to_file, 'rb') as f:
        total = os.path.getsize(path_to_file)
        with TQDMBytesReader(f, total=total, desc=desc) as pbfd:
            up = Unpickler(pbfd)
            data = up.load()

    return data

if __name__ == '__main__':
    dummy = load_pickle('path_to_pickle_file/pickle.pkl', 'My pickle')