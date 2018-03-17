@echo off
TITLE Kevin Rudd
ECHO.

ECHO ------CALLING venv/Scripts/activate.bat------

CALL venv/Scripts/activate.bat
GOTO bot_start

:bot_start
ECHO ----------------LAUNCHING BOT----------------
ECHO.
ECHO.
python bot.py
TIMEOUT /NOBREAK /T 1
IF EXIST kill.txt GOTO killed
ECHO.
ECHO.
ECHO ----------RESTARTING BOT IN 10 SECS----------
TIMEOUT /T 10
ECHO.
GOTO bot_start

:killed
ECHO ------------RUDD DEAD, NO RESTART------------
DEL kill.txt
ECHO. 
EXIT /B