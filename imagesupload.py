from pymongo import MongoClient
import gridfs
import os

# MongoDB connection parameters
mongo_uri = 'mongodb://localhost:27017/'
db_name = 'ISmongo'

# Connect to your MongoDB database
client = MongoClient(mongo_uri)
db = client[db_name]

# Initialize GridFS
fs = gridfs.GridFS(db)

# Folder containing your images
#images_folder = '/home/student/Downloads/mongoimages/IN_img'
#images_folder = '/home/student/Downloads/mongoimages/GB_img'
#images_folder = '/home/student/Downloads/mongoimages/US_img'
images_folder = '/home/student/Downloads/mongoimages/CA_img'
# Function to upload a single image
def upload_image(image_path):
    with open(image_path, 'rb') as image_file:
        # The image filename is used as the GridFS filename
        file_name = os.path.basename(image_path)
        # Check if the file already exists to avoid duplicates
        if fs.exists({"filename": file_name}):
            print(f"File {file_name} already exists in GridFS.")
        else:
            # Upload the image to GridFS
            file_id = fs.put(image_file, filename=file_name)
            print(f"Uploaded {file_name} to GridFS with file_id: {file_id}")

# Loop through all images in the folder and upload them
for image_name in os.listdir(images_folder):
    image_path = os.path.join(images_folder, image_name)
    if os.path.isfile(image_path):
        upload_image(image_path)

