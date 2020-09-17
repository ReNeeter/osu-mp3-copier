# osu-MP3-Copier
osu!の譜面フォルダからMP3ファイル等をコピーするPythonスクリプトです。

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ReNeeter/osu-MP3-Copier)](https://github.com/ReNeeter/osu-MP3-Copier/releases/latest)
[![GitHub All Releases](https://img.shields.io/github/downloads/ReNeeter/osu-MP3-Copier/total)](https://github.com/ReNeeter/osu-MP3-Copier/releases)

## 使い方
Windowsの方は[リリースページ](https://github.com/ReNeeter/osu-MP3-Copier/releases/latest)からビルド済みバイナリをダウンロード出来ます。  
Mac、Linuxの方は[Pythonスクリプト](osu-MP3-Copier.py)をダウンロードして実行してください。

第1引数にosu!の譜面フォルダのパスを、第2引数にファイルのコピー先のパスを入力して実行してください。

## 例
```bat
osu-MP3-Copier.exe %LOCALAPPDATA%\osu!\Songs %USERPROFILE%\Music
```

## Todo
- [ ] 譜面からMP3ファイルを読み込み
- [ ] カバーアートもコピー・合成を可能に
- [ ] オプションを追加