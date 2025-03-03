# Installing the OpenTopography API
[Official Overview on Website; ](https://opentopography.org/developers)
[ Official API Documentation](https://portal.opentopography.org/apidocs/)
## Requesting an API KEY:
1. Go to https://opentopography.org/
2. Select the tab: "MyOpenTOPO"
3. Create an account by selecting the button under the login button called "Create New Account"
4. Fill out fields, verify email
5. Request an API key in the MyOpenTopo dashboard
6. Add API key to your environment variable
* I will be adding to my bashrc file:
```
nano ~.bashrc
```
Then when the bashrc file opens add the line
```
# <<< conda initialize <<<
export OPEN_TOPO_API_KEY="your_api_key"
```
replacing "your_api_key" with your api key
save and write out 
for nano: cntrl + S, cntrl + X

then activate your changes by doing:
```
source ~/.bashrc
```
reactivate the environment via: 
`conda activate your-enviro-name`

now when wanting to pass this credential into your script, you can call it via: `os.environ['OPEN_TOPO_API_KEY']`

## example of some data for the call:
""" 
that covers a small area in the Czech Republic, specifically around the city of Prague. T
he approximate central point of this bounding box is at latitude 50.05 and longitude 14.475.

This central point is located in the vicinity of Prague, the capital city of the Czech Republic. 
An approximate address for this location would be:
Prague, Czech Republic
"""

Sample data for prague:
south_number = "-70" # Southern boundary at latitude 50.0 degrees
north_number = "-5.1" # Northern boundary at latitude 50.1 degrees.
west_number = "-34.35" # Western boundary at longitude 14.35 degrees.
east_number = "-74.6" # Eastern boundary at longitude 14.6 degrees.