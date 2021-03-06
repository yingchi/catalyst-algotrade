# Catalyst Algotrade
This repo is to experiment trading strategies in Python using Catalyst library.
For the full documentation of Catalyst, please refer to their [official repo](https://github.com/enigmampc/catalyst).

The jupyter notebooks will be run in the IPython Notebook environment for fast and interactive feedback and analysis.

The python scripts will be run in a command-line interface (CLI) or a python IDE (IDEA or PyCharm recommended).

The setup instructions of the above 2 environments are below.

> Note: I use MacOS, Anaconda and Python 3.6. For other settings, please refer to Catalyst's 
[installation manual](https://enigma.co/catalyst/install.html)


## Installation 

The two running environments both require we install Catalyst first. It is recommended to install 
it in a separate virtual environment. 

Download this repo. Then

```shell
cd ~/Documents/github/catalyst-algotrade
conda env create -f etc/python3.6-environment.yml
```
This step will take a while, as the config file will download the catalyst library and all the dependencies of it.

Now, if you want to use Catalyst in CLI mode, then activate the environment by:

```shell
source activate catalyst
```
And run the `catalyst run` commands to execute the strategies. Details, please refer to 
[running the algorithm in CLI](https://enigma.co/catalyst/beginner-tutorial.html#running-the-algorithm)

But if you want to use one of the recommended two (IPython Notebook or PyCharm IDE), you do not need 
to keep the virtual environment active all the time. Refer to the following for respective 
instructions.


### 1. IPython Notebook
Something you need to know about Python virtual environment and IPython Kernels:
The set of ipython kernels available are independent of what your virtualenv is when you start jupyter Notebook. The trick is setting up the the ipykernel package in the environment you want to identify itself uniquely to jupyter.

Thus, to use Catalyst in IPython Notebook, we need to do the following:

```shell
source activate catalyst
conda install ipykernel
```
Now, fire up `jupyter notebook` (you can exit the virtual environment if you want, it does not matter), you will see a kernel with "Python [conda env: catalyst]". And you are able to run the notebooks in this repo.

### 2. PyCharm IDE
If you prefer to use IntelliJ IDEA, follow these steps to configure the python environment for 
the project. 

1. Open the folder in the IDE
2. "File" -> "Project Structure"
3. "Project Settings: Project" -> "Project SDK" -> "New" -> "Python SDK" -> "Add local" 
4. Choose "Existing environment" -> select the python executor path for your `catalyst` env. 
For example, it looks like this for me `Users/yingchipei/anaconda3/envs/catalyst/bin/python`
5. "Project Settings: Project" -> "Platform Settings" -> choose the "Python 3.6 (catalyst)"

Done


## Run the examples
Before running the actually code, make sure you have ingested the data bundles used first 
```shell
source activate catalyst
catalyst ingest-exchange -x poloniex -f daily -i btc_usdt
catalyst ingest-exchange -x poloniex -f minute -i btc_usdt
```

### 1. IPython Notebook
```shell
cd ~/Documents/github/catalyst-algotrade
jupyter notebook
```
Then go to the `notebook/example-dma.ipynb` and run the cells


### 2. PyCharm IDE
Open "Terminal" in IDE, then
```shell
cd ~/Documents/github/catalyst-algotrade
python scripts/example-dma.py
```
Then you will see a subplot popping up to show you the backtesting result.









