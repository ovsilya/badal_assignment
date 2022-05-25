**1. Enable the Cloud Document AI API**

- In Google Cloud Console, on the Navigation menu (Navigation menu), click APIs & services > Library.
- Search for Cloud Document AI API, then click the Enable button to use the API in your Google Cloud project.

**2. Create a general form processor**

Next you will create a Document AI processor using the Document AI Form Parser.
- In the console, on the Navigation menu (Navigation menu), click Document AI > Overview.
- Click Create processor and select Form Parser, which is a type of general processor.
- Specify the processor name as form-parser and select the region US (United States) from the list.
- Click Create to create the general form-parser processor.
```
us parser: 27926b3449bc9ea8
eu parser: ff89fff9a3e82976
```
In the SSH session create an environment variable to contain the Document AI processor ID. 
You must replace the placeholder for [your processor id]:

```
export PROCESSOR_ID=[your processor id]
export PROCESSOR_ID=27926b3449bc9ea8
export PROCESSOR_ID=ff89fff9a3e82976
```

**3. Authenticate API requests **
- Set an environment variable with your Project ID:
```
export PROJECT_ID=$(gcloud config get-value core/project)
```

- Create a new service account to access the Document AI API:
```
export SA_NAME="document-ai-service-account"
gcloud iam service-accounts create $SA_NAME --display-name $SA_NAME
```

- Bind the service account to the Document AI API user role:
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
--member="serviceAccount:$SA_NAME@${PROJECT_ID}.iam.gserviceaccount.com" \
--role="roles/documentai.apiUser"
```

- Create the credentials to log in as a new service account and save them in a JSON file called key.json:
```
gcloud iam service-accounts keys create key.json \
--iam-account  $SA_NAME@${PROJECT_ID}.iam.gserviceaccount.com
```

- Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to the credentials file:
```
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/key.json"
```

**4. Make a synchronous call to the Document AI API using the Python Document AI client libraries.**

4.1 Configure VM Instance to use the Document AI Python client
import the .pdf file into VM Instance
```
gsutil cp gs://cloud-training/gsp924/synchronous_doc_ai.py .
```

- install the Python client libraries required for Document AI and the other libraries
```
python3 -m pip install --upgrade google-cloud-documentai google-cloud-storage prettytable
```

4.2 Run the Document AI Python code
Call the synchronous_doc_ai.py python program with the parameters it requires:

- download the sample form to your working directory
```
gsutil cp gs://transfering_files/deed-of-trust_template_3pages.pdf .
```

**5. Running the parser:**
```
python3 parsing_document.py \
--project_id=$PROJECT_ID \
--processor_id=$PROCESSOR_ID \
--location=us \
--file_name=deed-of-trust_template_3pages.pdf | tee badal_docAI.txt
```


**Handling the processing response**

The response to a processing request contains a document object that holds everything known about the processed document, including all of the structured information that Document AI was able to extract.
This page explains the layout of document object by providing sample documents and then mapping them to fields in the document object. It also provides Client Library code samples. These code samples all use online processing, but the document object parsing works the same for batch processing.

https://cloud.google.com/document-ai/docs/handle-response#python_2
