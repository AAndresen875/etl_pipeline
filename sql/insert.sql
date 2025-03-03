-- Insert a farm location in São Paulo, Brazil
INSERT INTO locations (name, location, service_area)
VALUES (
    'Fazenda Boa Vista',
    ST_GeomFromText('POINT(-47.92972 -15.77972)', 4326), -- Coordinates in São Paulo region
    ST_GeomFromText('POLYGON((-47.93972 -15.76972, -47.91972 -15.76972, 
                             -47.91972 -15.78972, -47.93972 -15.78972, 
                             -47.93972 -15.76972))', 4326)
); 

-- Insert specific agricultural fields within the farm
INSERT INTO field_boundaries (location_id, shape, area_hectares, crop_type, last_surveyed)
VALUES (
    (SELECT id FROM locations WHERE name = 'Fazenda Boa Vista'), 
    ST_GeomFromText('POLYGON((-47.93772 -15.77272, -47.92772 -15.77272, 
                             -47.92772 -15.78272, -47.93772 -15.78272, 
                             -47.93772 -15.77272))', 4326),
    25.7,
    'Coffee',
    CURRENT_TIMESTAMP - INTERVAL '2 months'
);

-- Insert another field for the same farm
INSERT INTO field_boundaries (location_id, shape, area_hectares, crop_type, last_surveyed)
VALUES (
    (SELECT id FROM locations WHERE name = 'Fazenda Boa Vista'), 
    ST_GeomFromText('POLYGON((-47.92672 -15.77172, -47.91672 -15.77172, 
                             -47.91672 -15.78172, -47.92672 -15.78172, 
                             -47.92672 -15.77172))', 4326),
    18.3,
    'Sugarcane',
    CURRENT_TIMESTAMP - INTERVAL '1 month'
);