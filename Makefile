# Sparkup makefile
# ================

# Account for incremental version numbers (e.g., 0.3.5-20091229)
VERSION    = $(subst {date},${shell date +%Y%m%d},$(shell cat VERSION))
ROOT      := $(PWD)

# Paths
PLUGINS_PATH      = plugins
DOC_PATH          = docs
DISTRIB_PATH      = sparkup-${VERSION}
DISTRIB_PLUGINS   = ${DISTRIB_PATH}/textmate ${DISTRIB_PATH}/vim ${DISTRIB_PATH}/generic ${DISTRIB_PATH}/docs
DISTRIB_FILES     = ${DISTRIB_PLUGINS} ${DISTRIB_PATH}/readme.txt

# Files
README      = README.md
SPARKUP_PY  = ${DISTRIB_PATH}/sparkup.py
FINAL_ZIP   = sparkup-${VERSION}.zip

.PHONY: all distrib ${DISTRIB_PATH} ${DISTRIB_PLUGINS} distrib_cleanup ${SPARKUP_PY}
all: ${FINAL_ZIP}
	@echo ------
	@echo  
	@echo Done!
	@echo  
	@echo . - ${FINAL_ZIP}
	@echo .   This is the redistributable ZIP file.
	@echo .
	@echo . - ${DISTRIB_PATH}/
	@echo .   The plugins are here, ready-to-use.

# Final .zip
${FINAL_ZIP}: distrib
	cd ${DISTRIB_PATH} && zip -9r "${ROOT}/$@" ${DISTRIB_FILES:${DISTRIB_PATH}/%=%} \
 	  --exclude */.DS_Store --exclude */Thumbs.db --exclude */*.pyc

# Distribution path
distrib: ${DISTRIB_PATH} ${DISTRIB_FILES} distrib_cleanup

distrib_cleanup:
	rm ${SPARKUP_PY}

${DISTRIB_PATH}:
	mkdir -p "$@"

${DISTRIB_PATH}/readme.txt: ${README}
	cp ${README} "$@"

${DISTRIB_PATH}/textmate: ${SPARKUP_PY}
	mkdir -p "$@"
	cp -R "${PLUGINS_PATH}/textmate" "${DISTRIB_PATH}"
	mkdir -p "$@/Sparkup.tmbundle"
	mkdir -p "$@/Sparkup.tmbundle/Support"
	cp ${SPARKUP_PY} \
	   "$@/Sparkup.tmbundle/Support/sparkup.py"

${DISTRIB_PATH}/vim: ${SPARKUP_PY}
	mkdir -p "$@"
	cp -R "${PLUGINS_PATH}/vim" "${DISTRIB_PATH}"
	mkdir -p "$@/ftplugin/html"
	cp ${SPARKUP_PY} "$@/ftplugin/html/sparkup.py"

${DISTRIB_PATH}/generic: ${SPARKUP_PY}
	mkdir -p "$@"
	cp -R "${PLUGINS_PATH}/generic" "${DISTRIB_PATH}"
	cat ${SPARKUP_PY} > "$@/sparkup"
	chmod +x "$@/sparkup"

${DISTRIB_PATH}/docs:
	cp -R docs "$@"

# Sources
${SPARKUP_PY}:
	cat "src/sparkup/sparkup.py" | sed 's/^VERSION.*$$/VERSION = "${VERSION}"/' > $@

