# Makefile for sparkup distribution
# TODO: this should use a separate build dir to copy SPARKUP_PY into.
#       SPARKUP_PY should not reside in the Vim runtime dir (getting not updated via Git!)
SPARKUP_PY=sparkup.py
VERSION=`date '+%Y%m%d'`
README=README.md

.PHONY: all textmate vim textmate-dist vim-dist plugins plugins-pre generic all-dist
all: plugins

plugins-pre:
	mkdir -p distribution

plugins: plugins-pre all-dist

textmate-dist: textmate
	cd TextMate && zip -9r ../distribution/sparkup-textmate-${VERSION}.zip . && cd ..

vim-dist: vim
	cd vim && zip -9r ../distribution/sparkup-vim-${VERSION}.zip . && cd ..

generic-dist: generic
	cd generic && zip -9r ../distribution/sparkup-generic-${VERSION}.zip . && cd ..

all-dist:
	zip -9r distribution/sparkup-${VERSION}.zip generic vim textmate README.md -x */sparkup-readme.txt
	cp distribution/sparkup-${VERSION}.zip distribution/sparkup-latest.zip

generic:
	cat ${SPARKUP_PY} > generic/sparkup
	chmod +x generic/sparkup
	#cp ${README} generic/sparkup-readme.txt

textmate:
	#cp ${README} TextMate/sparkup-readme.txt

vim: vim/doc/sparkup.txt

# create pathogen friendly structure
vim-pathogen: vim ftplugin doc

ftplugin doc:
	ln -s vim/$@

# Add asterisks to title, so it gets matched by `:helptags`
vim/doc/sparkup.txt: ${README}
	mkdir -p $(@D)
	sed '1s/.*/*\0*/' $< > $@
