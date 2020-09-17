from cx_Freeze import setup
from cx_Freeze import Executable

setup(
        name = 'osu-MP3-Copier',
        version = '0.3',
        description = 'osu!の譜面フォルダからMP3ファイル等をコピーするPythonスクリプトです。',
        executables = [Executable('osu-MP3-Copier.py')]
)
