" Sparkup
" Installation:
" add the sparkup's vim directory to vim's runtimepath:
"   set rtp+=~/sparkup/vim

if !exists('g:sparkup')
  let g:sparkup = 'sparkup'
endif

if !exists('g:sparkupArgs')
    let g:sparkupArgs = '--no-last-newline'
endif

" check the user's path first. if not found then search relative to
" sparkup.vim in the runtimepath.
if !executable(g:sparkup)
    let paths = substitute(escape(&runtimepath, ' '), '\(,\|$\)', '/**\1', 'g')
    let g:sparkup = fnamemodify(findfile('sparkup.vim', paths), ':p:h:h:h:h') .  '/sparkup'

    if !filereadable(g:sparkup)
        echohl WarningMsg
        echom 'Warning: could not find sparkup on your path or in your vim runtime path.'
        echohl None
        finish
    endif
endif

let g:sparkup .= printf(' %s --indent-spaces=%s', g:sparkupArgs, &shiftwidth)

nmap <c-e> :exec '.!' . g:sparkup<cr>:call SparkupNext()<cr>
imap <c-e> <c-g>u<Esc>:exec '.!' . g:sparkup<Cr>:call SparkupNext()<cr>
nmap <c-n> :call SparkupNext()<cr>
imap <c-n> <c-g>u<Esc>:call SparkupNext()<cr>

function! SparkupNext()
    " 1: empty tag, 2: empty attribute, 3: empty line
    let n = search('><\/\|\(""\)\|^\s*$', 'Wp')
    if n == 3
        startinsert!
    else
        execute 'normal l'
        startinsert
    endif
endfunction
