import ctypes
import glob
import os
import re
import shutil
import sys
import tkinter
import threading
import webbrowser
from tkinter import filedialog, ttk, messagebox


# Aboutを表示
def showAbout():
    aboutDialog = tkinter.Toplevel(mainRoot)
    aboutDialog.grab_set()
    aboutDialog.resizable(False, False)
    aboutDialog.title("About")

    aboutFrame = ttk.Frame(aboutDialog)
    aboutNameLabel = ttk.Label(aboutFrame, text="osu! Music Copier", font=(None, 15))

    aboutVerLabel = ttk.Label(aboutFrame, text="ver.1.0")
    aboutAuthorLabel = ttk.Label(aboutFrame, text="作者: ReNeeter")
    aboutLinkLabel = ttk.Label(
        aboutFrame,
        text="https://github.com/ReNeeter/osu-Music-Copier",
        foreground="#0000EE",
    )
    aboutLinkLabel.bind(
        "<1>",
        lambda e: webbrowser.open("https://github.com/ReNeeter/osu-Music-Copier"),
    )

    aboutFrame.pack()
    aboutNameLabel.pack(pady=(10, 5))
    aboutVerLabel.pack()
    aboutAuthorLabel.pack()
    aboutLinkLabel.pack(padx=10, pady=(0, 10))


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

    # startThread(showProgress)

    copyMusicPathList = []
    osuSongDirNumList = []
    renameMusicNameList = []

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
                copyMusicName = (
                    [
                        s
                        for s in [s.strip() for s in f.readlines()]
                        if s.startswith("AudioFilename:")
                    ][0]
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
                renameMusicNameList.append(
                    osuSongDirName + os.path.splitext(copyMusicName)[1]
                )

    for copyMusicPath in copyMusicPathList:
        shutil.copy2(
            copyMusicPath,
            os.path.join(
                copyPath,
                os.path.basename(os.path.dirname(copyMusicPath))
                + os.path.splitext(copyMusicPath)[1],
            ),
        )

    if isRename:
        renameCopyFile(copyPath, renameMusicNameList)
    else:
        # progressDialog.destroy()
        messagebox.showinfo("情報", "音楽ファイルが全てコピーされました。")


# ディレクトリ選択ダイアログを表示
def showDirSelect(setEntry):
    selectDir = tkinter.filedialog.askdirectory()
    if selectDir:
        setEntry.delete(0, "end")
        setEntry.insert(0, selectDir)


# コピーしたファイルをリネーム
def renameCopyFile(copyPath, renameMusicNameList):
    for renameMusicName in renameMusicNameList:
        renameMusicNameExt = os.path.splitext(renameMusicName)[1]
        renamedMusicName = re.sub(
            r" \[no video\]" + renameMusicNameExt + r"$",
            renameMusicNameExt,
            re.sub(r"^\d+ ", "", renameMusicName),
        )
        if os.path.isfile(os.path.join(copyPath, renamedMusicName)):
            renamedMusicName = renamedMusicName.replace(
                renameMusicNameExt, " (1)" + renameMusicNameExt
            )
            renameCount = 1
            while os.path.isfile(os.path.join(copyPath, renamedMusicName)):
                renameCount += 1
                renamedMusicName = renamedMusicName.replace(
                    " (" + str(renameCount - 1) + ")" + renameMusicNameExt,
                    " (" + str(renameCount) + ")" + renameMusicNameExt,
                )
        os.rename(
            os.path.join(copyPath, renameMusicName),
            os.path.join(copyPath, renamedMusicName),
        )

    # progressDialog.destroy()
    messagebox.showinfo("情報", "音楽ファイルが全てコピー＆リネームされました。")


# 進捗状況を表示
def showProgress():
    progressDialog = tkinter.Toplevel(mainRoot)
    progressDialog.grab_set()
    progressDialog.resizable(False, False)
    progressDialog.title("進捗状況")

    progressFrame = ttk.Frame(progressDialog)
    progressBar = ttk.Progressbar(progressFrame, mode="indeterminate")

    progressFrame.pack()
    progressBar.pack()
    progressBar.start()


# スレッドを開始
def startThread(thread, *args):
    threading.Thread(target=thread, args=args).start()


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
    text="コピー後にファイル名から識別番号等のゴミを取り除く",
    variable=isRenameCheckButtonChecked,
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
copyStartButton.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

mainRoot.mainloop()
