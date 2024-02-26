# About Trips Are US (trips_r_us)
This project is all about revolutionizing the way people plan their travels. Our web-based application offers personalized travel planning experiences by generating custom itineraries tailored to user preferences. Whether you're looking for adventure, relaxation, cultural immersion, or culinary experiences, Trips-R-Us makes your travel planning seamless and intuitive. Dive into our code, contribute, or simply explore how we're using Django and cutting-edge technologies to bring personalized travel planning to your fingertips. Join us on this journey to make travel planning easier, smarter, and more personalized than ever before!

## Table of Contents

- [Getting Started](#getting-started)
  - [Clone Repository](#clone-repository)
  - [Setup Virtual Environment](#setup-virtual-environment)
  - [Activate Virtual Environment](#activate-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Install New Dependency](#install-new-dependency)
  - [Package Dependencies](#package-dependencies)

## Getting Started
### Clone Repository

To get started, clone the repository to your local machine:

```shell
git clone https://github.com/dakota-county-technical-college/travel-companion.git
```

### Setup Virtual Environment
For both windows and mac:
```shell
python3 -m venv venv
```

### Activate Virtual Environment
Depending on your operating system, activate the virtual environment using the appropriate command:
For Mac:
```shell
. venv/bin/activate
```

For Windows:
```shell
source ./venv/Scripts/activate
```

On Windows machines your system's default execution policy will not permit the running of scripts as detailed  the [powershell documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)

To change your execution policy within the scope of your user run the command:
```shell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Dependencies
Install the project dependencies as specified in requirements.txt:
```shell
pip install -r requirements.txt
```

### Install New Dependency
To add a new dependency to the project:
```shell
pip install <dependency_name>
```
### Package Dependencies
Remember to update requirements.txt with the new dependency
```shell
pip freeze > requirements.txt
```