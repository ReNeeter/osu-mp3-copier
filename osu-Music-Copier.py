import ctypes
import glob
import os
import re
import shutil
import tkinter
import threading
import webbrowser
from tkinter import filedialog, ttk, messagebox


# ホームページを開く
def openHomepage():
    webbrowser.open("https://github.com/ReNeeter/osu-Music-Copier")


# Aboutを表示
def showAbout():
    aboutDialog = tkinter.Toplevel(mainRoot)
    aboutDialog.grab_set()
    aboutDialog.resizable(False, False)
    aboutDialog.title("About")

    aboutFrame = ttk.Frame(aboutDialog)
    aboutNameLabel = ttk.Label(aboutFrame, text="osu! Music Copier", font=("", 15))

    aboutVerLabel = ttk.Label(aboutFrame, text="ver.1.0")
    aboutAuthorLabel = ttk.Label(aboutFrame, text="作者: ReNeeter")
    aboutLinkLabel = ttk.Label(
        aboutFrame,
        text="https://github.com/ReNeeter/osu-Music-Copier",
        foreground="#0000EE",
    )
    aboutLinkLabel.bind(
        "<1>",
        openHomepage(),
    )

    aboutFrame.pack()
    aboutNameLabel.pack(pady=(10, 5))
    aboutVerLabel.pack()
    aboutAuthorLabel.pack()
    aboutLinkLabel.pack(padx=10, pady=(0, 10))


# ディレクトリ選択ダイアログを表示
def showDirSelect(setEntry):
    selectDir = filedialog.askdirectory()
    if selectDir:
        setEntry.delete(0, "end")
        setEntry.insert(0, selectDir)


# スレッドを開始
def startThread(thread, *args):
    threading.Thread(target=thread, args=args).start()


# 進捗状況を表示
def showProgress():  # FIXME
    progressDialog = tkinter.Toplevel(mainRoot)
    progressDialog.grab_set()
    progressDialog.resizable(False, False)
    progressDialog.title("進捗状況")

    progressFrame = ttk.Frame(progressDialog)
    progressBar = ttk.Progressbar(progressFrame, mode="indeterminate")

    progressFrame.pack()
    progressBar.pack()
    progressBar.start()


# コピー
def copy(osuSongsPath, copyPath, isRename):
    if not osuSongsPath or not copyPath:
        messagebox.showerror("エラー", "パスが入力されていません。")
        return
    osuSongsPath = os.path.expandvars(osuSongsPath)
    copyPath = os.path.expandvars(copyPath)
    if not os.path.isdir(osuSongsPath) and not os.path.isdir(copyPath):
        messagebox.showerror("エラー", "入力されたパスが壊れています。")
        return

    copyMusicPathList = []
    osuSongDirNumList = []
    renameMusicNameList = []
    renamedMusicNameList = []

    for osuSongPath in glob.glob(
        os.path.join(osuSongsPath, r"**\*.osu"), recursive=True
    ):
        with open(osuSongPath, encoding="UTF-8") as f:
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
                if not os.path.isfile(os.path.join(osuSongDirPath, copyMusicName)):
                    messagebox.showwarning(
                        "注意",
                        osuSongDirName + "の音楽ファイルが見つかりません。\nスキップします。",
                    )
                    continue
                copyMusicPathList.append(os.path.join(osuSongDirPath, copyMusicName))
                osuSongDirNumList.append(osuSongDirNum)
                if isRename:
                    renamedMusicNameOriginal = [
                        s for s in osuSong if s.startswith("TitleUnicode:")
                    ]
                    if renamedMusicNameOriginal:
                        renamedMusicName = (
                            renamedMusicNameOriginal[0].lstrip("TitleUnicode:").strip()
                        )
                    else:
                        renamedMusicName = (
                            [s for s in osuSong if s.startswith("Title:")][0]
                            .lstrip("Title:")
                            .strip()
                        )
                    renamedMusicNameList.append(
                        renamedMusicName + os.path.splitext(copyMusicName)[1]
                    )

    if (
        len(copyMusicPathList) != len(osuSongDirNumList)
        or len(osuSongDirNumList) != len(renamedMusicNameList)
        or len(renamedMusicNameList) != len(copyMusicPathList)
    ):
        messagebox.showerror("エラー", "譜面を読込中にエラーが発生しました。")
        return

    for copyMusicPath in copyMusicPathList:
        copiedMusicName = (
            os.path.basename(os.path.dirname(copyMusicPath))
            + os.path.splitext(copyMusicPath)[1]
        )
        renameMusicNameList.append(copiedMusicName)
        shutil.copy2(copyMusicPath, os.path.join(copyPath, copiedMusicName))

    if isRename:
        renameCopyFile(copyPath, renameMusicNameList, renamedMusicNameList)
    else:
        messagebox.showinfo("情報", "音楽ファイルが全てコピーされました。")


# コピーしたファイルをリネーム
def renameCopyFile(copyPath, renameMusicNameList, renamedMusicNameList):
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

    messagebox.showinfo("情報", "音楽ファイルが全てコピー＆リネームされました。")


# Tkinterを設定
ctypes.windll.shcore.SetProcessDpiAwareness(True)

mainRoot = tkinter.Tk()
mainRoot.resizable(False, False)
mainRoot.title("osu! Music Copier")

mainMenu = tkinter.Menu(mainRoot)
mainMenu.add_command(label="About", command=showAbout)
mainRoot.config(menu=mainMenu)

mainFrame = ttk.Frame(mainRoot)
osuSongsPathLabel = ttk.Label(mainFrame, text="osu!のSongsフォルダのパス")
osuSongsPathEntry = ttk.Entry(mainFrame, width=80)
osuSongsPathBrowseButton = ttk.Button(
    mainFrame, text="参照…", command=lambda: showDirSelect(osuSongsPathEntry)
)
copyPathLabel = ttk.Label(mainFrame, text="音楽ファイルのコピー先のパス")
copyPathEntry = ttk.Entry(mainFrame, width=80)
copyPathBrowseButton = ttk.Button(
    mainFrame, text="参照…", command=lambda: showDirSelect(copyPathEntry)
)
isRenameCheckButtonChecked = tkinter.BooleanVar(value=True)
isRenameCheckButton = ttk.Checkbutton(
    mainFrame,
    text="コピー後にファイル名を曲名にリネームする",
    variable=isRenameCheckButtonChecked,
)
isAddTagCheckButtonChecked = tkinter.BooleanVar(value=True)
isAddTagCheckButton = ttk.Checkbutton(
    mainFrame,
    text="コピー後に譜面から音楽ファイルの情報を読み取りタグ付けする",
    variable=isAddTagCheckButtonChecked,
)
copyStartButton = ttk.Button(
    mainFrame,
    text="コピー",
    command=lambda: startThread(
        copy,
        osuSongsPathEntry.get(),
        copyPathEntry.get(),
        isRenameCheckButtonChecked.get(),
    ),
)

mainFrame.pack()
osuSongsPathLabel.grid(row=0, column=0, padx=10, pady=10)
osuSongsPathEntry.grid(row=0, column=1, padx=10, pady=10)
osuSongsPathBrowseButton.grid(row=0, column=2, padx=10, pady=10)
copyPathLabel.grid(row=1, column=0, padx=10, pady=10)
copyPathEntry.grid(row=1, column=1, padx=10, pady=10)
copyPathBrowseButton.grid(row=1, column=2, padx=10, pady=10)
isRenameCheckButton.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
isAddTagCheckButton.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
copyStartButton.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

mainRoot.mainloop()
