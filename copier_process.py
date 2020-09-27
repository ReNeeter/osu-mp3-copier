import glob
import os
import re
import shutil

from mutagen import id3
from mutagen.easyid3 import EasyID3
from pathlib import Path  # FIXME
from tkinter import messagebox


# コピー
def copy(osuSongsPath, copyPath, isAddTag, isRename):
    if not osuSongsPath or not copyPath:
        messagebox.showerror("エラー", "パスが入力されていません。")
        return
    if not os.path.isdir(osuSongsPath) and not os.path.isdir(copyPath):
        messagebox.showerror("エラー", "入力されたパスが壊れています。")
        return

    osuSongDirNumList = []
    copyMusicPathList = []
    addTagList = []
    renameMusicNameList = []
    renamedMusicNameList = []

    for osuSongPath in glob.glob(
        os.path.join(osuSongsPath, r"**\*.osu"), recursive=True
    ):
        with open(osuSongPath, encoding="utf8") as f:
            osuSongDirPath = os.path.dirname(osuSongPath)
            osuSongDirName = os.path.basename(osuSongDirPath)
            osuSongDirReMatch = re.match(r"\d+", osuSongDirName)
            if osuSongDirReMatch:
                osuSongDirNum = osuSongDirReMatch.group()
            else:
                osuSongDirNum = ""

            if not osuSongDirNum in osuSongDirNumList:
                osuSong = [s.strip() for s in f.readlines()]
                copyMusicName = (
                    [s for s in osuSong if s.startswith("AudioFilename:")][0]
                    .lstrip("AudioFilename:")
                    .strip()
                )
                copyMusicPath = os.path.join(osuSongDirPath, copyMusicName)
                osuSongDirNumList.append(osuSongDirNum)
                if not os.path.isfile(copyMusicPath):
                    messagebox.showwarning(
                        "注意",
                        osuSongDirName + "の音楽ファイルが見つかりません。\nスキップします。",
                    )
                    continue
                copyMusicPathList.append(copyMusicPath)

                copyMusicTitleOriginal = [
                    s for s in osuSong if s.startswith("TitleUnicode:")
                ]
                if copyMusicTitleOriginal:
                    copyMusicTitle = (
                        copyMusicTitleOriginal[0].lstrip("TitleUnicode:").strip()
                    )
                else:
                    copyMusicTitle = (
                        [s for s in osuSong if s.startswith("Title:")][0]
                        .lstrip("Title:")
                        .strip()
                    )

                if isRename:
                    renamedMusicNameList.append(
                        copyMusicTitle + os.path.splitext(copyMusicName)[1]
                    )

                if isAddTag:
                    try:
                        addTag = EasyID3(copyMusicPath)
                    except id3._util.ID3NoHeaderError:
                        continue
                    addTag["title"] = copyMusicTitle

                    copyMusicArtistOriginal = [
                        s for s in osuSong if s.startswith("ArtistUnicode:")
                    ]
                    if copyMusicArtistOriginal:
                        copyMusicArtist = (
                            copyMusicArtistOriginal[0].lstrip("ArtistUnicode:").strip()
                        )
                    else:
                        copyMusicArtist = (
                            [s for s in osuSong if s.startswith("Artist:")][0]
                            .lstrip("Artist:")
                            .strip()
                        )
                    addTag["artist"] = copyMusicArtist

                    copyMusicAlbumOriginal = [
                        s for s in osuSong if s.startswith("Source:")
                    ]
                    if copyMusicAlbumOriginal:
                        copyMusicAlbum = (
                            copyMusicAlbumOriginal[0].lstrip("Source:").strip()
                        )
                        addTag["album"] = copyMusicAlbum

                    addTagList.append(addTag)

    for copyMusicPath in copyMusicPathList:
        copiedMusicName = (
            os.path.basename(os.path.dirname(copyMusicPath))
            + os.path.splitext(copyMusicPath)[1]
        )
        renameMusicNameList.append(copiedMusicName)
        shutil.copy2(copyMusicPath, os.path.join(copyPath, copiedMusicName))

    if isAddTag:
        addTagCopyFile(addTagList)

    if isRename:
        renameCopyFile(copyPath, renameMusicNameList, renamedMusicNameList, isAddTag)
    elif isAddTag:
        messagebox.showinfo("情報", "音楽ファイルが全てコピー＆タグ付けされました。")
    else:
        messagebox.showinfo("情報", "音楽ファイルが全てコピーされました。")


# コピーしたファイルにタグを付ける
def addTagCopyFile(addTagList):
    for addTag in addTagList:
        addTag.save()


# コピーしたファイルをリネーム
def renameCopyFile(copyPath, renameMusicNameList, renamedMusicNameList, isAddTag):
    for renameMusicName, renamedMusicName in zip(
        renameMusicNameList, renamedMusicNameList
    ):
        renamedMusicNameExt = os.path.splitext(renamedMusicName)[1]
        renamedMusicName = renamedMusicName.replace('"', "'")
        renamedMusicName = re.sub(r"[\\/:*?<>|]", "", renamedMusicName)

        if os.path.isfile(os.path.join(copyPath, renamedMusicName)):
            renamedMusicName = re.sub(
                renamedMusicNameExt + r"$",
                " (1)" + renamedMusicNameExt,
                renamedMusicName,
            )
            renameCount = 1
            while os.path.isfile(os.path.join(copyPath, renamedMusicName)):
                renameCount += 1
                renamedMusicName = re.sub(
                    r" \(" + str(renameCount - 1) + r"\)" + renamedMusicNameExt + r"$",
                    " (" + str(renameCount) + ")" + renamedMusicNameExt,
                    renamedMusicName,
                )

        os.rename(
            os.path.join(copyPath, renameMusicName),
            os.path.join(copyPath, renamedMusicName),
        )

    if isAddTag:
        messagebox.showinfo("情報", "音楽ファイルが全てコピー＆タグ付け＆リネームされました。")
    else:
        messagebox.showinfo("情報", "音楽ファイルが全てコピー＆リネームされました。")
