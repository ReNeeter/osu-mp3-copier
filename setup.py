from cx_Freeze import setup
from cx_Freeze import Executable

setup(
        name = 'osu-MP3-Extracter',
        version = '0.3',
        description = 'osu!のSongsフォルダに有るMP3ファイルを正しく抽出するPythonスクリプトです。',
        executables = [Executable('osu-MP3-Extracter.py')]
)
