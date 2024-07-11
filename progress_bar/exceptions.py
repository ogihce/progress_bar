class ProgressBarException(Exception):
    pass

class CannotInstantiateError(ProgressBarException):
    """インスタンス化できないことを表す"""
    def __init__(self, message="This class cannot be instantiated."):
        super().__init__(message)

class MissingArgumentError(ProgressBarException):
    """不足している引数によるエラー"""
    def __init__(self, message="Missing required argument"):
        super().__init__(message)

class ArgumentTypeError(ProgressBarException):
    """引数の型が不正な場合のエラー"""
    def __init__(self, message="Argument type is incorrect"):
        super().__init__(message)

class InvalidArgumentsError(ProgressBarException):
    """無効な引数によるエラーを表す"""
    def __init__(self, message="Invalid arguments provided"):
        super().__init__(message)

class InvalidAppearanceError(ProgressBarException):
    """無効な表示位置を表す"""
    def __init__(self, message="Invalid appearance provided"):
        super().__init__(message)

class InvalidCharacterError(ProgressBarException):
    """無効な文字を表す"""
    def __init__(self, message="Invalid character provided"):
        super().__init__(message)

class InvalidProgressError(ProgressBarException):
    """無効な進捗状況を表す"""
    def __init__(self, message="Invalid progress provided"):
        super().__init__(message)

class InvalidSizeError(ProgressBarException):
    """無効なサイズを表す"""
    def __init__(self, message="Invalid size provided"):
        super().__init__(message)

class InvalidValueError(ProgressBarException):
    """無効な値を表す"""
    def __init__(self, message="Invalid value provided"):
        super().__init__(message)