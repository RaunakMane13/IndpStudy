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
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_data_cleaned_withfk.csv'
INTO TABLE youtube_trending_data
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(video_id, title, publishedAt, channelId, channelTitle, categoryId, trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, Region, region_fk); 
-- (2 min 14.63 sec) for data load.

-- Alter publishedAt and trending_date column to date type.
ALTER TABLE youtube_trending_data
MODIFY COLUMN publishedAt DATE;

ALTER TABLE youtube_trending_data
MODIFY COLUMN trending_date DATE;

ALTER TABLE youtube_trending_data
MODIFY COLUMN thumbnail_link BLOB;

-- Create table region_coordinates.
DROP TABLE IF EXISTS region_coordinates;
CREATE TABLE region_coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    region VARCHAR(2)
);

-- Add data in region_coordinates table.
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_region_coordinates.csv'
INTO TABLE region_coordinates
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(latitude, longitude, region);

-- Add foreign key constraints after adding data.
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

SELECT * FROM youtube_trending_data yt
INNER JOIN region_coordinates rc ON yt.region_fk = rc.id
WHERE rc.region = 'IN';

-- Create index for frequently queried columns to optimize them.
CREATE INDEX idx_region_fk ON youtube_trending_data(region_fk);
CREATE INDEX idx_id ON region_coordinates(id);
CREATE INDEX idx_region ON region_coordinates(region);

ALTER TABLE youtube_trending_data
DROP INDEX idx_region_fk;

ALTER TABLE region_coordinates
DROP INDEX idx_region;

ALTER TABLE region_coordinates
DROP INDEX idx_id;
SHOW CREATE TABLE youtube_trending_data;

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

SELECT COUNT(*),region from region_coordinates
group by region;

SELECT MIN(categoryId) AS MinValue, MAX(categoryId) AS MaxV FROM youtube_trending_data;

-- Create category table.
DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id INT PRIMARY KEY,
    title VARCHAR(255)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_category_cleaned.csv'
INTO TABLE category
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, title);

-- add foreign key constraints after adding data.
ALTER TABLE youtube_trending_data
ADD FOREIGN KEY (categoryId) REFERENCES category(id);
--  (2 min 7.85 sec) time taken.
