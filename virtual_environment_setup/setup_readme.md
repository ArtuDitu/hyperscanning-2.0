# Virtual environment Setup:
The following commands will create a virtual environment with the same packages / version as used during development of the script. The necessary information is specified in 'requirements.txt' and 'environment.yml'

## 1 Using Virtualenvwrapper (requirements.txt):
pip install -r requirements.txt

## 2 Using Anaconda venv (environment.yml):
conda env create -f environment.yml -n <env_name>
