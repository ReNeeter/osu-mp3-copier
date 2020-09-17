# osu-mp3-copier
osu!のSongsフォルダに有るMP3ファイルを正しくコピーするPythonスクリプトです。

## 使い方
Windowsの方は[リリースページ](https://github.com/ReNeeter/osu-mp3-copier/releases)からビルド済みバイナリをダウンロード出来ます。  
Mac、Linuxの方は[Pythonスクリプト](osu-mp3-copier.py)をダウンロードして実行してください。

第1引数にosu!のインストールフォルダのパス(通常は「C:\Users\[ユーザー名]\AppData\Local\osu!」にあります)を、第2引数にMP3のコピー先のパスを入力して実行してください。

### 例
```bat
osu-mp3-copier.exe C:\Users\renee\AppData\Local\osu! C:\Users\renee\Music
```

## 仕様
一旦osu!のSongsフォルダからコピー先のフォルダにコピーしてから、ファイル名から先頭にある番号や「[no video]」を削除しています。  
ちなみにコピー時はコピーするMP3の直上のディレクトリ名にリネームしてコピーしています。  
(ファイル名が重複するのを防ぐのと、MP3Tag等のソフトでタグをつけやすくするため)  
リネーム時にファイル名が重複した物は「(1)」や「(2)」をファイル名の末尾に付けています。