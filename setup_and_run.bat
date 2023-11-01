@echo off

REM Step 1: Set up a virtual environment (optional but recommended)
echo Setting up a virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Step 2: Install the requirements
echo Installing requirements...
pip install -r requirements.txt

REM Step 3: Run the application
echo Running the Logz.io-API-Query-Tool App...
python flask_app.py
