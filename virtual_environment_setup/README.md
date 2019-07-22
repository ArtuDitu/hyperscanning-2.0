# Virtual environment Setup


## 1. Use the virtualenvs from store folder
In order to use the already isntalled virtual environments from this folder, one has to:  
### A. Execute a few commands from terminal:  
- pip install virtualenvwrapper
- ln -s /net/store/nbp/projects/hyperscanning ~  (create link to the hyperscanning project in local home folder)

### B. Add several commands to the local ~/.bashrc file:  
- export HYPER=hyperscanning/hyperscanning-2.0/virtual\_environment\_setup/.virtualenvs
- export WORKON\_HOME=$HOME/$HYPER
- export VIRTUALENVWRAPPER\_PYTHON=/usr/bin/python3
- export VIRTUALENVWRAPPER\_VIRTUALENV=~/.local/bin/virtualenv
- source ~/.local/bin/virtualenvwrapper.sh (creates the necessary files in .virtualenvs folder in case they're not there yet)

In the end run the command 'source ~/.bashrc' from terminal.



## 2. Install virtual environment via requirements textfiles
The following commands will create a virtual environment with the same packages / version as used during development of the script.  
For the "hyper-2.0_env" (used to run main preprocessing-script), the necessary information is specified in 'requirements.txt' (**A.**) and 'environment.yml' (**B.**).  
For the "load_cnt" environment (used to convert original .cnt to mne-compatible format), the required packages are stored in 'requirements\_load\_CNT.txt'. This environment has to be created with python2.  

### A. Using Virtualenvwrapper (requirements.txt):
- mkvirtualenv -p python3 hyper-2.0_env  
- pip install -r requirements.txt

##3 B. Using Anaconda venv (environment.yml):
- conda env create -f environment.yml -n <env_name>


