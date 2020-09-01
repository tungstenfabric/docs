# Python coding style

`Programs must be written for people to read, and only incidentally for machines to execute`

`-Abelson & Sussman, Structure and Interpretation of Computer Programs`

This document talk about the new technique and idioms followed for python contrail code and ways to verify code if based on coding requirement.

# PEP 8 standard
PEP 8 (Python Enhancement Proposal) is the de-facto code style guide for Python. A high quality, easy-to-read version of PEP 8 is also available at pep8.org. PEP 8 is a new coding standard adopted by all new juniper python code. You can also refer to following link to learn more about PEP 8:
http://www.python.org/dev/peps/pep-0008/
All new code has to adhere to the above standard.

# Utilities to verify your code:
There are many utilities that are avaliable in market for checking PEP8 coding guidelines. Following are few ways to do it.

### For VIM users:
- Using pep8 
    1. pip install pep8
    2. Run your python file with pep8 ` pep8 optparse.py `


- Using VIM indent
    1. Download http://www.vim.org/scripts/script.php?script_id=974 
    2. Save to ~/.vim/indent/python.vim
    3. In vimrc add line `source ~/.vim/indent/python.vim`

With Pathogen:
Install pathogen in vim:
https://github.com/tpope/vim-pathogen
- Flask 8
    1. pip install flask8 (Make sure you install flask8 on your m/c)
    2. Git clone https://github.com/nvie/vim-flake8 repo in ~/.vim/bundle 
    3. Add following lines in your vimrc files
        let g:flake8_show_in_file=1
        let g:flake8_show_in_gutter=1
    4. Open a Python file
        Press <F7> to run flake8 on it
    5. For more info checkout : https://github.com/nvie/vim-flake8

- Python-mode (This is more complicated way but it comes with more feature)
    1. Git clone https://github.com/klen/python-mode.git ~/.vim/bundle
    2. Add following lines in your vimrc:
        " Pathogen load
        filetype off
        call pathogen#infect()
        call pathogen#helptags()
        filetype plugin indent on
        syntax on
    3. When ever you save file your current file will be checked for pep standard
    4. For more info checkout : https://github.com/python-mode/python-mode


    
### For Sublime users:

- Using Sublime Package Control
    1. Use cmd+shift+P shortcut then Package Control: Install Package
    2. Look for Python PEP8 Autoformat and install it.

### For Atom user:
- Instal https://atom.io/packages/python-indent

References:
- https://www.python.org/dev/peps/pep-0008
- https://github.com/aniketgawade/PythonCodingGuideline/blob/master/README.md
- http://docs.python-guide.org/en/latest/writing/style
- https://google.github.io/styleguide/pyguide.html


