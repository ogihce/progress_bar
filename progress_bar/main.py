import shutil
import sys
from enum import Enum

class Percent(Enum):
    SHOW_IN_BAR = 1
    SHOW_IN_BEFORE_SUFFIX = 2
    SHOW_IN_AFTER_SUFFIX = 3
    SHOW_IN_BEFORE_PREFIX = 4
    SHOW_IN_AFTER_PREFIX = 5
    DONT_SHOW = 6

class Step(Enum):
    SHOW_IN_BAR = 1
    SHOW_IN_BEFORE_SUFFIX = 2
    SHOW_IN_AFTER_SUFFIX = 3
    SHOW_IN_BEFORE_PREFIX = 4
    SHOW_IN_AFTER_PREFIX = 5
    DONT_SHOW = 6

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
    show_percent : Enum, optional
        パーセンテージの表示方法
        progress_bar.Percent.SHOW_IN_BAR: バーの中に表示 (ステップと同時に表示することはできない)
        progress_bar.Percent.SHOW_IN_BEFORE_PREFIX: prefixの前に表示
        progress_bar.Percent.SHOW_IN_AFTER_PREFIX: prefixの後に表示
        progress_bar.Percent.SHOW_IN_BEFORE_SUFFIX: suffixの前に表示 (デフォルト)
        progress_bar.Percent.SHOW_IN_AFTER_SUFFIX: suffixの後に表示
        progress_bar.Percent.DONT_SHOW: 表示しない
    showstep : Enum, optional
        ステップの表示方法
        progress_bar.Step.SHOW_IN_BAR: バーの中に表示 (パーセンテージと同時に表示することはできない)
        progress_bar.Step.SHOW_IN_BEFORE_PREFIX: prefixの前に表示
        progress_bar.Step.SHOW_IN_AFTER_PREFIX: prefixの後に表示
        progress_bar.Step.SHOW_IN_BEFORE_SUFFIX: suffixの前に表示
        progress_bar.Step.SHOW_IN_AFTER_SUFFIX: suffixの後に表示
        progress_bar.Step.DONT_SHOW: 表示しない (デフォルト)
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
    bar_ratio : float, optional
        バーの長さを最大値の何倍にするか
        (bar_length と bar_ratio の両方が指定された場合は bar_length を優先する)

    Returns
    -------
    bar : str
        プログレスバー

    Raises
    ------
    ValueError
        show_percent, showstep, filled_char, empty_char, prefix, bar_length のいずれかが不正な値の場合
    """
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
    if kwargs.get('bar_ratio') is None:
        bar_ratio = 1
    else:    
        try:
            bar_ratio = float(kwargs.get('bar_ratio'))
            if bar_ratio <= 0:
                raise ValueError('bar_ratio must be greater than 0')
            elif bar_ratio > 1:
                raise ValueError('bar_ratio must be less than or equal to 1')
        except ValueError:
            raise ValueError('bar_ratio must be a float or can be converted to a float')
    if kwargs.get('bar_length') is None:
        bar_length = int(get_terminal_size() * bar_ratio) - 2
        if bar_length < 5:
            raise ValueError(f'bar_length must be greater than or equal to 5 but bar_length is {bar_length}')
    else:
        try:
            bar_length = int(kwargs.get('bar_length'))
        except ValueError:
            raise ValueError('bar_length must be an integer or can be converted to an integer')

    # バーの長さを計算
    # バーの前後に表示する文字列の長さを考慮する
    bar_length -= len(prefix) + 1 + len(suffix) + 1
    # パーセンテージをバー以外に表示する場合は8文字分のスペースを確保する
    if kwargs.get('show_percent') is not None and Percent(kwargs.get('show_percent')) != Percent.DONT_SHOW and Percent(kwargs.get('show_percent')) != Percent.SHOW_IN_BAR:
        bar_length -= 8
    # バーに出す場合は2文字分のスペースを確保する
    elif kwargs.get('show_percent') is not None and Percent(kwargs.get('show_percent')) == Percent.SHOW_IN_BAR:
        bar_length -= 2
    # ステップをバー以外に表示する場合は最大値の桁数 * 2 + 3 + 1分のスペースを確保する
    if kwargs.get('showstep') is not None and Step(kwargs.get('showstep')) != Step.DONT_SHOW and Step(kwargs.get('showstep')) != Step.SHOW_IN_BAR:
        bar_length -= len(str(max)) * 2 + 3 + 1
    # バーに出す場合は2文字分のスペースを確保する
    elif kwargs.get('showstep') is not None and Step(kwargs.get('showstep')) == Step.SHOW_IN_BAR:
        bar_length -= 2

    # バーの長さが5以下の場合はエラーを出す
    if bar_length < 5:
        raise ValueError(f'bar_length must be greater than or equal to 5 but bar_length is {bar_length}')

    # パーセンテージの表示方法を取得
    if kwargs.get('show_percent') is None:
        show_percent = Percent.SHOW_IN_BAR
    else:
        try:
            show_percent = Percent(kwargs.get('show_percent'))
        except ValueError:
            raise ValueError('show_percent must be an instance of Percent')
    
    # ステップの表示方法を取得
    if kwargs.get('showstep') is None:
        showstep = Step.DONT_SHOW
    else:
        try:
            showstep = Step(kwargs.get('showstep'))
        except ValueError:
            raise ValueError('showstep must be an instance of Step')
        
    # パーセンテージもステップもバーに表示することはできない
    if show_percent == Percent.SHOW_IN_BAR and showstep == Step.SHOW_IN_BAR:
        raise ValueError('show_percent and showstep cannot be shown in the bar at the same time')
        
    # バーの作成
    # パーセンテージを表示する場合
    if show_percent == Percent.SHOW_IN_BAR:
        filled = int(bar_length * current / max)
        empty = bar_length - filled
        percentage_position = int(bar_length * 0.5) - 3
        percentage_str = f' {round(current / max * 100, 2):6.2f}% '
        bar = f'[{filled_char * filled}{empty_char * empty}]'
        bar = bar[:percentage_position] + percentage_str + bar[percentage_position + 6:]

    # ステップを表示する場合
    elif showstep == Step.SHOW_IN_BAR:
        filled = int(bar_length * current / max)
        empty = bar_length - filled
        step_str = f' {str(current).rjust(len(str(max)))} / {max} '
        step_position = int(bar_length * 0.5) - int(len(step_str) * 0.5)
        bar = f'[{filled_char * filled}{empty_char * empty}]'
        bar = bar[:step_position] + step_str + bar[step_position + len(step_str) - 1:]

    # なにも表示しない場合
    else:
        filled = int(bar_length * current / max)
        empty = bar_length - filled
        bar = f'[{filled_char * filled}{empty_char * empty}]'

    before_bar = ""
    after_bar = ""
    # バーの前に表示する文字列
    # prefixの前にパーセンテージを表示する場合
    if show_percent == Percent.SHOW_IN_BEFORE_PREFIX:
        before_bar += f'{round(current / max * 100, 2):6.2f}% '
    # prefixの前にステップを表示する場合
    if showstep == Step.SHOW_IN_BEFORE_PREFIX:
        before_bar += f'{str(current).rjust(len(str(max)))} / {max} '

    if prefix != '':
        before_bar += f'{prefix} '

    # prefixの後にパーセンテージを表示する場合
    if show_percent == Percent.SHOW_IN_AFTER_PREFIX:
        before_bar += f'{round(current / max * 100, 2):6.2f}% '
    # prefixの後にステップを表示する場合
    if showstep == Step.SHOW_IN_AFTER_PREFIX:
        before_bar += f'{str(current).rjust(len(str(max)))} / {max} '

    # バーの後に表示する文字列
    # suffixの前にパーセンテージを表示する場合
    if show_percent == Percent.SHOW_IN_BEFORE_SUFFIX:
        after_bar += f' {round(current / max * 100, 2):6.2f}%'
    # suffixの前にステップを表示する場合
    if showstep == Step.SHOW_IN_BEFORE_SUFFIX:
        after_bar += f' {str(current).rjust(len(str(max)))} / {max}'

    if suffix != '':
        after_bar += f' {suffix}'

    # suffixの後にパーセンテージを表示する場合
    if show_percent == Percent.SHOW_IN_AFTER_SUFFIX:
        after_bar += f' {round(current / max * 100, 2):6.2f}% '

    # suffixの後にステップを表示する場合
    if showstep == Step.SHOW_IN_AFTER_SUFFIX:
        after_bar += f' {str(current).rjust(len(str(max)))} / {max}'

    bar = before_bar + bar + after_bar

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