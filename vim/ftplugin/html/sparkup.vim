" Sparkup
" Installation:
"    Copy the contents of vim/ftplugin/ to your ~/.vim/ftplugin directory.
"
"        $ cp -R vim/ftplugin ~/.vim/ftplugin/
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
"     Mapping used to execute sparkup.
"
"   g:sparkupNextMapping (Default: '<c-n>') -
"     Mapping used to jump to the next empty tag/attribute.
"
"   g:sparkupMaps (Default: 1) -
"     Setup mappings?
"
"   g:sparkupMapsNormal (Default: 0) -
"     Setup mappings for normal mode?

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
    exec 'inoremap <buffer> ' . g:sparkupExecuteMapping . ' <Plug>SparkupExecute'
  endif
  if ! hasmapto('<Plug>SparkupNext', 'i')
    exec 'inoremap <buffer> ' . g:sparkupNextMapping . ' <Plug>SparkupNext'
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
        let s:sparkupArgs = exists('g:sparkupArgs') ? g:sparkupArgs : '--no-last-newline'
        let s:sparkupArgs = s:sparkupArgs . ' --' . &filetype

        " check the user's path first. if not found then search relative to
        " sparkup.vim in the runtimepath.
        if !executable(s:sparkup)
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
        let s:sparkup .= printf(' %s --indent-spaces=%s', s:sparkupArgs, &shiftwidth)
        if has('win32') || has('win64')
            let s:sparkup = 'python ' . s:sparkup
        endif
    endif
    exec '.!' . s:sparkup
    call s:SparkupNext()
endfunction

function! s:SparkupNext()
    " 1: empty tag, 2: empty attribute, 3: empty line
    let n = search('><\/\|\(""\)\|^\s*$', 'Wp')
    if n == 3
        startinsert!
    else
        execute 'normal l'
        startinsert
    endif
endfunction
