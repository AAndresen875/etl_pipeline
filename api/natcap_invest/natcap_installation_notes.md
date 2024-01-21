# Overview of what has been done so far:
Tried to install w pip:
`pip install natcap.invest`

Then I read [here](https://stackoverflow.com/questions/68011881/how-to-deal-with-the-errors-when-installing-natcap-inve) to try and install gdal seperately. 
`pip install GDAL`
got the following error:
```
Could not find gdal-config. Make sure you have installed the GDAL native library and development headers
```
read the gdal docs [here](https://pypi.org/project/GDAL/). I am not sure how to get that specific thing added. some more info [here](https://gdal.org/api/python_bindings.html):

* going to follow this [tutorial](https://stackoverflow.com/questions/72887400/install-gdal-on-linux-ubuntu-20-04-4lts-for-python)
* did not work, I am going to try and install the repo locally so I can run the requirements.txt in my conda environment
ALSO did not work.

Tried:
* `sudo apt install libgdal-dev`
* `pip install GDAL=="$(gdal-config --version).*"`
* then did: `pip install GDAL` but it said that was already satisfied.
* reran: `pip install natcap.invest` got the following error:
```
Successfully built natcap.invest pygeoprocessing
Failed to build GDAL
ERROR: Could not build wheels for GDAL, which is required to install pyproject.toml-based projects
```

Going to try and see if I can pip install the requirements.txt file that is in the github repo for invest:

* did not work, got the error message:
```
      error: command '/usr/bin/gcc' failed with exit code 1
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for GDAL
  Running setup.py clean for GDAL
Failed to build GDAL
ERROR: Could not build wheels for GDAL, which is required to install pyproject.toml-based projects
```
Tried to read other source docs which suggested: pip install natcap.invest --upgrade-strategy=only-if-needed
got the same error:
```
      error: command '/usr/bin/gcc' failed with exit code 1
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for GDAL
  Running setup.py clean for GDAL
Failed to build GDAL
ERROR: Could not build wheels for GDAL, which is required to install pyproject.toml-based projects
```

pausing, will come back to at a later date:
