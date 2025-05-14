echo [$(date)]: "START"

echo [$(date)]: "Creating env with python 3.10 version"

conda create --prefix ./env python=3.10 -y

echo [$(date)]: "activating the environment"

source activate ./env

echo [$(date)]: "Installing the requirements"

pip install -r requirements.txt

echo [$(date)]: "End"