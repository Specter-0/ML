
all:
	python3 ./main.py $(if $(count), $(count), 1)
