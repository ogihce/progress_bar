import shutil
import sys
from enum import Enum

from .exceptions import *

class TerminalUtils:
    def __init__(self):
        raise CannotInstantiateError('This class cannot be instantiated.')

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
    

class StringUtils:
    def __init__(self):
        raise CannotInstantiateError('This class cannot be instantiated.')
    
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


class Appearance(Enum):
    SHOW_IN_BAR = 1
    SHOW_IN_BEFORE_SUFFIX = 2
    SHOW_IN_AFTER_SUFFIX = 3
    SHOW_IN_BEFORE_PREFIX = 4
    SHOW_IN_AFTER_PREFIX = 5
    DONT_SHOW = 6


class ProgressBar:
    def __init__(self, current, max):
        if current is None or max is None:
            raise MissingArgumentError('Current progress and max progress must be provided.')

        if not isinstance(current, int):
            raise ArgumentTypeError('Current progress must be an integer.')
        if not isinstance(max, int):
            raise ArgumentTypeError('Max progress must be an integer.')
        if current > max:
            raise InvalidProgressError('Current progress must be less than or equal to max progress.')
        if current < 0:
            raise InvalidProgressError('Current progress must be greater than or equal to 0.')
        if max < 0:
            raise InvalidProgressError('Max progress must be greater than or equal to 0.')
        if max == 0:
            raise InvalidProgressError('Max progress must be greater than 0.')

        self.current = current
        self.max = max
        self.show_percent = Appearance.SHOW_IN_BEFORE_SUFFIX
        self.show_step = Appearance.DONT_SHOW
        self.filled_char = '█'
        self.empty_char = ' '
        self.prefix = ''
        self.suffix = ''
        self.ring_cursor = ["/", "-", "\\", "|"]
        self.ring_cursor_frequency = 100
        self.show_ring_cursor = Appearance.DONT_SHOW
        self.ring_cursor_reverse = False

    def set_current(self, current: int):
        self.current = current

    def set_max(self, max: int):
        self.max = max

    def add(self, add: int):
        self.current += add
    
    def set_show_percent(self, show_percent: Appearance):
        self.show_percent = show_percent
    
    def set_show_step(self, show_step: Appearance):
        self.show_step = show_step

    def set_show_ring_cursor(self, show_ring_cursor: Appearance):
        if show_ring_cursor != Appearance.DONT_SHOW and show_ring_cursor != Appearance.SHOW_IN_BEFORE_PREFIX and show_ring_cursor != Appearance.SHOW_IN_AFTER_SUFFIX:
            raise InvalidAppearanceError('show_ring_cursor must be DONT_SHOW, SHOW_IN_BEFORE_PREFIX, or SHOW_IN_AFTER_SUFFIX.')
        self.show_ring_cursor = show_ring_cursor
    
    def set_ring_cursor(self, ring_cursor: list):
        if not all(isinstance(i, str) for i in ring_cursor):
            raise InvalidValueError('All elements in ring_cursor must be strings.')
        if not all(i.isascii() for i in ring_cursor):
            raise InvalidCharacterError('All elements in ring_cursor must be ASCII characters.')
        if not all(len(i) == 1 for i in ring_cursor):
            raise InvalidValueError('All elements in ring_cursor must be single characters.')
        if len(ring_cursor) == 0:
            raise InvalidValueError('ring_cursor must have at least one element.')
        
        self.ring_cursor = ring_cursor
    
    def set_ring_cursor_frequency(self, ring_cursor_frequency: int):
        if ring_cursor_frequency <= 0:
            raise InvalidValueError('ring_cursor_frequency must be greater than 0.')
        
        self.ring_cursor_frequency = ring_cursor_frequency

    def set_ring_cursor_reverse(self, ring_cursor_reverse: bool):
        self.ring_cursor_reverse = ring_cursor_reverse
    
    def set_filled_char(self, filled_char: str):
        if not filled_char.isascii():
            raise InvalidCharacterError('Filled character must be an ASCII character.')
        if len(filled_char) != 1:
            raise InvalidCharacterError('Filled character must be a single character.')
        
        self.filled_char = filled_char
    
    def set_empty_char(self, empty_char: str):
        if not empty_char.isascii():
            raise InvalidCharacterError('Empty character must be an ASCII character.')
        if len(empty_char) != 1:
            raise InvalidCharacterError('Empty character must be a single character.')
        
        self.empty_char = empty_char

    def set_prefix(self, prefix: str):
        if not prefix.isascii():
            raise InvalidCharacterError('Prefix must be an ASCII character.')
        
        self.prefix = prefix

    def set_suffix(self, suffix: str):
        if not suffix.isascii():
            raise InvalidCharacterError('Suffix must be an ASCII character.')
        
        self.suffix = suffix

    def make(self):
        """
        プログレスバーを生成する。
        
        Returns
        -------
        bar : str
            生成したプログレスバー
        """

        # validation
        if self.show_percent != Appearance.DONT_SHOW and self.show_step != Appearance.DONT_SHOW and self.show_percent == self.show_step:
            raise InvalidAppearanceError("show_percent and show_step cannot be the same.")
        
        if self.filled_char == self.empty_char:
            raise InvalidCharacterError("filled_char and empty_char cannot be the same.")

        # generate before_bar and after_bar
        percent = self.current / self.max * 100

        before_bar = ""
        after_bar = ""

        if self.show_ring_cursor == Appearance.SHOW_IN_BEFORE_PREFIX and self.current != self.max:
            if self.ring_cursor_reverse:
                before_bar += list(reversed(self.ring_cursor))[(self.current // self.ring_cursor_frequency) % len(self.ring_cursor)] + " "
            else:
                before_bar += self.ring_cursor[(self.current // self.ring_cursor_frequency) % len(self.ring_cursor)] + " "

        if self.show_step == Appearance.SHOW_IN_BEFORE_PREFIX:
            before_bar += f"{str(self.current).rjust(len(str(self.max)))} / {self.max} "
        if self.show_percent == Appearance.SHOW_IN_BEFORE_PREFIX:
            before_bar += f"{percent:3.2f}% "

        before_bar += self.prefix

        if self.show_step == Appearance.SHOW_IN_AFTER_PREFIX:
            before_bar += f" {str(self.current).rjust(len(str(self.max)))} / {self.max}"
        if self.show_percent == Appearance.SHOW_IN_AFTER_PREFIX:
            before_bar += f" {percent:3.2f}%"
        
        
        if self.show_step == Appearance.SHOW_IN_BEFORE_SUFFIX:
            after_bar += f"{str(self.current).rjust(len(str(self.max)))} / {self.max} "
        if self.show_percent == Appearance.SHOW_IN_BEFORE_SUFFIX:
            after_bar += f"{percent:3.2f}% "

        after_bar += self.suffix

        if self.show_step == Appearance.SHOW_IN_AFTER_SUFFIX:
            after_bar += f" {str(self.current).rjust(len(str(self.max)))} / {self.max}"
        if self.show_percent == Appearance.SHOW_IN_AFTER_SUFFIX:
            after_bar += f" {percent:3.2f}%"

        if self.show_ring_cursor == Appearance.SHOW_IN_AFTER_SUFFIX and self.current != self.max:
            after_bar += " " + self.ring_cursor[(self.current // self.ring_cursor_frequency) % len(self.ring_cursor)]

        if before_bar != "":
            before_bar += " "

        if after_bar != "":
            after_bar = " " + after_bar
        
        bar_length = TerminalUtils.get_terminal_size(self) - len(before_bar) - len(after_bar) - 2

        filled_length = int(bar_length * self.current / self.max)
        empty_length = bar_length - filled_length

        bar = f"[{self.filled_char * filled_length}{self.empty_char * empty_length}]"

        if self.show_step == Appearance.SHOW_IN_BAR:
            str_in_bar = f" {self.current.rjust(len(str(self.max)))} / {self.max} "
            replace_start_index = (bar_length - len(str_in_bar)) // 2
            bar = bar[:replace_start_index] + str_in_bar + bar[replace_start_index + len(str_in_bar):]
        if self.show_percent == Appearance.SHOW_IN_BAR:
            str_in_bar = f" {percent:3.2f}% "
            replace_start_index = (bar_length - len(str_in_bar)) // 2
            bar = bar[:replace_start_index] + str_in_bar + bar[replace_start_index + len(str_in_bar):]       

        return before_bar + bar + after_bar 

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
