from cx_Freeze import Executable, setup

setup(
    name="osu! Music Copier",
    version="1.2",
    description="osu!の譜面フォルダーから音楽ファイルをコピーします。",
    executables=[Executable("osu-Music-Copier.py")],
)
