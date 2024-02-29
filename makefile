
all:
	python3 ./draw.py $(if $(count), $(count), 1)
