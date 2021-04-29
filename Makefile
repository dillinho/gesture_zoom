default:
	cat ./Makefile
format_code:
	black -l 120 .
run_tests:
	pytest tests
build:
	pyinstaller main.spec
	# try: pyinstaller --add-data "PATH\TO\mediapipe\modules;mediapipe\modules" --onefile --noconsole main.py
run_exe:
	dist\main.exe
