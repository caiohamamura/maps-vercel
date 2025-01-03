# Flask hello world
from io import BytesIO
import flask
import os
import rasterio
from rasterio.io import MemoryFile
import requests
from flask_cors import CORS
import re


app = flask.Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})



origins = [
    "https://vercel-opencv.vercel.app/",
    "http://localhost:8080",
]

# Get from environment variable ENVIPIXEL_PLATFORM_KEY
app.secret_key = os.environ.get('ENVIPIXEL_PLATFORM_KEY', 'default_secret_key')


@app.route('/')
def hello_world():
    return 'Hello, World!'


raster_ids = dict(
    cf2019 = 'CF2019.tif',
    cf2020 = 'CF2020.tif',
    cf2021 = 'CF2021.tif',
    tf2019 = 'TF2019.tif',
    tf2020 = 'TF2020.tif',
    tf2021 = 'TF2021.tif',
    sf2019 = 'SF2019.tif',
    sf2020 = 'SF2020.tif',
    sf2021 = 'SF2021.tif',
)

raster_cache = dict()

@app.route('/video')
def video():
    return '<video><source src="https://dd12b372tby3d.cloudfront.net/DTM_viz.mp4" type="video/mp4"></video>'

@app.route('/raster/<string:dataset_id>')
def raster(dataset_id):
    file_url = raster_ids[dataset_id]

    with rasterio.open(file_url) as src:
        # Ignore no data
        data = src.read(1, masked=True)
        min = data.min()
        max = data.max()
        mean = data.mean()
        std = data.std()

        return flask.jsonify({
            'alias': re.sub(r'(\d{4})', r'', dataset_id.lower()),
            'year': int(re.search(r'(\d{4})', dataset_id).group(0)),
            'min': float(min),
            'max': float(max),
            'mean': float(mean),
            'std': float(std)
        })



if __name__ == '__main__':
    app.run()