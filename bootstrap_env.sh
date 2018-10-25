#get Python >=3.6 (and pip) for your distribution
#apt-get install python3
#apt-get install pip

pip install --user virtualenv
python -m virtualenv env
#.\env\Scripts\activate #this is the windows version
source env/bin/activate #use this for linux instead
pip install pipenv

pipenv install   # installs all dependencies based on pipfile

# manual installation
#pipenv install matrix-client
