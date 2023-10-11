# EKS Tests

Tests to ensure that a cluster has all core applications
installed and configured correctly.

As these are tests connecting to k8s, they cannot be run
by GitHub as part of any CI/CD process.

## Prerequisites

- Ensure you have enabled a python `3.11`

``` bash
#pyenv install 3.11.0
pyenv local 3.11.0
```

- enable virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**WARNING AFTERING INSTALLING REQUIREMENTS.TXT YOU MAY NEED TO CLOSE YOUR TERMINAL AND OPEN IT AGAIN (REMEMBER TO SOURCE BACK INTO THE VENV)**

## Running the tests

- Connect to a AWS:

``` bash
aws sso login --profile <profile>
export AWS_PROFILE=<profile>
```

- Set kubectx to the cluster you wish to test against

```bash
kubectx <cluster>
```

- Run all tests from `tests/eks`:

```bash
pytest
```

### Running a subset of tests

- Run all blueprint tests:

```bash
pytest -m blueprint
```

- Run all cluster tests:

```bash
pytest -m argo
```
