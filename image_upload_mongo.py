import os
import mysql.connector
from mysql.connector import Error

# Database connection parameters
host = 'localhost'
database = 'IndStd'
user = 'root'
password = 'password'

def connect_to_database():
    """Connect to the MySQL database and return the connection."""
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if connection.is_connected():
            #print('Connected to MySQL database')
            return connection
    except Error as e:
        print(e)

def upload_image(image_path, image_id):
    """Upload an image to the MySQL database."""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            with open(image_path, 'rb') as file:
                binary_data = file.read()
            query = "INSERT INTO images (image_id, image) VALUES (%s, %s)"
            cursor.execute(query, (image_id, binary_data))
            connection.commit()
            print(f"Image {image_path} uploaded successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    images_folder = '/home/student/Downloads/images dataset/images dataset/CA_img' # Change images directory accordingly.
    total_images = 0
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        if os.path.isfile(image_path):
            # Extract the index from the filename (assuming format 'image_{index}.jpg')
            # and increment by 1 to start IDs from 1
            image_id = int(image_name.split('_')[1].split('.')[0]) + 1
            upload_image(image_path, image_id)
            total_images +=1

    print(f"Finished uploading {total_images} images.")
if __name__ == "__main__":
    main()





