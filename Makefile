
lint:
	@find . -iname "*.py" | xargs pylint

format:
	@autopep8 --in-place --recursive --aggressive .

deps:
	@pip install -r requirements.txt

run:
	@python3 main.py --uri="https://m.google.com"

install:
	sudo python3 setup.py install
