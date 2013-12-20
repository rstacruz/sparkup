Installation
------------

   1. Copy the contents of vim/ftplugin/ to your ~/.vim/ftplugin directory.

       (Assuming your current dir is sparkup/vim/)
       $ cp -R ftplugin ~/.vim/

   2. Copy the sparkup.py file to your ~/.vim directory

       (Assuming your current dir is sparkup/vim/)
       $ cp ../sparkup.py ~/.vim/

Or use tpope's vim-pathogen:

       cd ~/.vim/bundle ; git clone
       cd sparkup
       make vim-pathogen

Configuration
-------------

  g:sparkup (Default: 'sparkup') -
    Location of the sparkup executable. You shouldn't need to change this
    setting if you used the install option above.

  g:sparkupArgs (Default: '--no-last-newline') -
    Additional args passed to sparkup.

  g:sparkupExecuteMapping (Default: '<c-e>') -
    Mapping used to execute sparkup.

  g:sparkupNextMapping (Default: '<c-n>') -
    Mapping used to jump to the next empty tag/attribute.
