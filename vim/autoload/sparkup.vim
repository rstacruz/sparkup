if !exists('g:sparkup') | let g:sparkup = {} | endif | let s:c = g:sparkup

" TODO: make this a list ? - use ShellDSL of VAM or the like?
let s:c.args = get(s:c, 'args', '--no-last-newline')

let s:c.lhs_expand = get(s:c, 'lhs_expand', '<c-e>')
let s:c.lhs_jump_next_empty_tag = get(s:c, 'lhs_jump_next_empty_tag', '<c-n>')
let s:c.python = get(s:c, 'py_file', 'python')
let s:c.py_file = get(s:c, 'py_file', expand('<sfile>:h:h:h').'/sparkup.py')

fun! sparkup#Setup()
    exec 'nnoremap <buffer> ' . s:c.lhs_expand . ' :call sparkup#Expand()<cr>'
    exec 'inoremap <buffer> ' . s:c.lhs_expand . ' <c-g>u<Esc>:call sparkup#Expand()<cr>'
    exec 'nnoremap <buffer> ' . s:c.lhs_jump_next_empty_tag . ' :call sparkup#Next()<cr>'
    exec 'inoremap <buffer> ' . s:c.lhs_jump_next_empty_tag . ' <c-g>u<Esc>:call sparkup#Next()<cr>'
endf


function! sparkup#Next()
    " 1: empty tag, 2: empty attribute, 3: empty line
    let n = search('><\/\|\(""\)\|^\s*$', 'Wp')
    if n == 3
        startinsert!
    else
        execute 'normal l'
        startinsert
    endif
endfunction


" historical name: s:Sparkup()
function! sparkup#Expand()
  if !executable(s:c.py_file)
    echoe 'Warning: could not find sparkup on your path or in your vim runtime path.'
    return
  endif
  let s:c.cmd = shellescape(s:c.python).' '.shellescape(s:c.py_file).' '.s:c.args.' --indent-spaces='.&sw
  exec '.!' . s:c.cmd
  call sparkup#Next()
endfunction
