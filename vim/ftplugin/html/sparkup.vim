" Sparkup
" Installation:
" add the sparkup's vim directory to vim's runtimepath:
"   set rtp+=~/sparkup/vim

let paths = substitute(escape(&runtimepath, ' '), '\(,\|$\)', '/**\1', 'g')
let sparkup = fnamemodify(findfile('sparkup.vim', paths), ':p:h:h:h:h') .
  \ '/sparkup --no-last-newline --indent-spaces=' . &shiftwidth

nmap <c-e> :exec '.!' . sparkup<cr>:call SparkupNext()<cr>
imap <c-e> <c-g>u<Esc>:exec '.!' . sparkup<Cr>:call SparkupNext()<cr>
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
