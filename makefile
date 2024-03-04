all:
	python3 ./main.py $(if $(count), $(count), 1)

ai:
	python3 ./ai.py $(if $(speed), $(speed), 10)

test:
	python3 ./ml_tests/${file}.py