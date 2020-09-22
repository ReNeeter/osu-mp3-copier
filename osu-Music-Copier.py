import glob
import os
import re
import shutil
import sys

# ソフトの詳細を表示
print('osu-Music-Copier ver.0.4')
print('作者:ReNeeter\n')

# 引数の判定
if len(sys.argv) == 1:
    print('-----使い方-----')
    print('第1引数にosu!の譜面フォルダーのパスを、第2引数にファイルのコピー先のパスを入力して実行してください。\n')
    print('-----例-----')
    print(r'osu-Music-Copier.exe %LOCALAPPDATA%\osu!\Songs %USERPROFILE%\Music')
    sys.exit(0)
elif len(sys.argv) != 3:
    print('引数が正しく指定されていません。')
    sys.exit(1)

# パス
osuSongsPath = os.path.expandvars(sys.argv[1].strip("'"'"'))
copyPath = os.path.expandvars(sys.argv[2].strip("'"'"'))

# 譜面を取得開始
print('譜面を取得中です…')

# osuSongsPathにある譜面を全て取得して値を取り出す
copyMusicPaths = []
copyMusicDirectoryNames = []
for osuMusicPath in glob.glob(os.path.join(osuSongsPath, r'**\*.osu'), recursive=True):
    with open(osuMusicPath, encoding='UTF-8') as f:
        if not os.path.basename(os.path.dirname(osuMusicPath)) in copyMusicDirectoryNames:
            copyMusicPaths.append(os.path.join(os.path.dirname(osuMusicPath), [s for s in [s.strip(
            ) for s in f.readlines()] if s.startswith('AudioFilename:')][0].lstrip('AudioFilename:').strip()))
            copyMusicDirectoryNames.append(os.path.basename(os.path.dirname(osuMusicPath)))

# 譜面を取得完了
print('譜面が正しく取得されました。\n')

# コピー開始
print('コピー中です…')

# 取り出した値のMP3ファイルをcopyPathに全てコピー
renameMP3FileNameList = []
for copyMP3Path in copyMusicPaths:
    copyMP3DirectoryName = os.path.basename(os.path.dirname(copyMP3Path))
    copyMP3ReMatch = re.match(r'\d+', copyMP3DirectoryName)
    if copyMP3ReMatch == None:
        copyMP3Number = ''
    else:
        copyMP3Number = copyMP3ReMatch.group()
    if copyMP3Number == '' or glob.glob(os.path.join(copyPath, copyMP3Number + ' *.mp3')):
        continue
    renameMP3FileNameList.append(copyMP3DirectoryName + ".mp3")
    if not os.path.isfile(os.path.join(copyPath, copyMP3DirectoryName + ".mp3")):
        print(copyMP3DirectoryName + 'の音楽ファイルが見つかりません。スキップします。')
    shutil.copy2(copyMP3Path, os.path.join(copyPath, copyMP3DirectoryName + ".mp3"))

# コピー完了
print('ファイルが正しくコピーされました。\n')

# リネーム開始
print('リネーム中です…')

# コピーしたMP3ファイルをリネーム
for renameMP3FileName in renameMP3FileNameList:
    renamedMP3FileName = re.sub(r'^\d+ ', '', renameMP3FileName)
    renamedMP3FileName = re.sub(r' \[no video\]\.mp3$', '.mp3', renamedMP3FileName)
    if os.path.isfile(os.path.join(copyPath, renamedMP3FileName)):
        renamedMP3FileName = renamedMP3FileName.replace('.mp3', ' (1).mp3')
        renameCount = 1
        while os.path.isfile(os.path.join(copyPath, renamedMP3FileName)):
            renameCount += 1
            renamedMP3FileName = renamedMP3FileName.replace(' (' + str(renameCount - 1) +').mp3', ' (' + str(renameCount) +').mp3')
    os.rename(os.path.join(copyPath, renameMP3FileName), os.path.join(copyPath, renamedMP3FileName))

# 終了
print('ファイルが正しくリネームされました。')
sys.exit(0)
