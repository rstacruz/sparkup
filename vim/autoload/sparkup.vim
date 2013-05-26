if !exists('g:sparkup') | let g:sparkup = {} | endif | let s:c = g:sparkup

" TODO: make this a list ? - use ShellDSL of VAM or the like?
let s:c.args = get(s:c, 'args', '--no-last-newline')
let s:c.py_file = get(s:c, 'py_file', expand('<sfile>:h:h:h').'/sparkup.py')

fun! sparkup#Setup()
  call SparkupSetup()
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


let s:c.plugin_home = expand("<sfile>:h:h:h")
let s:setup = 0

" historical name: s:Sparkup()
function! sparkup#Expand()
  if !has('python') || !s:c.use_vim_python_if_available
    if !executable(s:c.py_file)
      echoe 'Warning: could not find sparkup on your path or in your vim runtime path.'
      return
    endif
    let s:c.cmd = shellescape(s:c.python).' '.shellescape(s:c.py_file).' '.s:c.args.' --indent-spaces='.&sw
    exec '.!' . s:c.cmd
  else
    exec 'pyfile '.fnameescape(g:sparkup.plugin_home).'/vim/autoload/sparkup_helper.py'
  endif
  call sparkup#Next()
endfunction
