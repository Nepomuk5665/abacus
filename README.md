# abacus
mach eif schnell das:

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

pip3 install selenium webdriver-manager

brew install --cask google-chrome

python3 abacus.py
