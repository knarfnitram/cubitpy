

# Cubitpy

A `python3` wrapper for Cubit. It is tested with Cubit15.2.

## Code formating

CubitPy uses the python code formatter [black](https://github.com/psf/black).
The testsuite checks if all files are formatted accordingly.

## Installation

Cubitpy is developed with `python3.8`.
Other versions of Python might lead to issues.
It is recommended to use virtual environments with `python`.
On Debian systems the following packages have to be installed
```bash
sudo apt-get install python3-venv python3-dev
```

Now a virtual environment can be created (chose an appropriate directory for this, e.g., `/home/user/opt`)
```bash
python3 -m venv cubitpy-env
```

The created virtual environment can be loaded with
```bash
source cubitpy-env/bin/activate
```

From now on we assume that the virtual enviroment is loaded.
To install `cubitpy` go to the repository root directory
```bash
cd path_to_cubitpy
```

And install `cubitpy` via `pip`
```bash
pip install .
```

If you intend to actively develop `cubitpy`, install it in *editable mode*
```bash
pip install -e .
```

To run CubitPy it is required to set an environment variable with the path to the Cubit directory (on Linux the directory containing the main cubit executable and on MacOS to the binary directory)
```bash
export CUBIT=path_to_cubit_directory
```

(Optional) If the BACI preprocessor `pre_exodus` should be used the path to the executable has to be set
```bash
export BACI_PRE_EXODUS=path_to_pre-exodus
```

To check if everything worked as expected, run the tests from within the `tests` directory
```bash
cd path_to_cubitpy/tests
python testing.py
```
