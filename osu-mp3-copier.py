import glob
import os
import re
import shutil
import sys

# ソフトの詳細を表示
print('osu-mp3-copier ver.0.2\n作者:ReNeeter\n')

# 引数のエラー判定
if len(sys.argv) != 3:
    print('引数が正しく指定されていません。')
    sys.exit(1)

# パス
osuPath = os.path.expandvars(repr(sys.argv[1]).strip("'"))
copyPath = os.path.expandvars(repr(sys.argv[2]).strip("'"))

# コピー開始
print('コピー中です...')

# osuPathのSongsフォルダの中にあるMP3ファイルをcopyPathに全てコピー
for copyMP3Path in glob.glob(os.path.join(osuPath, r'Songs\**\*.mp3'), recursive=True):
    copyMP3DirectoryName = os.path.basename(os.path.dirname(copyMP3Path))
    copyMP3ReMatch = re.match(r'\d+', copyMP3DirectoryName)
    if copyMP3ReMatch == None:
        copyMP3Number = ''
    else:
        copyMP3Number = copyMP3ReMatch.group()
    if copyMP3Number == '' or glob.glob(os.path.join(copyPath, copyMP3Number + ' *.mp3')):
        continue
    shutil.copy2(copyMP3Path, os.path.join(copyPath, copyMP3DirectoryName + ".mp3"))

# コピー完了
print('MP3ファイルが正しくコピーされました。\n')

# リネーム開始
print('リネーム中です...')

# コピーしたMP3ファイルをリネーム
for renameMP3FileName in [f for f in os.listdir(copyPath) if os.path.isfile(os.path.join(copyPath, f))]:
    if os.path.splitext(renameMP3FileName)[1] != '.mp3':
        continue
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
print('MP3ファイルが正しくリネームされました。')
sys.exit(0)
