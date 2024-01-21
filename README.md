# etl_pipeline
an example pipeline getting data, transforming it, and loading it somewhere else

General idea:
Extract data from the NEON dataset and the open_topography dataset, 
Transform the data to be compatible to feed into a normal view for loading
Load data into the natcap model for an output.
    * maybe load model outputs into a database somewhere to train a machine learning model later on?