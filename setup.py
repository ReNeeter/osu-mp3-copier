from cx_Freeze import Executable, setup

setup(
    name="osu! Music Copier",
    version="2.0",
    description="Copy the music file from the music folder of osu!.",
    executables=[Executable("osu-music-copier.py")],
)
