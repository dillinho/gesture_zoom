default:
	cat ./Makefile
format_code:
	black -l 120 .
run_tests:
	pytest tests
build:
	pyinstaller main.py
