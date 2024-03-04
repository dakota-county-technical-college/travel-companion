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
- [SOPs](#sops)
  - [Branch Naming Conventions](#branch-naming-conventions)
  - [Commit Naming Conventions](#commit-naming-conventions)

## Getting Started

### Clone Repository

To get started, clone the repository to your local machine from the `dev` branch:

```shell
git clone -b dev https://github.com/dakota-county-technical-college/travel-companion.git
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

## SOPs

### Branch Naming Conventions

In order to connect with YouTrack, all branches should begin with the YouTrack issue ID, as applicable (ie. "TRU-6")

- For new features, add: `feature-your_initials-featurename` (e.g., `TRU-6 feature-jd-nav-bar`).
- For defects, add: `defect-your_initials-description-of-issue` (e.g., `TRU-81 defect-jd-nav-bar-date_not_converting_as_expected`).
- For patches, add: `patch-your_initials-description-of-patch` (e.g., `TRU-36 patch-jd-date-formatting`).

### Commit Naming Conventions

In order to connect with YouTrack, all commit messages should following the following conventions:

- Begin with your commit message text (e.g., `I did a thing!`).
- Include a pound sign / hashtag followed by the issue ID (e.g., `#TRU-6`).
- If you'd like, include the name of a status the issue should move into (e.g., `Testing`).
- On a new line, include a comment to include in the issue, if you'd like (e.g., `@toddharper Is this thing on?`).
  Altogher, the above commit message would look like:
  I did a thing! #TRU-6 Testing
  @toddharper Is this thing on?

### Contribution Workflow
To contribute to the repository, please follow these steps:

- Clone the repository from the dev branch.
- Create a new branch from dev following the branch naming conventions.
- Implement your changes and commit them following the commit naming conventions.
- Open a pull request (PR) to merge your branch back into dev. This PR requires approval from at least 2 reviewers.
- Once approved and merged into dev, a repository maintainer will create a PR to merge dev into stage for further testing. This PR requires approval from at least 1 reviewer.
- After successful testing in stage, a final PR will be made to merge stage into main (production). This PR requires approval from at least 1 reviewer.


Pair Programming
For pair programming contributions:

- Include at least one person from the pair in the branch name, using their initials.
- One of the reviewers must be a part of the project's owners.
- Ensure that all commits are co-authored, including both contributors' names and email addresses in the commit message.
This workflow ensures a structured and review-centric development process, fostering high-quality code and collaboration.
