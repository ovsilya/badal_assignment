# The first two code blocks import the required libraries and parses parameters 
# to initialize variables that identify the Document AI processor and input data.

import argparse
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage
from prettytable import PrettyTable

parser = argparse.ArgumentParser()
parser.add_argument("-P", "--project_id", help="Google Cloud Project ID")
parser.add_argument("-D", "--processor_id", help="Document AI Processor ID")
parser.add_argument("-F", "--file_name", help="Input file name", default="form.pdf")
parser.add_argument("-L", "--location", help="Proocessor Location", default="us")
args = parser.parse_args()

# The process_document function is used to make a synchronous call to a Document AI processor. 
# The function creates a Document AI API client object.
# The processor name required by the API call is created using the 
# project_id,location, and processor_id parameters and the document to be processed is read in and stored in a mime_type structure.

# The processor name and the document are then passed to the Document API client object and 
# a synchronous call to the API is made. If the request is successful the document object that 
# is returned will include properties that contain the data that has been detected by the Document AI processor.

def process_document(project_id, location, processor_id, file_path ):

        # Instantiates a client
        client = documentai.DocumentProcessorServiceClient()

        # The full resource name of the processor, e.g.:
        # projects/project-id/locations/location/processor/processor-id
        # You must create new processors in the Cloud Console first
        name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Create the document object 
        document = {"content": image_content, "mime_type": "application/pdf"}

        # Configure the process request
        request = {"name": name, "document": document}

        # Use the Document AI client synchronous endpoint to process the request
        result = client.process_document(request=request)

        return result.document

# Define a function to retrieve an object dictionary for a named element
def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

# ##############################################################################
# The script then calls the process_document function with the required parameters and saves the response in the document variable.

document=process_document(args.project_id,args.location,args.processor_id,args.file_name)
document_pages = document.pages

# The final block of code prints the .text property that contains all of the text detected in the document:
print("Document processing complete.")
print("Text: \n{}\n".format(document.text))


# ################################
# then displays the form information using the text anchor data for each of the form fields detected by the form parser
# Grab each key/value pair and their corresponding confidence scores

print("Form data detected:\n")

# For each page fetch each form field and display fieldname and value
for page in document_pages:

    print("Page Number:{}".format(page.page_number))

    for form_field in page.form_fields:

        fieldName=get_text(form_field.field_name,document)
        fieldValue = get_text(form_field.field_value,document)

        print("fieldName:", fieldName)
        print("fieldValue:", fieldValue)

        # print(fieldName+fieldValue +"  (Confidence Scores: (Name) "+str(nameConfidence)+", (Value) "+str(valueConfidence)+")\n")



