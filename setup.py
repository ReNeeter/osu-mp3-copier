from cx_Freeze import setup
from cx_Freeze import Executable

setup(
        name = 'osu-Music-Copier',
        version = '0.4',
        description = 'osu!の譜面フォルダーから音楽ファイル等をコピーするPythonスクリプトです。',
        executables = [Executable('osu-Music-Copier.py')]
)
