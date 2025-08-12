:main
CALL "virt\Scripts\activate"
python src\debug.py
timeout /t 5
goto main