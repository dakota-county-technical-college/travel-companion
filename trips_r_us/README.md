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
  - [Workflow Instructions for Contributors](#workflow-instructions-for-contributors)

- [Dealing with Merge Conflics](#dealing-with-merge-conflicts)
  - [Scenario](#scenario)
  - [Steps to Resolve Merge Conflicts](#steps-to-resolve-merge-conflicts)

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

On Windows machines your system's default execution policy will not permit the running of scripts as detailed the [powershell documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)

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

## SOPs

### Branch Naming Conventions

In order to connect with YouTrack, all branches should begin with the YouTrack issue ID, as applicable (ie. "TRU-6")

- For new features, add: `feature-your_initials-featurename` (e.g., `TRU-6 feature-jd-nav-bar`).
- For defects, add: `defect-your_initials-description-of-issue` (e.g., `TRU-81 defect-jd-nav-bar-date_not_converting_as_expected`).
- For patches, add: `patch-your_initials-description-of-patch` (e.g., `TRU-36 patch-jd-date-formatting`).
- For document updates, add `docs-your_initials-description-of-change` (e.g., `TRU-4 updated-readme`).

### Commit Naming Conventions

In order to connect with YouTrack, all commit messages should following the following conventions:

- Begin with your commit message text (e.g., `I did a thing!`).
- Include a pound sign / hashtag followed by the issue ID (e.g., `#TRU-6`).
- If you'd like, include the name of a status the issue should move into (e.g., `Testing`).
- On a new line, include a comment to include in the issue, if you'd like (e.g., `@toddharper Is this thing on?`).
  Altogher, the above commit message would look like:
  I did a thing! #TRU-6 Testing
  @toddharper Is this thing on?

### Workflow Instructions for Contributors

To contribute to the repository, please follow these steps:

Please follow these steps to contribute to the project:

1. **Clone the Repository**: Start by cloning the repository, ensuring you're on the `dev` branch. This is your starting point for any new development.

2. **Create a New Branch**: From the `dev` branch, create a new branch for your work. Make sure to follow our branch naming conventions to keep our repository organized.

3. **Implement Your Changes**: With your new branch checked out, implement your changes. As you make changes, commit them to your branch using our commit naming conventions. This helps maintain a clear and understandable project history.

4. **Open a Pull Request (PR)**: Once your changes are complete, and you've tested your code to ensure it doesn't introduce errors or breaking changes, open a PR to merge your branch back into `dev`. Your PR must be approved by at least two reviewers. The second reviewer will be responsible for merging it into `dev`.

5. **Final Steps**: After your PR has been approved and merged into `dev`, a repository maintainer will take responsibility for creating a PR to merge `dev` into `stage/main`. This step is crucial for backup and further testing before final deployment.

Thank you for contributing to our project! Your efforts help us build and maintain a robust and efficient codebase.

## Dealing with Merge Conflicts

When working with Git, merge conflicts can sometimes occur, especially when multiple people are working on the same parts of a project. This guide will help you resolve merge conflicts in Visual Studio Code (VSCode).

## Scenario

You're working on the branch `feature/jj/userlogin` and encounter a merge conflict when trying to merge into the `dev` branch.

## Steps to Resolve Merge Conflicts

1. **Ensure Your Branch is Up-to-Date**

First, make sure your local `dev` branch is up to date with the remote `dev` branch.

```sh
git checkout dev
git pull origin dev
```

2. **Switch to Your Feature Branch**

Switch back to your feature branch.

```sh
git checkout feature/jj/userlogin
```

3. **Start the Merge Process**

Attempt to merge dev into your feature branch. This is where you might encounter conflicts.

```sh
git merge dev
```

4. **In VSCode:**

The Source Control panel will show merge conflicts.
Click on a conflicted file to open it.
VSCode presents three options for each conflict: Accept Current Change, Accept Incoming Change, Accept Both Changes.
Make your choices for how to resolve each conflict.

5. **Save and Commit**

After resolving all conflicts, save your files in VSCode

```sh
git add .
git commit -m "Resolved merge conflicts merging dev into feature/jj/userlogin"
```

6. **Push Your Changes**

Once conflicts are resolved and committed, you can push your changes back to the remote repository.

```sh
git push origin feature/jj/userlogin
```

[Additional Resources](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)