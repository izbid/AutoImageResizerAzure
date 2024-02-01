import azure.functions as func
import logging
from PIL import Image
import io

app = func.FunctionApp()
#Bindings in declarative code(V2)
@app.blob_trigger(arg_name="myblob", path="image-container/{name}", connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",path="resized-images/{name}",connection="AzureWebJobsStorage")
def ImageProcessor(myblob: func.InputStream, outputblob: func.Out[func.InputStream]) -> None:
    logging.info(f"Python blob trigger function has been triggered by blob"
                 f"Name: {myblob.name} "
                 f"Blob Size: {myblob.length} bytes")
    
    # Open the triggering blob as an image
    image_stream = io.BytesIO(myblob.read())
    image = Image.open(image_stream)

    # Perform an operation on the image, e.g., resize
    processed_image = image.resize((100, 100))

    # Write the processed image to the output blob
    output_stream = io.BytesIO()
    processed_image.save(output_stream,format=image.format)
    output_stream.seek(0)

    # Define the outputblob container
    output_container_name = "resized-images"
    outputblob.set(output_stream.getvalue())
    logging.info(f"Processed image uploaded to {output_container_name}/{myblob.name}")
