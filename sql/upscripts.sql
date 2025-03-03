-- Creating the locations table
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location GEOMETRY(Point, 4326),
    service_area GEOMETRY(Polygon, 4326)
);

-- Create spatial index
CREATE INDEX idx_locations_location ON locations USING GIST(location);

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