import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="osu! Music Copier",
    version="1.0",
    description="osu!の譜面フォルダーから音楽ファイルをコピーします。",
    executables=[Executable("osu-Music-Copier.py", base=base)],
)
