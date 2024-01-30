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


# In[55]:


# Remove '\n' from all columns in the DataFrame
df = df.replace('\n', '', regex=True)

# Add a new line at the end of every record in the CSV file
output_file_path = 'C:\\Users\\rauna\\Downloads\\IS Dataset raw\\merged_data_cleaned(2).csv'
df.to_csv(output_file_path, index=False, line_terminator='\n')

# Display the first few rows of the cleaned DataFrame
print("DataFrame with removed '\\n' and added new line at the end:")
print(df.head())


# In[ ]:




