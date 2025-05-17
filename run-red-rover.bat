:main
CALL "virt\Scripts\activate"
python src\main.py
timeout /t 5
goto main