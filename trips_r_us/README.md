# About Trips Are US(trips_r_us)
This project is all about revolutionizing the way people plan their travels. Our web-based application offers personalized travel planning experiences by generating custom itineraries tailored to user preferences. Whether you're looking for adventure, relaxation, cultural immersion, or culinary experiences, Trips-R-Us makes your travel planning seamless and intuitive. Dive into our code, contribute, or simply explore how we're using Django and cutting-edge technologies to bring personalized travel planning to your fingertips. Join us on this journey to make travel planning easier, smarter, and more personalized than ever before!

## Table of Contents

- [Getting Started](#getting-started)
  - [Clone repository](#clone-repository) 
  - [Set up virtual environment](#virtual-environment)

## Getting Started
### Clone Repository
```shell
git clone https://github.com/dakota-county-technical-college/travel-companion.git
```

### Virtual Environment

A virtual environment in Python is a self-contained directory tree that enables the isolation of dependencies required by a specific project. This isolation ensures that each project can have its own set of libraries or versions of a library, without affecting other projects or the global Python installation on the system. Virtual environments are crucial in managing project-specific dependencies, avoiding version conflicts, and ensuring that projects are reproducible across different machines or deployments. By using virtual environments, developers can work on multiple projects with differing requirements simultaneously, making development workflows more efficient and reliable

_On Mac_

creates the virtual environment folder

```commandline
 python3 -m venv venv
```

activates your virtual environment

```commandline
 . venv/bin/activate
```

install dependencies in requirements.txt

```commandline
pip install -r requirements.txt
```

Install New Dependency

```commandline
 pip install dependency_name
```

packages all the dependencies needed to a file.

```commandline
pip freeze > requirements.txt
```

_On Windows_

creates the virtual environment folder

```commandline
 python3 -m venv venv
```

activates your virtual environment

```commandline
source ./venv/Scripts/activate
```

install dependencies in requirements.txt

```commandline
pip install -r requirements.txt
```

Install New Dependency

```commandline
 pip install dependency_name
```

packages all the dependencies needed to a file.

```commandline
pip freeze > requirements.txt
```