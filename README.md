## 使い方
1. `pip install git+https://github.com/ogihce/progress_bar` でpipからインストール
2. `import progress_bar` と書いてインポートする
3. `bar = progress_bar.ProgressBar(現在値, 最大値)` と書いてインスタンス化する
4. `bar.print(bar.make())` で表示
5. ループの中に、`bar.add(1)`と手順4番を入れて実行する


## サンプルコード
```Python
import progress_bar as pb

progress = pb.ProgressBar(0, 100000)
progress.set_show_percent(pb.Appearance.SHOW_IN_BAR)
progress.set_show_step(pb.Appearance.SHOW_IN_BEFORE_SUFFIX)
progress.set_prefix("Purchasing...")
progress.set_suffix("items")
progress.set_ring_cursor_frequency(1000)
progress.set_show_ring_cursor(pb.Appearance.SHOW_IN_BEFORE_PREFIX)

while progress.current < progress.max:
    progress.add(1)
    progress.print(progress.make())

```


## 依存モジュール
- shutils
- sys
- enum


## Enum
```Python
class Appearance(Enum):
    SHOW_IN_BAR = 1  # バーの中に表示
    SHOW_IN_BEFORE_SUFFIX = 2  # suffixの前に表示
    SHOW_IN_AFTER_SUFFIX = 3  # suffixの後ろに表示
    SHOW_IN_BEFORE_PREFIX = 4  # prefixの前に表示
    SHOW_IN_AFTER_PREFIX = 5  # prefixの後ろに表示
    DONT_SHOW = 6  # 表示しない
```

## メソッド
### `ProgressBar.set_current(int)`
現在値 `ProgressBar.current` を変更する


### `ProgressBar.set_max(int)`
最大値 `ProgressBar.max` を変更する


### `ProgressBar.add(int)`
現在値 `ProgressBar.current` に加算する


### `ProgressBar.set_show_percent(ProgressBar.Appearance)`
パーセンテージの表示位置 `ProgressBar.show_percent` を変更する

`progress_bar.Appearance.DONT_SHOW` を除いて、 `ProgressBar.show_step` と一致していると、`ProgressBar.make()` を実行したときに例外をスローする


### `ProgressBar.set_show_step(ProgressBar.Appearance)`
ステップ（現在値 / 最大値の文字列）の表示位置 `ProgressBar.show_step` を変更する

`progress_bar.Appearance.DONT_SHOW` を除いて、 `ProgressBar.show_percent` と一致していると、`ProgressBar.make()` を実行したときに例外をスローする


### `ProgressBar.set_show_ring_cursor(ProgressBar.Appearance)`
ぐるぐるマークの表示位置 `ProgressBar.show_ring_cursor` を変更する

パーセンテージ、ステップとは違い、以下の3つの値以外を渡すと `progress_bar.InvalidAppearanceError` をスローする

1. `ProgressBar.Appearance.DONT_SHOW`
2. `ProgressBar.Appearance.SHOW_IN_BEFORE_PREFIX`
3. `ProgressBar.Appearance.SHOW_IN_AFTER_SUFFIX`


### `ProgressBar.set_ring_cursor(list)`
ぐるぐるマークに表示する文字のリスト `ProgressBar.ring_cursor` を変更する

各要素はASCII文字1文字で、str型で、要素は最低1つなければならない


### `ProgressBar.set_ring_cursor_frequency(int)`
このモジュールのぐるぐるマークは、時間でぐるぐるするのではなく、現在値の動きに連動しています。

ここで設定したfrequencyあたり、`ProgressBar.ring_cursor` の1要素分進みます。

つまり、frequencyが1000で `ProgressBar.ring_cursor` の要素数が10なら、10000ステップで1周します。


### `ProgressBar.set_ring_cursor_reverse(bool)`
ぐるぐるマークの表示順番を反転させるかどうか `ProgressBar.ring_cursor_reverse` を変更する


### `ProgressBar.set_filled_char(str)`
プログレスバーの、塗りつぶし部分の文字 `ProgressBar.filled_char` を変更する

ASCII文字1文字でなければならない

`ProgressBar.empty_char` と一致していると、`ProgressBar.make()` を実行したときに例外をスローする


### `ProgressBar.set_empty_char(str)`
プログレスバーの、空白部分の文字 `ProgressBar.empty_char` を変更する

ASCII文字1文字でなければならない

`ProgressBar.filled_char` と一致していると、`ProgressBar.make()` を実行したときに例外をスローする


### `ProgressBar.set_prefix(str)`
プログレスバーの前に表示する文字列 `ProgressBar.prefix` を変更する

特に制約は設けていないが、マルチバイト文字を入れた場合コンソールウィンドウの幅に収まらない可能性がある


### `ProgressBar.set_suffix(str)`
プログレスバーの後ろに表示する文字列 `ProgressBar.suffix` を変更する

特に制約は設けていないが、マルチバイト文字を入れた場合コンソールウィンドウの幅に収まらない可能性がある


### `ProgressBar.make()`
設定に従い、プログレスバーの文字列を生成して返す


### `ProgressBar.print(str)`
引数に渡された文字列を、改行せず今のカーソルの行に上書きして表示する


### `TerminalUtils.get_terminal_size()`
コンソールの水平方向の文字数を取得する


### (未使用) `StringUtils.cut(string: str, max_length: int)`
引数として渡された文字列を、引数として渡された整数 `max_length` 文字目までに切り詰める。

文字列の長さが `max_length` を超えている場合、超えていない文字3文字までを削除し、`...` を末尾に追加した文字列を返す

例）`StringUtils.cut("GitHub Thanks", 12)  # GitHub Th...`

文字列の長さが `max_length` を超えていない場合、`max_length` まで半角スペースを補った文字列を返す

例）`StringUtils.cut("GitHub LOVE", 15)  # GitHub LOVE****`  ※便宜上半角スペースをアスタリスクで表している


## 初期値
```Python
self.current = current  # インスタンス引数
self.max = max  # インスタンス引数
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
```


## カスタム例外一覧
### 基底クラス `progress_bar.ProgressBarException`
すべてのカスタム例外の基底クラスです


### `progress_bar.CannotInstantiateError`
インスタンス化を想定していないクラスをインスタンス化したときにスローされます


### `progress_bar.MissingArgumentError`
引数が不足している場合にスローされます


### `progress_bar.ArgumentTypeError`
引数の型が不正な場合にスローされます


### `progress_bar.InvalidAppearanceError`
無効な表示位置が渡された場合にスローされます


### `progress_bar.InvalidArgumentsError`
無効な引数が渡された場合にスローされます


### `progress_bar.InvalidCharacterError`
無効な文字が渡された場合にスローされます


### `progress_bar.InvalidProgressError`
100%を超えるなど、無効な値になった場合にスローされます

### `progress_bar.InvalidValueError`
無効な値を検出した場合にスローされます
