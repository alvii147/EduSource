import os, io
from google.cloud import vision
from google.cloud.vision_v1.types.image_annotator import Image
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"MyFirstProject-da5d6b04be74.json"

def getString():
    client = vision.ImageAnnotatorClient()

    image_path = 'static/img.jpg'

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = Image(content=content)
    response = client.text_detection(image=image)
    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    return df['description'][0].split("\n")[0].replace(" ", "")