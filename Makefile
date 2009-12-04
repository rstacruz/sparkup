SPARKUP_PY=sparkup
.PHONY: all textmate vim
all: textmate vim
textmate:
	mkdir -p TextMate/Sparkup.tmbundle/Support
	cp ${SPARKUP_PY} TextMate/Sparkup.tmbundle/Support/sparkup.py
vim:
	mkdir -p vim/ftplugin/html
	cp ${SPARKUP_PY} vim/ftplugin/html/sparkup.py
