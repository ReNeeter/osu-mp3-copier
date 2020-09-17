import glob
import os
import re
import shutil
import sys

# ソフトの詳細を表示
print('osu-MP3-Copier ver.0.3')
print('作者:ReNeeter\n')

# 引数の判定
if len(sys.argv) == 1:
    print('-----使い方-----')
    print('第1引数にosu!の譜面フォルダのパスを、第2引数にファイルのコピー先のパスを入力して実行してください。\n')
    print('-----例-----')
    print(r'osu-MP3-Copier.exe %LOCALAPPDATA%\osu!\Songs %USERPROFILE%\Music')
    sys.exit(0)
elif len(sys.argv) != 3:
    print('引数が正しく指定されていません。')
    sys.exit(1)

# パス
osuSongsPath = os.path.expandvars(repr(sys.argv[1]).strip("'"))
copyPath = os.path.expandvars(repr(sys.argv[2]).strip("'"))

# コピー開始
print('コピー中です...')

# osuSongsPathにあるMP3ファイルをcopyPathに全てコピー
renameMP3FileNameList = []
for copyMP3Path in glob.glob(os.path.join(osuSongsPath, r'**\*.mp3'), recursive=True):
    copyMP3DirectoryName = os.path.basename(os.path.dirname(copyMP3Path))
    copyMP3ReMatch = re.match(r'\d+', copyMP3DirectoryName)
    if copyMP3ReMatch == None:
        copyMP3Number = ''
    else:
        copyMP3Number = copyMP3ReMatch.group()
    if copyMP3Number == '' or glob.glob(os.path.join(copyPath, copyMP3Number + ' *.mp3')):
        continue
    renameMP3FileNameList.append(copyMP3DirectoryName + ".mp3")
    shutil.copy2(copyMP3Path, os.path.join(copyPath, copyMP3DirectoryName + ".mp3"))

# コピー完了
print('ファイルが正しくコピーされました。\n')

# リネーム開始
print('リネーム中です...')

# コピーしたMP3ファイルをリネーム
for renameMP3FileName in renameMP3FileNameList:
    renamedMP3FileName = re.sub(r'^\d+ ', '', renameMP3FileName)
    renamedMP3FileName = re.sub(r' \[no video\].mp3$', '.mp3', renamedMP3FileName)
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
