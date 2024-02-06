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

-- Trying to increase timeout for timeout error.
SHOW VARIABLES LIKE "secure_file_priv";
SET GLOBAL net_read_timeout = 120;
SET GLOBAL net_write_timeout = 120;

-- Load data in table.
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_data_cleaned.csv'
INTO TABLE youtube_trending_data
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(video_id, title, publishedAt, channelId, channelTitle, categoryId, trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, Region, region_fk); 

-- Alter publishedAt and trending_date column to date type.
ALTER TABLE youtube_trending_data
MODIFY COLUMN publishedAt DATE;

ALTER TABLE youtube_trending_data
MODIFY COLUMN trending_data DATE;

-- Alter thumbnail_link column to BLOB type.
ALTER TABLE youtube_trending_data
MODIFY COLUMN thumbnail_link BLOB;

-- Create table region_coordinates.
DROP TABLE IF EXISTS region_coordinates;
CREATE TABLE region_coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(2),
    geo_lat DECIMAL(9,6),
    geo_long DECIMAL(9,6)
);

-- Add data in region_coordinates table.
INSERT INTO region_coordinates (region, geo_lat, geo_long) VALUES
-- India: 
('IN', 34.1526, 77.5771),  -- Leh, a far north point in India
('IN', 8.0883, 77.5385),   -- Kanyakumari, the southern tip of India
('IN', 20.593684, 78.962880),  -- India Point 1
-- United States:
('US', 47.6062, -122.3321),-- Seattle, WA (Northwest)
('US', 25.7617, -80.1918), -- Miami, FL (Southeast)
('US', 39.090240, -94.712891), -- US Point 3
-- Great Britain: 
('GB', 57.4788, -4.2247),  -- Inverness, Scotland
('GB', 50.9097, -1.4044),  -- Southampton, southern England
('GB', 56.378051, -2.435973),  -- GB Point 3
-- Canada: 
('CA', 49.2827, -123.1207),-- Vancouver, BC (West)
('CA', 46.8139, -71.2080), -- Quebec City, QC (East)
('CA', 57.130366, -107.346771);-- CA Point 2

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
