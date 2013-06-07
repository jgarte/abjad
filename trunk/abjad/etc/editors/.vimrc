" 0. preamble
" ===========

autocmd! bufwritepost .vimrc source %
call pathogen#infect()
filetype off
filetype plugin indent on
syntax on
let mapleader = ","


" 1. settings (alphabetical)
" ==========================

set autoindent
set autoread
set backspace=2
set background=light
set clipboard=unnamed
set colorcolumn=80
set completeopt=longest,menuone
set encoding=utf-8
set expandtab
set fileencodings=utf-8,latin1
set foldcolumn=4
set helpheight=80
set history=700
set incsearch
set mouse=a
set nobackup
set noswapfile
set nowrap
set nowritebackup
set number
set paste
set pastetoggle=<F2>
set ruler
set shiftround
set shiftwidth=4
set showcmd
set showmatch
set showmode
set smartcase
set softtabstop=4
set scrolloff=7
set tabstop=4
set tags=./tags
set textwidth=79
set title
set undolevels=700
set wildignore+=*.pyc
set wildignore+=*/coverage/*
set wildignore+=*_build/*
set wildmode=list:longest


" 2. mappings (alphabetical)
" ==========================

" comments
:map <F5> <Esc>:'a,'bs/^/#/<CR>
:map <F4> <Esc>:'a,'bs/#//<CR>

" copy & paste
vmap <C-y> y:call system("xclip -i -selection clipboard", getreg("\""))<CR>:call system("xclip -i", getreg("\""))<CR>
nmap <C-v> :call setreg("\"",system("xclip -o -selection clipboard"))<CR>p
imap <C-v> <Esc><C-v>a

" cursor vertical center
:nnoremap <Leader>zz :let &scrolloff=999-&scrolloff<CR>

" indentation 
vnoremap < <gv
vnoremap > >gv
map <Leader>a ggVG

" linesort 
vnoremap <Leader>s :sort<CR>
noremap <Leader>ab :'a,'bsort<CR>

" settings reload
map <Leader>v :source ~/.vimrc<CR>

" tab navigation 
map <Leader>n <esc>:tabprevious<CR>
map <Leader>m <esc>:tabnext<CR>

" window navigation 
map <c-j> <c-w>j
map <c-k> <c-w>k
map <c-l> <c-w>l
map <c-h> <c-w>h

" write & quit
noremap <Leader>w :write<CR>
noremap <Leader>q :quit<CR>
noremap <Leader>wq :wq<CR>


" 3. plugins (alphabetical)
" =========================

" ctrlp (https://github.com/kien/ctrlp.vim)
let g:ctrlp_max_height = 30

" jedi-vim (https://github.com/davidhalter/jedi-vim)
let g:jedi#related_names_command = "<leader>z"
let g:jedi#popup_on_dot = 0
let g:jedi#popup_select_first = 0
map <Leader>b Oimport ipdb; ipdb.set_trace() # BREAKPOINT<C-c>

" pydction (https://github.com/vim-scripts/Pydiction)
let g:pydiction_location='$ABJADTRUNK/abjad/etc/autocompletion/complete-dict'
let g:pydiction_menu_height = 20

" vim-powerline (https://github.com/Lokaltog/vim-powerline)
set laststatus=2
let g:Powerline_symbols = 'fancy'

" vim-markdown (https://github.com/tpope/vim-markdown)
set nofoldenable


" 4. other
" ========

" omnipopup (http://stackoverflow.com/a/2170800/70778)
function! OmniPopup(action)
    if pumvisible()
        if a:action == 'j'
            return "\<C-N>"
        elseif a:action == 'k'
            return "\<C-P>"
        endif
    endif
    return a:action
endfunction
inoremap <silent><C-j> <C-R>=OmniPopup('j')<CR>
inoremap <silent><C-k> <C-R>=OmniPopup('k')<CR>
