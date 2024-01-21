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