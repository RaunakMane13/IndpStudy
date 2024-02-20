#!/usr/bin/env python
# coding: utf-8

# # Upload each file separately to add region

# In[1]:


# Specify the path to your CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_youtube_trending_data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())
print(df.dtypes)

df['Region'] = 'US'
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_youtube_trending_data_with_region.csv'
df.to_csv(output_csv_path, index=False)


# In[12]:


# Specify the path to your CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_youtube_trending_data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())
print(df.dtypes)

df['Region'] = 'IN'
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_youtube_trending_data_with_region.csv'
df.to_csv(output_csv_path, index=False)


# In[9]:


# Specify the path to your CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_youtube_trending_data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())
print(df.dtypes)

df['Region'] = 'CA'
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_youtube_trending_data_with_region.csv'
df.to_csv(output_csv_path, index=False)


# In[14]:


# Specify the path to your CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GB_youtube_trending_data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())
print(df.dtypes)

df['Region'] = 'GB'
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GB_youtube_trending_data_with_region.csv'
df.to_csv(output_csv_path, index=False)


# # Merge all csv files 

# In[16]:


import pandas as pd

# Replace these file paths with the paths to your CSV files
file_paths = [
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_youtube_trending_data_with_region.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GB_youtube_trending_data_with_region.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_youtube_trending_data_with_region.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_youtube_trending_data_with_region.csv'
]

# Read each CSV file into a separate DataFrame
dfs = [pd.read_csv(file) for file in file_paths]

# Concatenate the DataFrames along the rows (axis=0)
merged_df = pd.concat(dfs, ignore_index=True)

# Display the first few rows of the merged DataFrame
print("Merged DataFrame:")
print(merged_df.head())

# Save the merged DataFrame to a new CSV file
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data.csv'
merged_df.to_csv(output_csv_path, index=False)

# Display the path of the saved file
print(f"\nMerged DataFrame saved to: {output_csv_path}")


# In[18]:


csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)


# # Checking null values and dropping if necessary
# 

# In[19]:


total_records = df.shape[0]
print("Total Number of Records:", total_records)

null_values = df.isnull().sum()

# Display the null values in each column
print("Null Values in Each Column:", null_values)


# In[20]:


df_cleaned = df.dropna()
df_cleaned.shape


# In[21]:


df_cleaned.head()


# # Changing the datetime format

# In[23]:


df_cleaned['publishedAt'] = pd.to_datetime(df['publishedAt'], format='%Y-%m-%dT%H:%M:%SZ')

# Create a new column with year, month, and day
df_cleaned['publishedAt'] = df_cleaned['publishedAt'].dt.strftime('%Y-%m-%d')

df_cleaned.head()


# In[40]:


df_cleaned['trending_date'] = pd.to_datetime(df['trending_date'], format='%Y-%m-%dT%H:%M:%SZ')

# Create a new column with year, month, and day
df_cleaned['trending_date'] = df_cleaned['trending_date'].dt.strftime('%Y-%m-%d')

df_cleaned.head()


# # Remove duplicates

# In[35]:


# Check for non-unique values in the specified column
non_unique_rows = df_cleaned.duplicated()
# Display rows that are duplicates
print("Duplicate rows:")
print(df_cleaned[non_unique_rows])

# Display the count of duplicate rows
print("\nNumber of duplicate rows:", non_unique_rows.sum())


# In[34]:


df_cleaned = df_cleaned.drop_duplicates()


# In[36]:


output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'
df_cleaned.to_csv(output_csv_path, index=False)


# In[38]:


print(df_cleaned.dtypes)


# In[42]:


df_cleaned.head()


# In[44]:


csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Convert the 'comment_count' column to numeric, replacing errors with NaN
df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

# Fill NaN values with a default value (e.g., 0)
df[column_name] = df[column_name].fillna(0).astype(int)

# Display the first few rows of the DataFrame with corrected values
print("DataFrame with corrected 'comment_count' column:")
print(df.head())

# Display the data types of each column
print("\nData Types of Each Column:")
print(df.dtypes)


# In[46]:


output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'
df_cleaned.to_csv(output_csv_path, index=False)


# In[48]:


