@ECHO off
TITLE Setting up bot environment
ECHO Creating new virtual environment ~/venv/
python -m venv --clear venv
CALL venv/Scripts/activate.bat
python -m pip install -r requirements.txt
ECHO Finished installing requirements
ECHO Launching bot (use run.bat in future)
TITLE Kevin Rudd
CALL run.bat