from flask import Flask, render_template_string, request, send_file
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId
import io

app = Flask(__name__)

@app.route('/')
def show_titles():
    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ISmongo']
    collection = db['yt_data']

    total_titles = collection.count_documents({})
    documents = collection.find({}, {'title_x': 1}).skip(skip).limit(per_page)
    titles = [(doc.get('title_x', 'No title found'), str(doc['_id']), idx + skip) for idx, doc in enumerate(documents)]

    start_number = skip + 1
    total_pages = (total_titles + per_page - 1) // per_page

    navigation_html = '<div style="padding: 20px;">'
    if page > 1:
        navigation_html += f'<a href="/?page={page - 1}">&laquo; Previous</a>'
    if page < total_pages:
        navigation_html += f'<a href="/?page={page + 1}" style="margin-left: 20px;">Next &raquo;</a>'
    navigation_html += '</div>'
    
    return render_template_string('''
        <html>
            <head>
                <title>Video Titles List</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    li { margin: 5px 0; }
                    a { text-decoration: none; color: blue; }
                    a:hover { text-decoration: underline; }
                    img { width: 100px; }
                </style>
            </head>
            <body>
                <h2>Video Titles from MongoDB</h2>
                <ol start="{{ start_number }}">
                    {% for title, id, idx in titles %}
                        <li><a href="/details/{{ id }}">{{ title }}</a> - {{ idx }}</li>
                    {% endfor %}
                </ol>
                {{ navigation_html|safe }}
            </body>
        </html>
    ''', titles=titles, navigation_html=navigation_html, start_number=start_number)

@app.route('/details/<record_id>')
def show_details(record_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ISmongo']
    collection = db['yt_data']
    fs = gridfs.GridFS(db)

    document = collection.find_one({'_id': ObjectId(record_id)})
    
    # Assuming the record's order number is somehow reflected in or calculable from the document
    # Here, it is assumed to be a direct pass; adjust based on your application's logic
    image_num = document.get('record_number', 1)  # Adjust for the offset
    
    image_filename = f'image_{image_num}.jpg'
    
    # Check if the image exists in GridFS and construct the image URL or use a placeholder
    if fs.exists(filename=image_filename):
        image_url = f"/image/{image_filename}"
    else:
        image_url = "/static/image_not_found.jpg"  # Ensure you have this placeholder image
    
    details_html = '<h2>Record Details</h2><ul>'
    if document:
        for key, value in document.items():
            details_html += f'<li><strong>{key}:</strong> {value}</li>'
        details_html += f'<li><img src="{image_url}" alt="Thumbnail"></li>'
    else:
        details_html = '<p>Record not found.</p>'
    
    return render_template_string('''
        <html>
            <head><title>Record Details</title></head>
            <body>
                {{ details_html|safe }}
                <a href="/">Back to List</a>
            </body>
        </html>
    ''', details_html=details_html)

@app.route('/image/<filename>')
def image(filename):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ISmongo']
    fs = gridfs.GridFS(db)

    try:
        grid_out = fs.get_last_version(filename=filename)
        return send_file(io.BytesIO(grid_out.read()), mimetype='image/jpeg')
    except gridfs.NoFile:
        return send_file('static/image_not_found.jpg', mimetype='image/jpeg')  # Ensure this placeholder

if __name__ == '__main__':
    app.run(debug=True)

