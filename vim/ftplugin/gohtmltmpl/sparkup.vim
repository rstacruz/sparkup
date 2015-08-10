for file in split(globpath(&rtp,'vim/ftplugin/html/sparkup.vim'), '\n')
  execute 'source ' . file
endfor
