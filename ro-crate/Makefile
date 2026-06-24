.PHONY: crate html all clean

.PHONY: crate html

crate:
	python generate_crate.py

html:
	docker run --rm -v "$(shell realpath .. -P):/data" simleo/rochtml /data/ro-crate-metadata.json

all: crate html

clean:
	rm -f ro-crate-metadata.json ro-crate-preview.html
