import ctypes
import tkinter
import tkinterdnd2  # FIXME
import threading
import webbrowser

from copier_process import copy
from tkinter import filedialog, ttk


# osu! Music Copierのリポジトリを開く
def openRepository(event):
    webbrowser.open("https://github.com/ReNeeter/osu-Music-Copier")


# Aboutを表示
def showAbout():
    aboutDialog = tkinter.Toplevel(mainRoot)
    aboutDialog.grab_set()
    aboutDialog.resizable(False, False)
    aboutDialog.title("About")

    aboutFrame = ttk.Frame(aboutDialog)
    aboutNameLabel = ttk.Label(aboutFrame, text="osu! Music Copier", font=("", 15))

    aboutVerLabel = ttk.Label(aboutFrame, text="ver.1.1")
    aboutAuthorLabel = ttk.Label(aboutFrame, text="作者: ReNeeter")
    aboutLinkLabel = ttk.Label(
        aboutFrame,
        text="https://github.com/ReNeeter/osu-Music-Copier",
        foreground="#0000EE",
    )
    aboutLinkLabel.bind(
        "<1>",
        openRepository,
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

isAddTagCheckButtonChecked = tkinter.BooleanVar(value=True)
isAddTagCheckButton = ttk.Checkbutton(
    mainFrame,
    text="コピー後に譜面から音楽ファイルの情報を読み取りタグ付けする\n（このオプションはコピーした音楽ファイルがID3形式の場合のみ機能します。\n既存のタグは上書きされます。）",
    variable=isAddTagCheckButtonChecked,
)
isRenameCheckButtonChecked = tkinter.BooleanVar(value=True)
isRenameCheckButton = ttk.Checkbutton(
    mainFrame,
    text="コピー後にファイル名を曲名にリネームする",
    variable=isRenameCheckButtonChecked,
)

copyStartButton = ttk.Button(
    mainFrame,
    text="コピー",
    command=lambda: threading.Thread(
        target=copy,
        args=(
            osuSongsPathEntry.get(),
            copyPathEntry.get(),
            isAddTagCheckButtonChecked.get(),
            isRenameCheckButtonChecked.get(),
        ),
    ).start(),
)

mainFrame.pack()
osuSongsPathLabel.grid(row=0, column=0, padx=10, pady=10)
osuSongsPathEntry.grid(row=0, column=1, padx=10, pady=10)
osuSongsPathBrowseButton.grid(row=0, column=2, padx=10, pady=10)
copyPathLabel.grid(row=1, column=0, padx=10, pady=10)
copyPathEntry.grid(row=1, column=1, padx=10, pady=10)
copyPathBrowseButton.grid(row=1, column=2, padx=10, pady=10)
isAddTagCheckButton.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
isRenameCheckButton.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
copyStartButton.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

mainRoot.mainloop()
