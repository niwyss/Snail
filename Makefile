url = http://sncf.mobi/infotrafic/iphoneapp/gares/index/lastUpdate/20120101000000

database: 
	./db/create-snailbase.py
	./db/insert-data-snailbase.py $(url)

clean:
	rm -f *~ ./db/*~ snailbase

