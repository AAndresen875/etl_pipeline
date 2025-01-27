# etl_pipeline
an example pipeline getting data, transforming it, and loading it somewhere else

General idea:
Extract data from the NEON dataset and the open_topography dataset, 
Transform the data to be compatible to feed into a normal view for loading
Load data into the natcap model for an output.
    * maybe load model outputs into a database somewhere to train a machine learning model later on?

# generation 2:
* create a postgressql database, with postGIS with it
* pull topo data and put it in the database,
* pull neon data and put it in a database
* do spatial join for an attribute table within the database
* some sort of viewer like geopandas or geojupyter

