# Notes created when setting up the database

# Installation:

## Confirming no previous installation:
* confirmed postgres wasn't already installed with `psql --version`; output: `Command 'psql' not found, but can be installed with:
sudo apt install postgresql-client-common`

### Understanding different installation commands 
I found a few installation commands and I want to understand the differences and which to use, this was generated with AI and here are the notes:
### PostgreSQL Installation Commands Explained

When working with PostgreSQL, it's important to understand the different installation packages and what they provide:

- `sudo apt install postgresql-client-common`
    
    This command installs only the common files needed for PostgreSQL client applications. It includes:
    
    - Basic client utilities shared across different PostgreSQL versions
    - Common libraries required by PostgreSQL clients
    - Configuration files used by client applications
    
    This package doesn't install the actual PostgreSQL server or full client applications. It's useful when you only need to connect to a remote PostgreSQL database without hosting a database locally.
    
- `sudo apt install postgresql postgresql-contrib`
    
    This command provides a complete PostgreSQL installation including:
    
    - The full PostgreSQL server (database engine)
    - Client applications to interact with the server
    - Core database functionality
    - Additional modules and extensions (postgresql-contrib) that add extra features
    
    The postgresql-contrib package includes popular extensions like:
    
    - uuid-ossp: For UUID generation
    - pg_stat_statements: For query performance monitoring
    - ltree: For hierarchical data structures
    - hstore: For key-value pair storage
    
    This combination is recommended for a full development or production environment where you need to run the database server locally.
    

### Which Command to Use?

Choose based on your needs:

- **Client-only (postgresql-client-common):** When you only need to connect to existing PostgreSQL servers
- **Full installation (postgresql postgresql-contrib):** When you need to host databases locally and want access to all features

For most geospatial development environments, the full installation with PostGIS is recommended:
```bash
# Full PostgreSQL with extensions and PostGIS for spatial capabilities
sudo apt install postgresql postgresql-contrib postgresql-14-postgis-3
```

I will be going with the one that also installs the geospatial package: `sudo apt install postgresql postgresql-contrib postgresql-14-postgis-3`

# Steps:
1. made sure the system was updated
    * `sudo apt update`
    * `sudo apt upgrade`
2. installed PostgreSql and PostGIS extention: 
    * `sudo apt install postgresql postgresql-contrib postgresql-14-postgis-3`
3. starting the PostgreSQL service
    * `sudo service postgresql start`
4. checked to see if there were users already in the system
    * `\du`
5. switch to postgres user:
    * `sudo -i -u postgres`
    * this changed the front of the line to `postgres@Echinacea:~$`
6. switch to PostgreSQL command prompt:
    * `psql`
    * this changed the front of the line to `postgres=#`
7. checked for users with the following query:
    * ```
        SELECT usename AS role_name,
        CASE
        WHEN usesuper AND usecreatedb THEN
            CAST('superuser, create database' AS pg_catalog.text)
        WHEN usesuper THEN
            CAST('superuser' AS pg_catalog.text)
        WHEN usecreatedb THEN
            CAST('create database' AS pg_catalog.text)
        ELSE
            CAST('' AS pg_catalog.text)
        END role_attributes
        FROM pg_catalog.pg_user
        ORDER BY role_name desc;
    * output:
    ``` 
    role_name |      role_attributes
    -----------+----------------------------
    postgres  | superuser, create database
    (1 row)
    ```
    * [doc](https://www.geeksforgeeks.org/how-to-list-all-users-in-postgresql/)
8. Checked for any databases:
    * `\l`
    * output: 
    ```
                                    List of databases
    Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges
    -----------+----------+----------+---------+---------+-----------------------
    postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 |
    template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
            |          |          |         |         | postgres=CTc/postgres
    template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
            |          |          |         |         | postgres=CTc/postgres
    (3 rows)
9. Created a new database:
    * `CREATE DATABASE field_mrv;`
10. connected to the database we just created:
    * `\c field_mrv`
    * this changed the start of the line to `field_mrv=#`
11. Check for any tables in this database (shouldn't be: `\dt`)
    * output: `Did not find any relations.`
12. Create a table called "location"
    * ```
        CREATE TABLE locations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        location GEOMETRY(Point, 4326),
        service_area GEOMETRY(Polygon, 4326)
        );
        ```
        * got an error saying Geometry wasn't allowed as a datatype.
            * confirmed that postgis was installed as an extention with: `SELECT * FROM pg_available_extensions;`
                * output contained geospatial PostGIS stuff
                * got out of that window with `\q`
            * checked if it was enabled on this datase with: `SELECT * FROM pg_extension;`
            the only thing enabled was plpsql
            * enabled this extention for this database with `CREATE EXTENSION postgis;`
            * re-ran  `SELECT * FROM pg_extension;`
            * confirmed the POSTGIS extention was installed, got out with `\q`
    * create a spatial index:
        * `CREATE INDEX idx_locations_location ON locations USING GIST(location);`
13. confirmed the creation of the table with `\dt`
    * 2 tables were found:
    ```              
    List of relations
    Schema |      Name       | Type  |  Owner
    --------+-----------------+-------+----------
    public | locations       | table | postgres
    public | spatial_ref_sys | table | postgres
    ```
14. created the field_boundaries table with: 
```
-- Create the field_boundaries table
CREATE TABLE field_boundaries (
    boundary_id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    shape GEOMETRY(Polygon, 4326),
    area_hectares FLOAT,
    crop_type VARCHAR(100),
    last_surveyed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    soil_type VARCHAR(50),
    elevation_avg FLOAT,
    CONSTRAINT fk_location 
        FOREIGN KEY(location_id) 
        REFERENCES locations(id)
        ON DELETE CASCADE
);

-- Create spatial index on the shape field
CREATE INDEX idx_field_boundaries_shape ON field_boundaries USING GIST(shape);

-- Add index on crop_type for quick filtering
CREATE INDEX idx_field_boundaries_crop ON field_boundaries(crop_type);

-- Add timestamp tracking for record management
ALTER TABLE field_boundaries ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE field_boundaries ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```
15. recording the table's upscripts in the file `sql/upscripts.sql`