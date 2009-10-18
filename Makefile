.PHONY: all textmate
textmate:
	mkdir -p TextMate/Sparkup.tmbundle/Support
	cp sparkup TextMate/Sparkup.tmbundle/Support/sparkup.py
all: textmate
