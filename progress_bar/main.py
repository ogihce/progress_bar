import shutil
import sys

def get_terminal_size():
    """
    端末のサイズを取得する。

    Returns
    -------
    size.columns : int
        端末の横幅
    """
    size = shutil.get_terminal_size()
    return size.columns

def make(current, max, **kwargs):
    """
    与えられた引数からプログレスバーを作成する。

    Parameters
    ----------
    current : int
        現在の値
    max : int
        最大値
    show_percent : bool, optional
        パーセントを表示するかどうか
    showstep : bool, optional
        現在の値と最大値を表示するかどうか
    filled_char : str, optional
        バーの塗りつぶしに使う文字
    empty_char : str, optional
        バーの空白に使う文字
    prefix : str, optional
        バーの前に表示する文字
    suffix : str, optional
        バー、パーセンテージ、現在の値と最大値の後に表示する文字列
    bar_length : int, optional
        バーの長さ

    Returns
    -------
    bar : str
        プログレスバー

    Raises
    ------
    ValueError
        show_percent, showstep, filled_char, empty_char, prefix, bar_length のいずれかが不正な値の場合
    """
    if kwargs.get('show_percent') is None:
        show_percent = True
    else:
        try:
            show_percent = bool(kwargs.get('show_percent'))
        except ValueError:
            raise ValueError('show_percent must be a boolean or can be converted to a boolean')
    if kwargs.get('showstep') is None:
        showstep = False
    else:
        try:
            showstep = bool(kwargs.get('showstep'))
        except ValueError:
            raise ValueError('showstep must be a boolean or can be converted to a boolean')
    if kwargs.get('filled_char') is None:
        filled_char = '█'
    else:
        try:
            filled_char = str(kwargs.get('filled_char'))
        except ValueError:
            raise ValueError('filled_char must be a string or can be converted to a string')
    if kwargs.get('empty_char') is None:
        empty_char = ' '
    else:
        try:
            empty_char = str(kwargs.get('empty_char'))
        except ValueError:
            raise ValueError('empty_char must be a string or can be converted to a string')
    if kwargs.get('prefix') is None:
        prefix = ''
    else:
        try:
            prefix = str(kwargs.get('prefix'))
        except ValueError:
            raise ValueError('prefix must be a string or can be converted to a string')
    if kwargs.get('suffix') is None:
        suffix = ''
    else:
        try:
            suffix = str(kwargs.get('suffix'))
        except ValueError:
            raise ValueError('suffix must be a string or can be converted to a string')
    if kwargs.get('bar_length') is None:
        bar_length = get_terminal_size() - len(prefix) - len(suffix) - 4
        if show_percent:
            bar_length -= (7 + 1)
        if showstep:
            bar_length -= (len(str(max)) * 2 + 3 + 2 + 1)
    else:
        try:
            bar_length = int(kwargs.get('bar_length'))
        except ValueError:
            raise ValueError('bar_length must be an integer or can be converted to an integer')
        
    percentage = round(current / max * 100, 2)
    filled_length = int(bar_length * current / max)
    bar = "[" + filled_char * filled_length + empty_char * (bar_length - filled_length) + "]"
    if prefix != '':
        bar = f'{prefix}{bar}'
    if show_percent:
        bar = f'{bar} {percentage:6.2f}%'
    if showstep:
        bar = f'{bar} ({str(current).rjust(len(str(max)))} / {max})'
    if suffix != '':
        bar = f'{bar} {suffix}'

    return bar

def print(string: str):
    """
    プログレスバーを表示する。

    Parameters
    ----------
    string : str
        表示する文字列
    """
    sys.stdout.write(f'\r{string}')
    sys.stdout.flush()

def cut(string, max_length):
    """
    文字列を指定した長さに切り詰める。

    Parameters
    ----------
    string : str
        切り詰める文字列
    max_length : int
        文字列の最大長
    
    Returns
    -------
    string : str
        切り詰めた文字列
    """
    if len(string) > max_length:
        return string[:max_length - 3] + '...'
    else:
        return string.ljust(max_length)