# Create a dictionary mapping region codes to latitude and longitude
region_coordinates = {
    'IN': {'lat': 20.5937, 'long': 78.9629},  # India
    'US': {'lat': 37.7749, 'long': -122.4194},  # United States
    'GB': {'lat': 51.5099, 'long': -0.1180},  # United Kingdom
    'CA': {'lat': 45.4215, 'long': -75.6993}  # Canada
}

# Add 'lat_geo' and 'long_geo' columns based on the region codes
df['lat_geo'] = df['Region'].map(lambda x: region_coordinates.get(x, {}).get('lat'))
df['long_geo'] = df['Region'].map(lambda x: region_coordinates.get(x, {}).get('long'))

# Display the first few rows of the DataFrame with the new columns
print("DataFrame with new 'lat_geo' and 'long_geo' columns:")
print(df.head())


# In[52]:


output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned(1).csv'
df.to_csv(output_csv_path, index=False)


# In[51]:


df.shape


# # Removing extra \ causing errors.

# In[64]:


csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)


# In[68]:


import pandas as pd

# Assuming 'df' is your DataFrame and 'your_column_name' is the name of the column you want to check
filtered_df = df[df['tags'].str.endswith('\\')]


# In[72]:


print(df)


# In[67]:


df['tags'] = df['tags'].str.rstrip('\\')


# In[76]:


output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'
df.to_csv(output_csv_path, index=False)


# # Creating category dataset

# In[1]:


import json

# Let's assume you have JSON data for each region in separate files
# Load JSON data for each region
with open('C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_category_id.json', 'r') as file:
    us_categories = json.load(file)

print (us_categories)
# ... Do the same for GB and CA

# Combine the JSON data
# combined_categories = in_categories + us_categories # + GB and CA

# Now `combined_categories` is a list of dictionaries with all categories across all regions


# In[2]:


import json

# Let's assume you have JSON data for each region in separate files
# Load JSON data for each region
with open('C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_category_id.json', 'r') as file:
    IN_categories = json.load(file)

print (IN_categories)


# # Creating a dataset of coordinates of the entire perimeter of the country. 

# In[4]:


import json

# Assuming 'gadm41_IND_0.json' is the path to your JSON file
file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_IND_0.json'

# Open the JSON file and load its content into a variable
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Now 'data' contains the JSON data as a Python dictionary or list
print(data)


# # Converting coordinates from json to csv.

# In[ ]:


import json
import csv

def flatten_coordinates(geometry):
    """
    Flattens the coordinates from the geometry object into a list of [longitude, latitude] pairs.
    Handles both Polygon and MultiPolygon geometries.
    """
    coordinates = []
    if geometry['type'] == 'Polygon':
        for polygon in geometry['coordinates']:
            for coord in polygon:
                coordinates.append(coord)
    elif geometry['type'] == 'MultiPolygon':
        for multipolygon in geometry['coordinates']:
            for polygon in multipolygon:
                for coord in polygon:
                    coordinates.append(coord)
    return coordinates

