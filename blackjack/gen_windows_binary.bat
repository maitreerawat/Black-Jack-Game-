@echo off
pyinstaller blackjack.spec
move dist\blackjack.exe blackjack.exe
rmdir /s/q build
rmdir /s/q dist
rmdir /s/q __pycache__