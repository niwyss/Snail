url = {Url to the Web Service}

database: 
	./db/create-snailbase.py
	./db/insert-data-snailbase.py $(url)

clean:
	rm -f *~ ./db/*~ ./query/*~ snail.sqlite

