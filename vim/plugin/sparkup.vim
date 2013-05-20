" functions will be loaded lazily when needed
" exec vam#DefineAndBind('s:c','g:sparkup', '{}')
if !exists('g:sparkup') | let g:sparkup = {} | endif | let s:c = g:sparkup

" for which filetypes to enable sparkup
let s:c.filetypes = get(s:c, 'filetypes','^\%(html\|xhtml\|xml\|ur\|urs\)$')

let s:c.use_vim_python_if_available = get(s:c, 'use_vim_python_if_available', 1)
let s:c.python = get(s:c, 'py_file', 'python')

fun! SparkupSetup()
    " mapping
    let s:c.lhs_expand = get(s:c, 'lhs_expand', '<c-e>')
    let s:c.lhs_jump_next_empty_tag = get(s:c, 'lhs_jump_next_empty_tag', '<c-n>')

    exec 'nnoremap <buffer> ' . s:c.lhs_expand . ' :call sparkup#Expand()<cr>'
    exec 'inoremap <buffer> ' . s:c.lhs_expand . ' <c-g>u<Esc>:call sparkup#Expand()<cr>'
    exec 'nnoremap <buffer> ' . s:c.lhs_jump_next_empty_tag . ' :call sparkup#Next()<cr>'
    exec 'inoremap <buffer> ' . s:c.lhs_jump_next_empty_tag . ' <c-g>u<Esc>:call sparkup#Next()<cr>'
endf

augroup SPARKUP
  au!
  " this one is which you're most likely to use?
  autocmd Filetype *  if &ft =~ s:c.filetypes | call SparkupSetup() | endif
augroup end
