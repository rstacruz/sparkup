" functions will be loaded lazily when needed
" exec vam#DefineAndBind('s:c','g:sparkup', '{}')
if !exists('g:sparkup') | let g:sparkup = {} | endif | let s:c = g:sparkup
let s:c.filetypes = get(s:c, 'filetypes','^\%(html\|xhtml\|xml\|ur\|urs\)$')

augroup SPARKUP
  au!
  " this one is which you're most likely to use?
  autocmd BufRead,BufNewFile *  if &ft =~ s:c.filetypes | call sparkup#SetupBuffer() | endif
augroup end
