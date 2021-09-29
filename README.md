# online-judge
This repository contains code for the event of Reverse Coding held during the techfest of Credenz 20' (21') in my college.

# Description
This project is similar to competitive coding platforms like codechef where the user submits their code and we run it on the server. The user's code is scored according to the number of test cases passed. The backend has been made using Django.

# Installation

Here is a quick guide for installing this project on your PC and hosting it locally:

### 1. Cloning the project

clone the project by the following command:

    git clone https://github.com/deshpandeneil/online-judge.git

### 2. Creating virtual environment

install python3-env and pip (if not already installed) for creating a virtual develpopment envirnoment.

    sudo apt-get install python3-venv python3-pip

create a virtual envirnoment:

    python3 -m venv env

activate the virtual envirnoment:

    source env/bin/activate

### 3. Installing required packages

execute the following command to install all requirements:
    
    cd online-judge/
    pip3 install -r requirements.txt

install all the required sandbox packages using the following commands:

    sudo apt-get install autoconf libtool gperf
    pip3 install cython
    git clone https://github.com/seccomp/libseccomp
    cd libseccomp
    sudo chmod +x autogen.sh
    ./autogen.sh
    ./configure
    make
    sudo make install
    cd src/python/
    
Open the the `setup.py` file and set `version = "2.4.4"` on line 32
    
    python3 setup.py install
    cd ../..
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
    export LD_LIBRARY_PATH
    cd ..

# Running the project on localhost

Before running the code, make sure to create the following directory structure in the project root directory:
```bash
data
├── include
│   ├── sandbox.h
│   └── sandbox.py
├── standard
│   ├── description
│   ├── executable
│   ├── input
│   └── output
└── users_code
```
The `include` directory should already exist in the cloned repository. The `standard` directory contains all details regarding the test cases for the problems.

Here is how the structure of each directory within the `standard` directory must be like:
```bash
.
├── question1
├── question2
├── question3
├── question4
├── question5
└── question6
```
The default number of questions is set to 6 in the [Users/views.py](Users/views.py) file hence 6 directories (one for each question).

Here is the structure for every `question` directory within the 4 `standard` directories:

1. Question directories within `description`
```bash
.
├── quota1.txt
├── quota2.txt
├── quota3.txt
├── quota4.txt
├── quota5.txt
└── quota6.txt
```
The `quota` files must contain the time limit (in seconds) on first line followed by the memory limit (in bytes) on the second line for the selected question.

2. Question directories within `executable`
```bash
.
├── a.out
└── code.cpp
```
The `code.cpp` file must contain the correct code for the selected question. The `a.out` file must be the executable version of the `code.cpp` file.

3. Question directories within `input`
```bash
.
├── input1.txt
├── input2.txt
├── input3.txt
├── input4.txt
├── input5.txt
└── input6.txt
```
The `input` directory must contain `input` files for the total number of test cases. The default number of test cases is set to 6 in the [Users/views.py](Users/views.py). Each `input` file must contain the total number of input values on the first line followed by the actual input values for the constructed test case. Each input value must be on a new line.

4. Question directories within `output`
```bash
.
├── expected_output1.txt
├── expected_output2.txt
├── expected_output3.txt
├── expected_output4.txt
├── expected_output5.txt
└── expected_output6.txt
```
The `output` directory must contain `expected_output` files for the total number of test cases. The default number of test cases is set to 6 in the [Users/views.py](Users/views.py). Each `expected_output` file must contain the total number output values for the constructed test case. Each output value must be on a new line.

The `users_code` directory will get populated automatically as and when users are registered through the registration page present in the project.

Run migrations on the database by executing the following commands:
    
    python3 manage.py makemigrations
    python3 manage.py makemigrations Users
    python3 manage.py migrate

Create an administrator user using the following command:

    python3 manage.py createsuperuser

Finally, start the development server with the following command:

    python3 manage.py runserver

Once localhost has started, go to the `/admin` url and login using the superuser credentials. After logging in, go to `/timer` url and set the time duration for the event (in seconds).

Users can be registered only by the admin via the `/register` url.
