Installation
------------

With Pathogen
^^^^^^^^^^^^^

If you are using tpope's vim-pathogen, install as follows:

       cd ~/.vim/bundle ; git clone https://github.com/rstacruz/sparkup.git
       cd sparkup
       make vim-pathogen


With Vundle
^^^^^^^^^^^

If using Vundle, you can specify Sparkup as a bundle and installation will happen
automatically.  Add this to your Vim configuration:

       Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}           

and run the standard installation command for Vundle:

       :PluginInstall


Manual installation
^^^^^^^^^^^^^^^^^^^

   1. Copy the contents of vim/ftplugin/ to your ~/.vim/ftplugin directory.

       (Assuming your current dir is sparkup/vim/)
       $ cp -R ftplugin ~/.vim/

   2. Copy the sparkup.py file to your ~/.vim directory

       (Assuming your current dir is sparkup/vim/)
       $ cp ../sparkup.py ~/.vim/


Configuration
-------------

Customise the Sparkup's configuration within Vim by specifying some or all of the following
as variables within your Vim configuration using the ``let`` directive.

   g:sparkup (Default: 'sparkup') -
     Location of the sparkup executable. You shouldn't need to change this
     setting if you used the install option above.

   g:sparkupArgs (Default: '--no-last-newline') -
     Additional args passed to sparkup.

   g:sparkupExecuteMapping (Default: '<c-e>') -
     Mapping used to execute sparkup within insert mode.

   g:sparkupNextMapping (Default: '<c-n>') -
     Mapping used to jump to the next empty tag/attribute within insert mode.

   g:sparkupMaps (Default: 1) -
     Set up automatic mappings for Sparkup. If set to 0, this can be
     used to disable creation of any mappings, which is useful if
     full customisation is required.

   g:sparkupMapsNormal (Default: 0) -
     Set up mappings for normal mode within Vim. The same execute and next
     mappings configured above will apply to normal mode if this option is
     set.

