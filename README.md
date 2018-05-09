# **Office Surveillance System** 

## **Basic Function**

**1. Web Video Streaming(to do)**

**2. Motion Detection**

**3. Face Detection**

**4. Face Recognition**

**5. Face Images Collection**

**6. KNN Classifier Training**

**7. Update MySQL Server with(NAME, DATETIME, ACTION)**

**8. Communicate with other hosts(to do)**

**9. Alert(to do)**

**...**
  
## **Usage**

**Normal Usage(surveillance and face recognition):**
- python3 surveillance.py

**Train a new classifier when face images databse changed:**
- python3 surveillance.py -t

**Collect face images for training and saving:**
- python3 surveillance.py -c

**Show help text:**
- python3 surveillance.py -h

**Press 'q' for quit program**

## **Installation**

**Requirements**
- Python3.3+ (Recommend Python3.6)
- Ubuntu(16.04+)/Linux

**Steps:**

- Install Dlib(http://dlib.net/) with Python3 bindings

Install dependancy(pass in Linux/Ubuntu):

```

sudo apt-get update

sudo apt-get install python3-pip\

    build-essential \

    cmake \

    gfortran \

    git \

    wget \

    curl \

    graphicsmagick \

    libgraphicsmagick1-dev \

    libatlas-dev(change to libatlas-base-dev for Ubuntu 18.04) \

    libavcodec-dev \

    libavformat-dev \

    libgtk2.0-dev \

    libjpeg-dev \

    liblapack-dev \

    libswscale-dev \

    pkg-config \

    python3-dev \

    python3-numpy \

    software-properties-common \

    zip \

sudo apt-get clean && rm -rf /tmp/* /var/tmp/*

pip3 install setuptools

```

Clone the code from github:

```

git clone https://github.com/davisking/dlib.git

```

Build the main dlib library:
```

cd dlib

mkdir build; cd build; cmake .. -DDLIB_USE_CUDA=0 -DUSE_AVX_INSTRUCTIONS=1; cmake --build .

```

Build and install the Python extensions:

```

cd ..

python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA

```

At this point, you should be able to run ```python3``` and type ```import dlib``` successfully.

- Install face_recognition library:

```

pip3 install face_recognition

```

- Install necessary Python libary to import:

```

pip3 install opencv-python

pip3 install pymysql

pip3 install scipy

pip3 install imutils

pip3 install sklearn

pip3 install numpy

```

- Clone source code from SAT GIT REPOSITORY:

Downlad SurveillanceSystem source code from
http://sat-git.starasiatrading.com/bonobo/Repository



*7 May 2018*
