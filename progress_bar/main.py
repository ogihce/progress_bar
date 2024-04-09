import shutil
import sys
from enum import Enum

class Appearance(Enum):
    SHOW_IN_BAR = 1
    SHOW_IN_BEFORE_SUFFIX = 2
    SHOW_IN_AFTER_SUFFIX = 3
    SHOW_IN_BEFORE_PREFIX = 4
    SHOW_IN_AFTER_PREFIX = 5
    DONT_SHOW = 6

class Progress:

    def __init__(self, current, max):
        self.current = current
        self.max = max
        self.show_percent = Appearance.SHOW_IN_BEFORE_SUFFIX
        self.showstep = Appearance.DONT_SHOW
        self.filled_char = '█'
        self.empty_char = ' '
        self.prefix = ''
        self.suffix = ''

    def set_current(self, current: int):
        self.current = current

    def set_max(self, max: int):
        self.max = max

    def add_current(self, add: int):
        self.current += add
    
    def set_show_percent(self, show_percent: Appearance):
        self.show_percent = show_percent
    
    def set_showstep(self, showstep: Appearance):
        self.showstep = showstep
    
    def set_filled_char(self, filled_char: str):
        self.filled_char = filled_char
    
    def set_empty_char(self, empty_char: str):
        self.empty_char = empty_char

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def set_suffix(self, suffix: str):
        self.suffix = suffix

    def get_terminal_size(self):
        """
        端末のサイズを取得する。

        Returns
        -------
        size.columns : int
            端末の横幅
        """
        size = shutil.get_terminal_size()
        return size.columns

    def make(self, **kwargs):
        """
        与えられた引数からプログレスバーを作成する。

        Parameters
        ----------
        bar_length : int, optional
            バーの長さ
        bar_ratio : float, optional
            バーの長さを最大値の何倍にするか
            (bar_length と bar_ratio の両方が指定された場合は bar_length を優先)

        Returns
        -------
        bar : str
            プログレスバー

        Raises
        ------
        ValueError
            show_percent, showstep, filled_char, empty_char, prefix, bar_length のいずれかが不正な値の場合
        """

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
            bar_length = int(self.get_terminal_size() * bar_ratio) - 2
            if bar_length < 5:
                raise ValueError(f'bar_length must be greater than or equal to 5 but bar_length is {bar_length}')
        else:
            try:
                bar_length = int(kwargs.get('bar_length'))
            except ValueError:
                raise ValueError('bar_length must be an integer or can be converted to an integer')

        # バーの長さを計算
        # バーの前後に表示する文字列の長さを考慮する
        bar_length -= len(self.prefix) + 1 + len(self.suffix) + 1
        # パーセンテージをバー以外に表示する場合は8文字分のスペースを確保する
        if self.show_percent is not None and Appearance(self.show_percent) != Appearance.DONT_SHOW and Appearance(self.show_percent) != Appearance.SHOW_IN_BAR:
            bar_length -= 8
        # バーに出す場合は2文字分のスペースを確保する
        elif self.show_percent is not None and Appearance(self.show_percent) == Appearance.SHOW_IN_BAR:
            bar_length -= 2
        # ステップをバー以外に表示する場合は最大値の桁数 * 2 + 3 + 1分のスペースを確保する
        if self.showstep is not None and Appearance(self.showstep) != Appearance.DONT_SHOW and Appearance(self.showstep) != Appearance.SHOW_IN_BAR:
            bar_length -= len(str(max)) * 2 + 3 + 1
        # バーに出す場合は2文字分のスペースを確保する
        elif self.showstep is not None and Appearance(self.showstep) == Appearance.SHOW_IN_BAR:
            bar_length -= 2

        # バーの長さが5以下の場合はエラーを出す
        if bar_length < 5:
            raise ValueError(f'bar_length must be greater than or equal to 5 but bar_length is {bar_length}')
            
        # パーセンテージもステップもバーに表示することはできない
        if self.show_percent == Appearance.SHOW_IN_BAR and self.showstep == Appearance.SHOW_IN_BAR:
            raise ValueError('show_percent and showstep cannot be shown in the bar at the same time')
            
        # バーの作成
        # パーセンテージを表示する場合
        if self.show_percent == Appearance.SHOW_IN_BAR:
            filled = int(bar_length * self.current / self.max)
            empty = bar_length - filled
            percentage_position = int(bar_length * 0.5) - 3
            percentage_str = f' {round(self.current / self.max * 100, 2):6.2f}% '
            bar = f'[{self.filled_char * filled}{self.empty_char * empty}]'
            bar = bar[:percentage_position] + percentage_str + bar[percentage_position + 6:]

        # ステップを表示する場合
        elif self.showstep == Appearance.SHOW_IN_BAR:
            filled = int(bar_length * self.current / self.max)
            empty = bar_length - filled
            step_str = f' {str(self.current).rjust(len(str(self.max)))} / {self.max} '
            step_position = int(bar_length * 0.5) - int(len(step_str) * 0.5)
            bar = f'[{self.filled_char * filled}{self.empty_char * empty}]'
            bar = bar[:step_position] + step_str + bar[step_position + len(step_str) - 1:]

        # なにも表示しない場合
        else:
            filled = int(bar_length * self.current / self.max)
            empty = bar_length - filled
            bar = f'[{self.filled_char * filled}{self.empty_char * empty}]'

        before_bar = ""
        after_bar = ""
        # バーの前に表示する文字列
        # prefixの前にパーセンテージを表示する場合
        if self.show_percent == Appearance.SHOW_IN_BEFORE_PREFIX:
            before_bar += f'{round(self.current / self.max * 100, 2):6.2f}% '
        # prefixの前にステップを表示する場合
        if self.showstep == Appearance.SHOW_IN_BEFORE_PREFIX:
            before_bar += f'{str(self.current).rjust(len(str(self.max)))} / {self.max} '

        if self.prefix != '':
            before_bar += f'{self.prefix} '

        # prefixの後にパーセンテージを表示する場合
        if self.show_percent == Appearance.SHOW_IN_AFTER_PREFIX:
            before_bar += f'{round(self.current / self.max * 100, 2):6.2f}% '
        # prefixの後にステップを表示する場合
        if self.showstep == Appearance.SHOW_IN_AFTER_PREFIX:
            before_bar += f'{str(self.current).rjust(len(str(self.max)))} / {self.max} '

        # バーの後に表示する文字列
        # suffixの前にパーセンテージを表示する場合
        if self.show_percent == Appearance.SHOW_IN_BEFORE_SUFFIX:
            after_bar += f' {round(self.current / self.max * 100, 2):6.2f}%'
        # suffixの前にステップを表示する場合
        if self.showstep == Appearance.SHOW_IN_BEFORE_SUFFIX:
            after_bar += f' {str(self.current).rjust(len(str(self.max)))} / {self.max}'

        if self.suffix != '':
            after_bar += f' {self.suffix}'

        # suffixの後にパーセンテージを表示する場合
        if self.show_percent == Appearance.SHOW_IN_AFTER_SUFFIX:
            after_bar += f' {round(self.current / max * 100, 2):6.2f}% '

        # suffixの後にステップを表示する場合
        if self.showstep == Appearance.SHOW_IN_AFTER_SUFFIX:
            after_bar += f' {str(self.current).rjust(len(str(self.max)))} / {self.max}'

        bar = before_bar + bar + after_bar

        return bar

    def print(self, string: str):
        """
        プログレスバーを表示する。

        Parameters
        ----------
        string : str
            表示する文字列
        """
        sys.stdout.write(f'\r{string}')
        sys.stdout.flush()

    def cut(self, string, max_length):
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