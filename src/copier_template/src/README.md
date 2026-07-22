# Setting up a development environment
1. Build the dev container
2. run "uv lock" to generate the uv.lock file
3. Create .env in this folder (with the path src/.env) containing the following variables:
HOST=https://argo-workflows.workflows.diamond.ac.uk/ (to submit to the production repo)
IMAGE= (usually python 3.10)
TOKEN=
NAMESPACE= (the cluster you wish to run the templates on)
AUTH=
