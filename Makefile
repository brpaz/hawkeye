
lint:
	@find . -iname "*.py" | xargs pylint

format:
	@autopep8 --in-place --recursive --aggressive .

deps:
	@pip install -r requirements.txt

run:
	@python3 main.py --uri="https://m.google.com"

run-pdf:
	@python3 main.py --uri="file://$(CURDIR)/testfiles/github-git-cheat-sheet.pdf"

run-md:
	@python3 main.py --uri="file://$(CURDIR)/testfiles/phpspec-cheat-sheet.md"

install:
	sudo python3 setup.py install
	make clean

clean:
	sudo python3 setup.py clean
