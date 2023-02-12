@ECHO OFF
GOTO main

:main
pdm run py -3.11 ./src/bot/main.py -q
pause
GOTO main