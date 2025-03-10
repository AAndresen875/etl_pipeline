class OpenTopographyAPI:
    """
    A class to interact with the OpenTopography API.

    Attributes:
        server_url (str): The base URL for the OpenTopography API.
        api_key (str): The API key for authentication.

    Methods:
        __init__(server_url, api_key): Initializes the OpenTopographyAPI with the given server URL and API key.
    """

    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key

    def download_data_from_url(self, request_url: str, output_directory: str) -> str:
        """
        Download data from a given URL and save it to a file.

        :param url: The URL of the data to download.
        :param output_file: The name of the file to save the data to.
        :param api_key: The API key for authentication.
            USGS 3DEP 1m raster dataset is currently restricted to academic users. Academic users can request
            access to these data via the OpenTopography portal. Non-academic users can enquire about an
            enterprise API key by emailing info@opentopography.org.
            * See OpenTopography Terms of Use for more information on appropriate use of the API.

            Default value : demoapikeyot2022
        :return: The path to the downloaded file.

        Code:Description
        200:OK
        204:No Data
        400:Bad request
        401:Unauthorized
        500:Internal error
        """
        # Make the request
        response = requests.get(request_url)

        # generate the file extension
        if response.headers["Content-Type"] == "image/tiff":
            file_extension = ".tif"
        # TODO: Add more file extensions here
        else:
            file_extension = ".dat"

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the filename from the response headers
            content_disposition = response.headers.get("content-disposition")
            if content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            else:
                filename = f"downloaded_data.{file_extension}"

            # Create the full path to the output file
            output_path = os.path.join(output_directory, filename)

            # Write the content to the file
            with open(output_path, "wb") as file:
                file.write(response.content)

            print(f"File downloaded successfully and saved to {output_path}")
        elif response.status_code == 204:
            print("No data available for the specified request.")
            output_path = None
        elif response.status_code == 400:
            print("Bad request. Please check the request parameters.")
            output_path = None
        elif response.status_code == 401:
            print("Unauthorized. Please check your API key.")
            output_path = None
        elif response.status_code == 500:
            print("Internal server error. Please try again later.")
            output_path = None
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

        return output_path


class GlobalDEM(OpenTopographyAPI):
    """ """

    def __init__(self, server_url: str, api_key: str):
        """
        Initialize the GlobalDEM class with the given server URL and API key.

        :param server_url: The base URL for the OpenTopography API.
        :param api_key: The API key for authentication.
        """
        super().__init__(server_url, api_key)
        self.endpoint_code = "globaldem/"

    def construct_request_url(
        self,
        demtype_code: str,
        south: str,
        north: str,
        west: str,
        east: str,
        output_format: str,
    ) -> str:
        """
        Construct the request URL for the GlobalDEM endpoint.

        :param demtype_code: The type of DEM requested.
            Available global raster datasets:
            SRTMGL3 (SRTM GL3 90m)
            SRTMGL1 (SRTM GL1 30m)
            SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)
            AW3D30 (ALOS World 3D 30m)
            AW3D30_E (ALOS World 3D Ellipsoidal, 30m)
            SRTM15Plus (Global Bathymetry SRTM15+ V2.1 500m)
            NASADEM (NASADEM Global DEM)
            COP30 (Copernicus Global DSM 30m)
            COP90 (Copernicus Global DSM 90m)
            EU_DTM (DTM 30m)
            GEDI_L3 (DTM 1000m)
            GEBCOIceTopo (Global Bathymetry 500m)
            GEBCOSubIceTopo (Global Bathymetry 500m)
        :param south: Southern boundary at latitude.
            WGS 84 bounding box south coordinates; Example : 50
        :param north: Northern boundary at latitude.
            WGS 84 bounding box north coordinates: Example : 50.1
        :param west: Western boundary at longitude.
            WGS 84 bounding box west coordinates: Example : 14.35
        :param east: Eastern boundary at longitude.
            WGS 84 bounding box east coordinates: Example : 14.6
        :param output_format: The format of the output file.
            Output Format (optional) - GTiff for GeoTiff, AAIGrid for Arc ASCII Grid, HFA for Erdas Imagine (.IMG). Defaults to GTiff if parameter is not provided
            Available values : GTiff, AAIGrid, HFA
            Default value : GTiff
            Example : GTiff
        :return: The constructed request URL.

        """
        # TODO: break into lines
        request_url = f"""{self.server_url}{self.endpoint_code}?demtype={demtype_code}&south={south}&north={north}&west={west}&east={east}&outputFormat={output_format}&API_Key={self.api_key}"""
        return request_url


class USGSDem(OpenTopographyAPI):
    def __init__(self, server_url: str, api_key: str):
        """
        Initialize the USGSDem class with the given server URL and API key.

        :param server_url: The base URL for the OpenTopography API.
        :param api_key: The API key for authentication.
        """
        super().__init__(server_url, api_key)
        self.endpoint_code = "usgsdem/"

    def construct_request_url(
        self,
        dataset_name: str,
        south: float,
        north: float,
        west: float,
        east: float,
        output_format: str,
    ) -> str:
        """
        Construct the request URL for the USGS DEM endpoint.

        :param dataset_name: The name of the dataset to request.
        :param south: The southern boundary at latitude.
        :param north: The northern boundary at latitude.
        :param west: The western boundary at longitude.
        :param east: The eastern boundary at longitude.
        :param output_format: The format of the output file.
            Output Format (optional) - GTiff for GeoTiff, AAIGrid for Arc ASCII Grid, HFA for Erdas Imagine (.IMG). Defaults to GTiff if parameter is not provided.
        :return: The constructed request URL.
        """
        request_url = f"""{self.server_url}{self.endpoint_code}?dataset={dataset_name}&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={self.api_key}"""
        return request_url


class OTCatalog(OpenTopographyAPI):
    def __init__(self, server_url: str, api_key: str):
        """
        Initialize the OTCatalog class with the given server URL and API key.

        :param server_url: The base URL for the OpenTopography API.
        :param api_key: The API key for authentication.
        """
        super().__init__(server_url, api_key)
        self.endpoint_code = "otCatalog/"

    def download_data_from_url(self, request_url: str, output_directory: str) -> str:
        """
        Download data from a given URL and save it to a file.
        Overwriting base class method bc this method doesn't have a 401 response

        :param url: The URL of the data to download.
        :param output_file: The name of the file to save the data to.
        """
        # Make the request
        response = requests.get(request_url)

        # generate the file extension
        if response.headers["Content-Type"] == "image/tiff":
            file_extension = ".tif"
        elif response.headers["Content-Type"] == "application/zip":
            file_extension = ".zip"
        else:
            file_extension = ".dat"

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the filename from the response headers
            content_disposition = response.headers.get("content-disposition")
            if content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            else:
                filename = f"downloaded_data.{file_extension}"

            # Create the full path to the output file
            output_path = os.path.join(output_directory, filename)

            # Write the content to the file
            with open(output_path, "wb") as file:
                file.write(response.content)

            print(f"File downloaded successfully and saved to {output_path}")
        elif response.status_code == 204:
            print("No data available for the specified request.")
            output_path = None
        elif response.status_code == 400:
            print("Bad request. Please check the request parameters.")
            output_path = None
        elif response.status_code == 500:
            print("Internal server error. Please try again later.")
            output_path = None
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

        return output_path
