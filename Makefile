
## env: creates and configures the environment.
## html: build the JupyterBook normally (calling jupyterbook build .). Note this build can only be viewed if the repository is cloned locally, or with the VNC desktop on the Hub.
## clean: clean up the figures, audio and _build folders.

.PHONY : env
env :
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml 
	conda activate ligo
	conda install ipykernel
	python -m ipykernel install --user --name ligo

.PHONY : html
html: 
	jupyter-book build . 

.PHONY : clean
clean: 
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*
