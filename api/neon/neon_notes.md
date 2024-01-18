# National Ecological Observatory Network (NEON)

* [Website](https://www.neonscience.org/)
* [Overview of Data and Samples](https://www.neonscience.org/data-samples)
    * useful for data governance
* [Code hub for useful code sorted by launguage](https://www.neonscience.org/resources/code-hub)
* [Introduction to NEON API in Python docs](https://www.neonscience.org/resources/learning-hub/tutorials/neon-api-intro-requests-py)
* [Learning hub with lots of project ideas](https://www.neonscience.org/resources/learning-hub/tutorials)

Querying levels:
* Sites: this is a good starting point if you want a specific area, or use site queries to determine which months a particular data product is available at a given site. You can use a site code and hit the `sites/` endpoint
* Product Querying: If you want a specific product, but aren't sure about the sites or months for which data is available, you can use a product code and hit the `products/` endpoint
*Data querying this is helpful if you have the site, month, and data product code you want to get data for hitting the `data/` endpoint. Alternatively you can construct the data_url with information you get from querying from other levels