def extract_coordinates(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract flattened coordinates for each feature
    flattened_coordinates = []
    for feature in data['features']:
        geometry = feature['geometry']
        flattened_coords = flatten_coordinates(geometry)
        flattened_coordinates.extend(flattened_coords)

    return flattened_coordinates

def save_to_csv(coordinates, csv_file_path):
    # Prepare the CSV file for all coordinates
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coord in coordinates:
            # Assuming the coordinates are in [longitude, latitude] format
            writer.writerow({'latitude': coord[1], 'longitude': coord[0]})

if __name__ == "__main__":
    json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_IN_0.json'  # Update this to your GeoJSON file path
    csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_IN_0.csv'  # Define your output CSV file path
    coordinates = extract_coordinates(json_file_path)
    save_to_csv(coordinates, csv_file_path)
    print(f"Coordinates have been extracted and saved to {csv_file_path}.")


# In[ ]:


import json
import csv

def flatten_coordinates(geometry):
    """
    Flattens the coordinates from the geometry object into a list of [longitude, latitude] pairs.
    Handles both Polygon and MultiPolygon geometries.
    """
    coordinates = []
    if geometry['type'] == 'Polygon':
        for polygon in geometry['coordinates']:
            for coord in polygon:
                coordinates.append(coord)
    elif geometry['type'] == 'MultiPolygon':
        for multipolygon in geometry['coordinates']:
            for polygon in multipolygon:
                for coord in polygon:
                    coordinates.append(coord)
    return coordinates

def extract_coordinates(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract flattened coordinates for each feature
    flattened_coordinates = []
    for feature in data['features']:
        geometry = feature['geometry']
        flattened_coords = flatten_coordinates(geometry)
        flattened_coordinates.extend(flattened_coords)

    return flattened_coordinates

def save_to_csv(coordinates, csv_file_path):
    # Prepare the CSV file for all coordinates
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coord in coordinates:
            # Assuming the coordinates are in [longitude, latitude] format
            writer.writerow({'latitude': coord[1], 'longitude': coord[0]})

if __name__ == "__main__":
    json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_GB_0.json'  # Update this to your GeoJSON file path
    csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_GB_0.csv'  # Define your output CSV file path
    coordinates = extract_coordinates(json_file_path)
    save_to_csv(coordinates, csv_file_path)
    print(f"Coordinates have been extracted and saved to {csv_file_path}.")


# In[ ]:


import json
import csv

def flatten_coordinates(geometry):
    """
    Flattens the coordinates from the geometry object into a list of [longitude, latitude] pairs.
    Handles both Polygon and MultiPolygon geometries.
    """
    coordinates = []
    if geometry['type'] == 'Polygon':
        for polygon in geometry['coordinates']:
            for coord in polygon:
                coordinates.append(coord)
    elif geometry['type'] == 'MultiPolygon':
        for multipolygon in geometry['coordinates']:
            for polygon in multipolygon:
                for coord in polygon:
                    coordinates.append(coord)
    return coordinates

def extract_coordinates(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract flattened coordinates for each feature
    flattened_coordinates = []
    for feature in data['features']:
        geometry = feature['geometry']
        flattened_coords = flatten_coordinates(geometry)
        flattened_coordinates.extend(flattened_coords)

    return flattened_coordinates

def save_to_csv(coordinates, csv_file_path):
    # Prepare the CSV file for all coordinates
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coord in coordinates:
            # Assuming the coordinates are in [longitude, latitude] format
            writer.writerow({'latitude': coord[1], 'longitude': coord[0]})

if __name__ == "__main__":
    json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_US_0.json'  # Update this to your GeoJSON file path
    csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_US_0.csv'  # Define your output CSV file path
    coordinates = extract_coordinates(json_file_path)
    save_to_csv(coordinates, csv_file_path)
    print(f"Coordinates have been extracted and saved to {csv_file_path}.")


# In[4]:


import json
import csv

def flatten_coordinates(geometry):
    """
    Flattens the coordinates from the geometry object into a list of [longitude, latitude] pairs.
    Handles both Polygon and MultiPolygon geometries.
    """
    coordinates = []
    if geometry['type'] == 'Polygon':
        for polygon in geometry['coordinates']:
            for coord in polygon:
                coordinates.append(coord)
    elif geometry['type'] == 'MultiPolygon':
        for multipolygon in geometry['coordinates']:
            for polygon in multipolygon:
                for coord in polygon:
                    coordinates.append(coord)
    return coordinates

def extract_coordinates(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract flattened coordinates for each feature
    flattened_coordinates = []
    for feature in data['features']:
        geometry = feature['geometry']
        flattened_coords = flatten_coordinates(geometry)
        flattened_coordinates.extend(flattened_coords)

    return flattened_coordinates

def save_to_csv(coordinates, csv_file_path):
    # Prepare the CSV file for all coordinates
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coord in coordinates:
            # Assuming the coordinates are in [longitude, latitude] format
            writer.writerow({'latitude': coord[1], 'longitude': coord[0]})

if __name__ == "__main__":
    json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_CAN_0.json'  # Update this to your GeoJSON file path
    csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_CAN_0.csv'  # Define your output CSV file path
    coordinates = extract_coordinates(json_file_path)
    save_to_csv(coordinates, csv_file_path)
    print(f"Coordinates have been extracted and saved to {csv_file_path}.")


# # Adding region column to every csv file to maintain data consistency.

# In[ ]:


import pandas as pd

# Load the CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_IN_0.csv'  # Adjust the path to your specific CSV file
df = pd.read_csv(csv_file_path)

# Add a new column 'region' with the value 'IN' for all records
df['region'] = 'IN'

# Save the updated DataFrame back to CSV
updated_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_IN_0.csv'  # Define your output CSV file path
df.to_csv(updated_csv_file_path, index=False)

print(f"Updated CSV saved to {updated_csv_file_path}.")


# In[ ]:


import pandas as pd

# Load the CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_GBR_0.csv'  # Adjust the path to your specific CSV file
df = pd.read_csv(csv_file_path)

# Add a new column 'region' with the value 'IN' for all records
df['region'] = 'GB'

# Save the updated DataFrame back to CSV
updated_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_GBR_0.csv'  # Define your output CSV file path
df.to_csv(updated_csv_file_path, index=False)

print(f"Updated CSV saved to {updated_csv_file_path}.")


# In[ ]:


import pandas as pd

# Load the CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_US_0.csv'  # Adjust the path to your specific CSV file
df = pd.read_csv(csv_file_path)

# Add a new column 'region' with the value 'IN' for all records
df['region'] = 'US'

# Save the updated DataFrame back to CSV
updated_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_US_0.csv'  # Define your output CSV file path
df.to_csv(updated_csv_file_path, index=False)

print(f"Updated CSV saved to {updated_csv_file_path}.")


# In[10]:


import pandas as pd

# Load the CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\gadm41_CAN_0.csv'  # Adjust the path to your specific CSV file
df = pd.read_csv(csv_file_path)

# Add a new column 'region' with the value 'IN' for all records
df['region'] = 'CAN'

# Save the updated DataFrame back to CSV
updated_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_CAN_0.csv'  # Define your output CSV file path
df.to_csv(updated_csv_file_path, index=False)

print(f"Updated CSV saved to {updated_csv_file_path}.")


# # Merging all csv files to create one dataset. 

# In[12]:


import pandas as pd

# Replace these file paths with the paths to your CSV files
file_paths = [
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_IND_0.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_GBR_0.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_USA_0.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\updated_gadm41_CAN_0.csv'
]

# Read each CSV file into a separate DataFrame
dfs = [pd.read_csv(file) for file in file_paths]

# Concatenate the DataFrames along the rows (axis=0)
merged_df = pd.concat(dfs, ignore_index=True)

# Display the first few rows of the merged DataFrame
print("Merged DataFrame:")
print(merged_df.head())

# Save the merged DataFrame to a new CSV file
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_region_coordinates.csv'
merged_df.to_csv(output_csv_path, index=False)

# Display the path of the saved file
print(f"\nMerged DataFrame saved to: {output_csv_path}")


# # Adding region_fk to the youtube_trending_data dataset.

# In[14]:


import pandas as pd
import numpy as np

# Load the CSV file
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned.csv'  # Update this path to your CSV file location
df = pd.read_csv(csv_file_path)

# Define the ranges for region_fk values based on the region
ranges = {
    'IN': (1, 38935),
    'GB': (38936, 51809),
    'US': (51810, 245946),
    'CA': (245947, 659536),
}

# Function to generate a region_fk value based on the region
def assign_region_fk(region):
    start, end = ranges[region]
    return np.random.randint(start, end + 1)

# Apply the function to each row in the DataFrame to create the new 'region_fk' column
df['region_fk'] = df['Region'].apply(assign_region_fk)

# Save the updated DataFrame back to CSV
updated_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned_withfk.csv'  # Define your output CSV file path
df.to_csv(updated_csv_file_path, index=False)

print(f"CSV file updated and saved to {updated_csv_file_path}.")
df.head()


# # Converting category json to csv.

# In[ ]:


import json
import pandas as pd

# Load the JSON file
json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_category_id.json'

# Read the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract ID values and their corresponding titles
# Assuming the JSON structure includes a list of categories, each with an "id" and a "snippet" that contains the "title"
id_title_pairs = [(category['id'], category['snippet']['title']) for category in data['items']]

# Convert to DataFrame
df = pd.DataFrame(id_title_pairs, columns=['id', 'title'])

# Save to CSV
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_category_id.csv'
df.to_csv(csv_file_path, index=False)

print(f"ID values and their corresponding titles have been saved to {csv_file_path}.")


# In[ ]:


import json
import pandas as pd

# Load the JSON file
json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GBR_category_id.json'

# Read the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract ID values and their corresponding titles
# Assuming the JSON structure includes a list of categories, each with an "id" and a "snippet" that contains the "title"
id_title_pairs = [(category['id'], category['snippet']['title']) for category in data['items']]

# Convert to DataFrame
df = pd.DataFrame(id_title_pairs, columns=['id', 'title'])

# Save to CSV
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GBR_category_id.csv'
df.to_csv(csv_file_path, index=False)

print(f"ID values and their corresponding titles have been saved to {csv_file_path}.")


# In[ ]:


import json
import pandas as pd

# Load the JSON file
json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_category_id.json'

# Read the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract ID values and their corresponding titles
# Assuming the JSON structure includes a list of categories, each with an "id" and a "snippet" that contains the "title"
id_title_pairs = [(category['id'], category['snippet']['title']) for category in data['items']]

# Convert to DataFrame
df = pd.DataFrame(id_title_pairs, columns=['id', 'title'])

# Save to CSV
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_category_id.csv'
df.to_csv(csv_file_path, index=False)

print(f"ID values and their corresponding titles have been saved to {csv_file_path}.")


# In[18]:


import json
import pandas as pd

# Load the JSON file
json_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_category_id.json'

# Read the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract ID values and their corresponding titles
# Assuming the JSON structure includes a list of categories, each with an "id" and a "snippet" that contains the "title"
id_title_pairs = [(category['id'], category['snippet']['title']) for category in data['items']]

# Convert to DataFrame
df = pd.DataFrame(id_title_pairs, columns=['id', 'title'])

# Save to CSV
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_category_id.csv'
df.to_csv(csv_file_path, index=False)

print(f"ID values and their corresponding titles have been saved to {csv_file_path}.")


# # Merging csv files.

# In[19]:


import pandas as pd

# Replace these file paths with the paths to your CSV files
file_paths = [
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\IN_category_id.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\GB_category_id.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\US_category_id.csv',
    'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\CA_category_id.csv'
]

# Read each CSV file into a separate DataFrame
dfs = [pd.read_csv(file) for file in file_paths]

# Concatenate the DataFrames along the rows (axis=0)
merged_df = pd.concat(dfs, ignore_index=True)

# Display the first few rows of the merged DataFrame
print("Merged DataFrame:")
print(merged_df.head())

# Save the merged DataFrame to a new CSV file
output_csv_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_category.csv'
merged_df.to_csv(output_csv_path, index=False)

# Display the path of the saved file
print(f"\nMerged DataFrame saved to: {output_csv_path}")


# # Searching duplicate records and dropping them.

# In[ ]:


# csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_category.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)
# Check for non-unique values in the specified column
non_unique_rows = df.duplicated()
# Display rows that are duplicates
print("Duplicate rows:")
print(df[non_unique_rows])

# Display the count of duplicate rows
print("\nNumber of duplicate rows:", non_unique_rows.sum())


# In[21]:


df = df.drop_duplicates()
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_category_cleaned.csv'
df.to_csv(csv_file_path, index=False)


# # Adding id to region_coordinates to help merge csv.

# In[31]:


csv_file_path = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_region_coordinates.csv'

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Add an 'id' column starting from 1 to n for every record
df.insert(0, 'id', range(1, 1 + len(df)))

# Save the modified DataFrame back to CSV
# Replace with the actual path where you want to save the modified CSV file
output_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\region-coordinates.csv'
df.to_csv(output_csv_file_path, index=False)


# In[32]:


df.head()


# # Creating mongodb document type dataset by embedding region coordinates and category dataset into youtube_trending data dataset.

# In[10]:


import pandas as pd

# Replace these file paths with the actual paths of your CSV files.
youtube_trending_data_csv = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_data_cleaned_withfk.csv'
category_csv = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\merged_category_cleaned.csv'
region_csv = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\region-coordinates.csv'
# Load the data into pandas DataFrames
youtube_trending_data_df = pd.read_csv(youtube_trending_data_csv)
category_df = pd.read_csv(category_csv)
region_df = pd.read_csv(region_csv)
# Merge the DataFrames on the 'category_id' column
# This assumes that 'category_id' is the column name in both DataFrames that you want to join on.
merged_df = youtube_trending_data_df.merge(category_df, left_on='categoryId', right_on='id', how='left')
merged_df['categoryId'] = merged_df.apply(lambda row: {'id': row['categoryId'], 'title': row['title_y']}, axis=1)

merged_df = merged_df.merge(region_df, left_on='region_fk', right_on='id', how='left')
merged_df['region_fk'] = merged_df.apply(lambda row: {'geo_lat': row['latitude'], 'geo_long': row['longitude']}, axis=1)

merged_df.head()


# # Dropping duplicate columns.

# In[11]:


merged_df.drop(columns=['id_x', 'title_y', 'id_y', 'latitude', 'longitude', 'region'], inplace=True)

merged_df.head()


# # Renaming columns according to mongodb dataset.

# In[12]:


# Rename the merged_df columns to match the MongoDB document field names
merged_df.rename(columns={'categoryId': 'category', 'region_fk': 'country_coordinates', 'Region': 'region'}, inplace=True)

merged_df.head()


# In[13]:


output_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data.csv'
merged_df.to_csv(output_csv_file_path, index=False)


# # Converting string value columns to json string.

# In[ ]:


# Define a function to safely convert a string representation of a dictionary into a JSON object
def convert_to_json(value):
    try:
        # First, we use ast.literal_eval to safely evaluate the string
        # into a Python dictionary since the input is not in JSON format
        dict_value = ast.literal_eval(value)
        # Then, we convert the dictionary into a JSON object
        return json.dumps(dict_value)
    except ValueError as e:
        # Return the original string if there's an error
        print(f"Error converting to JSON: {e}")
        return value

for index, row in df.iterrows():
    # Convert 'category' and 'country_coordinates' to JSON objects
    df.at[index, 'category'] = convert_to_json(row['category'])
    df.at[index, 'country_coordinates'] = convert_to_json(row['country_coordinates'])

df.head()


# In[15]:


output_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data_dn.csv'
df.to_csv(output_csv_file_path, index=False)


# # Converting tags column into a dict.

# In[18]:


import pandas as pd
import json

# Replace 'path_to_your_csv_file.csv' with the actual path to your CSV file.
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data_dn.csv'

# Load the CSV data into a pandas DataFrame.
df = pd.read_csv(csv_file_path)

# Define functions to safely convert strings to JSON objects.
def convert_category_string_to_json(category_string):
    try:
        return json.loads(category_string.replace("'", '"'))
    except json.JSONDecodeError:
        return None

# Convert the 'category' and 'country_coordinates' columns.
df['tags'] = df['tags'].apply(convert_category_string_to_json)

# Replace 'path_to_your_output_csv_file.csv' with the actual path where you want to save the modified CSV file.
output_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data_dn.csv'
df.to_csv(output_csv_file_path, index=False)

print(f"Updated CSV with JSON objects has been saved to {output_csv_file_path}")

df.head()


# In[19]:


import pandas as pd
import json

# Placeholder paths for your CSV input and output files
csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data_dn.csv'
output_csv_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\mongo dataset\\yt_trending_data_cleaned.csv'

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Define a function to convert the pipe-separated tags string to a JSON object (Python dictionary)
def tags_to_json(tags_str):
    # Split the string by '|' to get a list of tags
    tags_list = tags_str.split('|') if pd.notnull(tags_str) else []
    # Return a JSON string representation of the list
    return json.dumps(tags_list)

# Apply the conversion function to the 'tags' column
df['tags'] = df['tags'].apply(tags_to_json)

# Save the modified DataFrame back to CSV, which now contains the tags as JSON objects
df.to_csv(output_csv_file_path, index=False)


# In[ ]:




