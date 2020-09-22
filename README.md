# osu-Music-Copier
osu!の譜面フォルダーから音楽ファイル等をコピーするPythonスクリプトです。

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ReNeeter/osu-Music-Copier)](https://github.com/ReNeeter/osu-Music-Copier/releases/latest)
[![GitHub All Releases](https://img.shields.io/github/downloads/ReNeeter/osu-Music-Copier/total)](https://github.com/ReNeeter/osu-Music-Copier/releases)

## 使い方
Windowsの方は[リリースページ](https://github.com/ReNeeter/osu-Music-Copier/releases/latest)からビルド済みバイナリをダウンロードできます。  
Mac、Linuxの方は[Pythonスクリプト](osu-Music-Copier.py)をダウンロードして実行してください。

第1引数にosu!の譜面フォルダーのパスを、第2引数にファイルのコピー先のパスを入力して実行してください。

## 例
```bat
osu-Music-Copier.exe %LOCALAPPDATA%\osu!\Songs %USERPROFILE%\Music
```

## Todo
- [ ] 譜面からMP3ファイルを読み込み
- [ ] カバーアートもコピー・合成を可能に
- [ ] オプションを追加