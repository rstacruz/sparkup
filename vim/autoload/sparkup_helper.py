#!/usr/bin/env python

def sparkup_expand():
    if not 'sparkup_router' in globals():
        import sys, vim
        sys.path.append(vim.eval("g:sparkup.plugin_home"))
        import sparkup
        sparkup_router = sparkup.Router()

    options = { 'indent-spaces': vim.eval('&sw') }
    lines = sparkup_router.start(options, vim.current.line, True).split("\n")
    vim.current.line = lines[0]
    if len(lines) > 0:
        vim.current.buffer.append(lines[1:], int(vim.eval("line('.')")))

sparkup_expand()
