import sys
from cx_Freeze import setup, Executable

build_exe_options = {"includes": ["re"]}

exe = Executable(
    script="gui.py",
    targetName="Autobot.exe"
    )
setup(
    name = "Autobot",
    version = "1.0",
    options = {"build_exe": build_exe_options},
    description = "A bot that does what I say.",
    author="Me",
    executables = [exe])