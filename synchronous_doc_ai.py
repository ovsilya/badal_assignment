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

document=process_document(args.project_id,args.location,args.processor_id,args.file_name  )

print("Document processing complete.")
# print the raw text
print("Text: \n{}\n".format(document.text))

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

# Grab each key/value pair and their corresponding confidence scores.
document_pages = document.pages

print("Form data detected:\n")
# For each page fetch each form field and display fieldname, value and confidence scores
for page in document_pages:
    print("Page Number:{}".format(page.page_number))
    for form_field in page.form_fields:
        fieldName=get_text(form_field.field_name,document)
        nameConfidence = round(form_field.field_name.confidence,4)
        fieldValue = get_text(form_field.field_value,document)
        valueConfidence = round(form_field.field_value.confidence,4)
        print(fieldName+fieldValue +"  (Confidence Scores: (Name) "+str(nameConfidence)+", (Value) "+str(valueConfidence)+")\n")
