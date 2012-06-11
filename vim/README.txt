Installation
------------

  VAM: just add 'sparkup' to the list of plugins to be activated.

  manually:

   First checkout, then add to your .vimrc:
   let rtp=$SPARKUP/vim

INTERFACE
----------
<c-e>: expand sparkup string
<c-n>: jump to next empty tag

Configuration
-------------

  Put in your .vimrc if you want to change the defaults:

  let g:sparkup = {}
  let g:sparkup.filetypes = regex matching filetypes, see 

  let g:sparkup.args = ..
  let g:sparkup.lhs_expand = <c-e>
  let g:sparkup.lhs_jump_next_empty_tag = <c-n>

  defaults settings see plugin/sparkup.vim, autoload/sparkup.vim
