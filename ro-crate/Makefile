.PHONY: crate html validator all clean

.PHONY: crate html validator

crate:
	python generate_crate.py

html:
	docker run --rm -v "$(shell realpath .. -P):/data" simleo/rochtml /data/ro-crate-metadata.json
	# Without this, rocrate-validator complains about the missing doctype
	# https://github.com/Language-Research-Technology/ro-crate-html-js/issues/7
	sed -i '1i <!DOCTYPE html>' ../ro-crate-preview.html

validator:
	rocrate-validator validate --verbose --no-paging --output-format text ../

all: crate html validator

clean:
	rm -f ../ro-crate-metadata.json ../ro-crate-preview.html
