# Kubernetes Configuration Tests

A collection of python (pytest) tests to ensure that a cluster has all core applications
installed and configured correctly. In this example we have deployed core applications via
`ArgoCD` and `AWS EKS Blueprints` so tests have added marks to allow testing only a specific
source. 

As `ArgoCD` has an application `health` endpoint this has been used to show the health of
all argoCD applications. Note that the deployment of applications to `argocd` has a naming
standard which has been used which includes the kubernetes cluster name (This may need to be
changed in your instance).

While `blueprint` applications have individial resource tests. Where
a health check is possible it, it should be tested, but in most cases, im just looking for a
resource to be on the cluster with the currect name. 

## Prerequisites

Please ensure you have meet the pre-reqs

### Kubernetes

- Have a connection to a kubernetes cluster (access to call API)

### Python

It is presumed that you use `pyenv` to install multiple versions of python, this should run on
most versions of `python3.x` but has only been tested on `3.11`. It also uses `venv` for virtual
environments.

- Ensure you have enabled a python `3.11` in `pyenv`

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
