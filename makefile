
all:
	python3 ./main.py $(if $(count), $(count), 1)

ai:
	python3 ./ai.py