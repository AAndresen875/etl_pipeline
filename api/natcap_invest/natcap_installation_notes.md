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

1/21/2024: going to pause on this api and come back to it when I have a specific use.