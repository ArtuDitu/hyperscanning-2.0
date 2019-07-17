# Virtual environment Setup:
The following commands will create a virtual environment with the same packages / version as used during development of the script.  
For the "hyper-2.0_env" (used to run main preprocessing-script), the necessary information is specified in 'requirements.txt' and 'environment.yml'.  
For the "load_cnt" environment (used to convert original .cnt to mne-compatible format), the required packages are stored in 'requirements\_load\_CNT.txt'


## 1. Using Virtualenvwrapper (requirements.txt):
pip install -r requirements.txt

## 2. Using Anaconda venv (environment.yml):
conda env create -f environment.yml -n <env_name>
