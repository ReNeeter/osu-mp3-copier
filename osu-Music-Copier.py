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
osuSongsPath = os.path.expandvars(sys.argv[1])
copyPath = os.path.expandvars(sys.argv[2])

# 譜面を取得開始
print('譜面を取得中です…')

# osuSongsPathにある譜面を全て取得して値を取り出す
copyMusicPathList = []
osuMusicDirectoryNumberList = []
renameMusicFileNameList = []

for osuMusicPath in glob.glob(os.path.join(osuSongsPath, r'**\*.osu'), recursive=True):
    with open(osuMusicPath, encoding='UTF-8') as f:
        osuMusicDirectoryReMatch = re.match(r'\d+', os.path.basename(os.path.dirname(osuMusicPath)))
        if osuMusicDirectoryReMatch == None:
            osuMusicDirectoryNumber = ''
        else:
            osuMusicDirectoryNumber = osuMusicDirectoryReMatch.group()
        if not osuMusicDirectoryNumber in osuMusicDirectoryNumberList:
            copyMusicFileName = [s for s in [s.strip() for s in f.readlines()] if s.startswith('AudioFilename:')][0].lstrip('AudioFilename:').strip()
            copyMusicPathList.append(os.path.join(os.path.dirname(osuMusicPath), copyMusicFileName))
            osuMusicDirectoryNumberList.append(osuMusicDirectoryNumber)
            renameMusicFileNameList.append(copyMusicFileName)

# 譜面を取得完了
print('譜面が正しく取得されました。\n')

# コピー開始
print('コピー中です…')

# 取り出した値の音楽ファイルをcopyPathに全てコピー
for copyMusicPath in copyMusicPathList:
    copyMusicDirectoryName = os.path.basename(os.path.dirname(copyMusicPath))
    if not os.path.isfile(copyMusicPath):
        print(copyMusicDirectoryName + 'の音楽ファイルが見つかりません。スキップします。')
        continue
    shutil.copy2(copyMusicPath, os.path.join(copyPath, copyMusicDirectoryName + os.path.splitext(copyMusicPath)[1]))

# コピー完了
print('ファイルが正しくコピーされました。\n')

# リネーム開始
print('リネーム中です…')

# コピーした音楽ファイルを全てリネーム
for renameMusicFileName in renameMusicFileNameList:
    renameMusicFileNameExt = os.path.splitext(renameMusicFileName)[1]
    renamedMusicFileName = re.sub(r' \[no video\]' + renameMusicFileNameExt + r'$', renameMusicFileNameExt, re.sub(r'^\d+ ', '', renameMusicFileName))
    if os.path.isfile(os.path.join(copyPath, renamedMusicFileName)):
        renamedMusicFileName = renamedMusicFileName.replace(renameMusicFileNameExt, ' (1)' + renameMusicFileNameExt)
        renameCount = 1
        while os.path.isfile(os.path.join(copyPath, renamedMusicFileName)):
            renameCount += 1
            renamedMusicFileName = renamedMusicFileName.replace(' (' + str(renameCount - 1) + ')' + renameMusicFileNameExt, ' (' + str(renameCount) + ')' + renameMusicFileNameExt)
    os.rename(os.path.join(copyPath, renameMusicFileName), os.path.join(copyPath, renamedMusicFileName))

# 終了
print('ファイルが正しくリネームされました。')
