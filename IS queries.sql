-- Create database IndStd.
DROP DATABASE IF EXISTS IndStd;
CREATE DATABASE IndStd;
USE IndStd;

-- Create table youtube_trending_data.
DROP TABLE IF EXISTS youtube_trending_data;
CREATE TABLE youtube_trending_data (
	id BIGINT auto_increment Primary Key,
    video_id VARCHAR(255),
    title TEXT,
    publishedAt varchar(35),
    channelId VARCHAR(255),
    channelTitle TEXT,
    categoryId INT,
    trending_date varchar(35),
    tags TEXT,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link TEXT,
    comments_disabled TEXT,
    ratings_disabled TEXT,
    description TEXT,
    Region VARCHAR(255),
    region_fk INT
);

-- Load data in table.
LOAD DATA LOCAL INFILE '/home/student/Downloads/merged_data_cleaned_withfk.csv'
INTO TABLE youtube_trending_data
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(video_id, title, publishedAt, channelId, channelTitle, categoryId, trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, Region, region_fk); 

ALTER TABLE youtube_trending_data
ADD COLUMN image_id BIGINT NOT NULL;

SET @counter = 0;
UPDATE youtube_trending_data
SET image_id = (@counter:= @counter +1)
ORDER BY id;

ALTER TABLE youtube_trending_data
ADD CONSTRAINT fk_image_id
FOREIGN KEY (image_id) REFERENCES images(id);

-- Trying to increase timeout for timeout error.
SHOW VARIABLES LIKE "secure_file_priv";
SET GLOBAL net_read_timeout = 120;
SET GLOBAL net_write_timeout = 120;

-- Alter publishedAt and trending_date column to date type.
ALTER TABLE youtube_trending_data
MODIFY COLUMN publishedAt DATE;

ALTER TABLE youtube_trending_data
MODIFY COLUMN trending_data DATE;

-- Create table region_coordinates.
DROP TABLE IF EXISTS region_coordinates;
CREATE TABLE region_coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    region VARCHAR(2)
);

-- Add data in region_coordinates table.
LOAD DATA LOCAL INFILE '/home/student/Downloads/merged_region_coordinates.csv'
INTO TABLE region_coordinates
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(latitude, longitude, region);

-- Add foreign key constraints.
ALTER TABLE youtube_trending_data
ADD CONSTRAINT fk_region_coordinates
FOREIGN KEY (region_fk) REFERENCES region_coordinates(id);

-- Drop region column to remove redundancy. 
ALTER TABLE youtube_trending_data
DROP COLUMN Region;

-- Sample queries.
SELECT Count(*) FROM youtube_trending_data
JOIN region_coordinates ON youtube_trending_data.region_fk = region_coordinates.id
WHERE region_coordinates.region = 'IN';

SELECT COUNT(*) FROM youtube_trending_data yt
INNER JOIN region_coordinates rc ON yt.region_fk = rc.id
WHERE rc.region = 'IN';

-- Create index to optimize queries
CREATE INDEX idx_region_fk ON youtube_trending_data(region_fk);
CREATE INDEX idx_id ON region_coordinates(id);
CREATE INDEX idx_region ON region_coordinates(region);

-- Queries to find non-ascii containing records
SELECT * FROM youtube_trending_data
WHERE title REGEXP '[^\x00-\x7F]'
   OR description REGEXP '[^\x00-\x7F]'
   OR tags REGEXP '[^\x00-\x7F]'
   OR channelTitle REGEXP '[^\x00-\x7F]';

WITH NonAsciiRows AS (
    SELECT *
    FROM youtube_trending_data
    WHERE title REGEXP '[^\x00-\x7F]'
       OR description REGEXP '[^\x00-\x7F]'
       OR tags REGEXP '[^\x00-\x7F]'
       OR channelTitle REGEXP '[^\x00-\x7F]'
)
SELECT *
FROM NonAsciiRows;

-- Create a new column to assign indices.
ALTER TABLE youtube_trending_data
ADD COLUMN has_non_ascii BOOLEAN DEFAULT FALSE;

UPDATE youtube_trending_data
SET has_non_ascii = 
    (title REGEXP '[^\x00-\x7F]' OR
    description REGEXP '[^\x00-\x7F]' OR
    tags REGEXP '[^\x00-\x7F]' OR
    channelTitle REGEXP '[^\x00-\x7F]');

-- Set indices.
CREATE INDEX idx_has_non_ascii ON youtube_trending_data(has_non_ascii);

-- Optimized query to find non-ascii records.
SELECT *
FROM youtube_trending_data
WHERE has_non_ascii = TRUE;

-- Create category table
DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id INT PRIMARY KEY,
	title VARCHAR(30)
);

-- Add data in region_coordinates table.
LOAD DATA LOCAL INFILE '/home/student/Downloads/merged_category_cleaned.csv'
INTO TABLE category
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id,title);

-- Add foreign key constraints.
ALTER TABLE youtube_trending_data
ADD CONSTRAINT fk_category
FOREIGN KEY (categoryId) REFERENCES category(id);

-- geospatial queries to find records within a range.
SELECT id, region, ST_Distance_Sphere( POINT(longitude, latitude), POINT(-122.4194, 37.7749)) AS distance_in_meters
FROM region_coordinates
HAVING distance_in_meters <= 10000
ORDER BY distance_in_meters;

SELECT COUNT(yt.id) number_of_trending_v, c.title
FROM youtube_trending_data yt JOIN region_coordinates r ON yt.region_fk = r.id JOIN category c ON c.id = yt.categoryId
WHERE ST_Distance_Sphere( POINT(r.longitude, r.latitude), POINT(-122.4194, 37.7749)) <= 10000
GROUP BY c.title
ORDER BY number_of_trending_v DESC;

SELECT yt.video_id, yt.title, rc.region, rc.latitude, rc.longitude
FROM youtube_trending_data AS yt
JOIN region_coordinates AS rc ON yt.region_fk = rc.id
WHERE rc.latitude BETWEEN 30.0 AND 60.0 AND rc.longitude BETWEEN -130.0 AND -100.0 AND rc.region = 'CA';

-- Create images table.
DROP TABLE IF EXISTS images;
CREATE TABLE images(
	image_id INT PRIMARY KEY,
    image BLOB
);

ALTER TABLE images 
CHANGE COLUMN image_id id BIGINT;
