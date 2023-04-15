name: deploy-book

# Only run this when the master branch changes
on:
  push:
    branches:
    - main

# This job installs dependencies, build the book, and pushes it to `gh-pages`
jobs:
  deploy-book:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    # Install dependencies
    - name: Set up Python 3.9
      uses: actions/setup-python@v1
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        pip install -r book-requirements.txt
    # Build the book
    - name: Build the book
      run: |
        jupyter-book build .
    # Push the book's HTML to github-pages
    - name: GitHub Pages action
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_build/html
        
        
## env : creates and configures the environment
## html : build the JupyterBook normally (calling `jupyterbook build .`). Note this build can only be viewed if the repository is cloned locally, or with the VNC desktop on the Hub.
## clean : clean up the `figures`, `audio`  and `_build` folders.
.PHONY: env html clean

env:
    conda env create -f environment.yml
    conda activate ligo
    python -m ipykernel install --user --name=ligo

html:
    jupyter-book build .

clean:
    rm -rf figures audio _build