" Sparkup
" Installation:
"    Copy the contents of vim/ftplugin/ to your ~/.vim/ftplugin directory:
"
"        $ cp -R vim/ftplugin ~/.vim/ftplugin/
"
"    or use one of the automated methods specified in the README.txt file.
"
" Configuration:
"   g:sparkup (Default: 'sparkup') -
"     Location of the sparkup executable. You shouldn't need to change this
"     setting if you used the install option above.
"
"   g:sparkupArgs (Default: '--no-last-newline') -
"     Additional args passed to sparkup.
"
"   g:sparkupExecuteMapping (Default: '<c-e>') -
"     Mapping used to execute sparkup within insert mode.
"
"   g:sparkupNextMapping (Default: '<c-n>') -
"     Mapping used to jump to the next empty tag/attribute within insert mode.
"
"   g:sparkupMaps (Default: 1) -
"     Set up automatic mappings for Sparkup. If set to 0, this can be
"     used to disable creation of any mappings, which is useful if
"     full customisation is required.
"
"   g:sparkupMapsNormal (Default: 0) -
"     Set up mappings for normal mode within Vim. The same execute and next
"     mappings configured above will apply to normal mode if this option is
"     set.

if !exists('g:sparkupExecuteMapping')
  let g:sparkupExecuteMapping = '<c-e>'
endif

if !exists('g:sparkupNextMapping')
  let g:sparkupNextMapping = '<c-n>'
endif

if !exists('g:sparkupMaps')
  let g:sparkupMaps = 1
endif

if !exists('g:sparkupMapsNormal')
  let g:sparkupMapsNormal = 0
endif

inoremap <buffer> <Plug>SparkupExecute <c-g>u<Esc>:call <SID>Sparkup()<cr>
inoremap <buffer> <Plug>SparkupNext    <c-g>u<Esc>:call <SID>SparkupNext()<cr>

if g:sparkupMaps
  if ! hasmapto('<Plug>SparkupExecute', 'i')
    exec 'imap <buffer> ' . g:sparkupExecuteMapping . ' <Plug>SparkupExecute'
  endif
  if ! hasmapto('<Plug>SparkupNext', 'i')
    exec 'imap <buffer> ' . g:sparkupNextMapping . ' <Plug>SparkupNext'
  endif
  if g:sparkupMapsNormal
    if ! hasmapto('<Plug>SparkupExecute', 'n')
      exec 'nnoremap <buffer> ' . g:sparkupExecuteMapping . ' :call <SID>Sparkup()<cr>'
    endif
    if ! hasmapto('<Plug>SparkupNext', 'n')
      exec 'nnoremap <buffer> ' . g:sparkupNextMapping . ' :call <SID>SparkupNext()<cr>'
    endif
  endif
endif

if exists('*s:Sparkup')
    finish
endif

function! s:Sparkup()
    if !exists('s:sparkup')
        let s:sparkup = exists('g:sparkup') ? g:sparkup : 'sparkup'

        if !executable(s:sparkup)
            " If g:sparkup is not configured (and/or not found in $PATH),
            " look for sparkup.vim in Vim's runtimepath.
            " XXX: quite expensive for a Pathogen-like environment (where &rtp is huge)
            let paths = substitute(escape(&runtimepath, ' '), '\(,\|$\)', '/**\1', 'g')
            let s:sparkup = fnamemodify(findfile('sparkup.py', paths), ':p')

            if !filereadable(s:sparkup)
                echohl WarningMsg
                echom 'Warning: could not find sparkup/sparkup.py on your path or in your vim runtime path.'
                echohl None
                unlet s:sparkup
                return
            endif
        endif
        let s:sparkup = '"' . s:sparkup . '"'
        " Workaround for windows, where the Python file cannot be executed via shebang
        if has('win32') || has('win64')
            let s:sparkup = 'python ' . s:sparkup
        endif
    endif

    " Build arguments list (not cached, g:sparkupArgs might change, also
    " &filetype, &expandtab etc)
    let sparkupArgs = exists('g:sparkupArgs') ? g:sparkupArgs : '--no-last-newline'
    " Pass '--xml' option, if 'xml' is used as filetype (default: none/'html')
    " NOTE: &filetype can contain multiple values, e.g. 'smarty.html'
    if index(split(&filetype, '\.'), 'xml') >= 0
        let sparkupArgs .= ' --xml'
    endif
    " If the user's settings are to indent with tabs, do so!
    " TODO textmate version of this functionality
    if !&expandtab
        let sparkupArgs .= ' --indent-tabs'
    endif

    let sparkupCmd = s:sparkup . printf(' %s --indent-spaces=%s', sparkupArgs, &shiftwidth)
    exec '.!' . sparkupCmd
    call s:SparkupNext()
endfunction

function! s:SparkupNext()
    " 1: empty tag, 2: empty attribute, 3: empty line
    let n = search('><\/\|\(""\)\|\(^\s*$\)', 'Wp')
    if n == 3
        startinsert!
    else
        let p = getpos(".")
        let p[2] = p[2] + 1
        call setpos(".", p)
        startinsert
    endif
endfunction
