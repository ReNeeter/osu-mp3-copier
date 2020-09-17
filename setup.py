from cx_Freeze import setup
from cx_Freeze import Executable

setup(
        name = 'osu-mp3-copier',
        version = '0.1',
        description = 'osu!のSongsフォルダに有るMP3ファイルを正しくコピーするPythonスクリプトです。',
        executables = [Executable('osu-mp3-copier.py')]
)
