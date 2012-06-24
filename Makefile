url = {Web Service Url Here}

database:
	rm -f ./db/snailbase
	./db/create-snailbase.py
	./db/insert-data-snailbase.py $(url)

clean:
	rm -f *~

