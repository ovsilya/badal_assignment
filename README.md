<h1>Problem Statement</h1>

We want to create a POC to accelerate the house purchasing process using GCP native ML services. A sample deed of trust document can be found here deed-of-trust_template.pdf. The objective of the task is to extract useful customer information such as lender name, lender address, trusty, etc.

**What we except**

A working solution for an end to end machine learning pipeline to extract lender information from the provided document. We do not expect a perfect solution, just want to see how you approach the problem and test basic coding skills.

**Technologies**

You are free to use any tools of your choosing, but we recommend the following:
- DocAI
- VertexAI
- Cohere.ai
- Any python machine learning library if you are new to GCP, or find need to get around a limitation in one of the GCP services

**Deliverables**

- High level architecture and approach explanation
- Code of notebooks used and any extra configurations that need to be provided if using APIs manually
- Any challenges or issues encountered during the process + recommendations for improvements in a production environment.

<h1>Solution</h1>

<h3>Tool selection</h3>

- VM instance has been created in GCP with the access through the SSH connection
- Document AI by Google Cloud is being used here as a tool for processing unstructured data to analyze and extract entities
- General form processor is used to extract form elements (this processor has public access)


Below are the steps to be executed before running the analysis task on the processor.


<h2>1. Enable the Cloud Document AI API</h2>

- In Google Cloud Console, on the Navigation menu (Navigation menu), click APIs & services > Library.
- Search for Cloud Document AI API, then click the Enable button to use the API in your Google Cloud project.

<h2>2. Create a general form processor</h2>

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

<h2>3. Authenticate API requests</h2>
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

<h2>4. Make a synchronous call to the Document AI API using the Python Document AI client libraries.</h2>

4.1 Configure VM Instance to use the Document AI Python client

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

<h2>5. Running the parser</h2>

```
python3 parsing_document.py \
--project_id=$PROJECT_ID \
--processor_id=$PROCESSOR_ID \
--location=us \
--file_name=deed-of-trust_template_3pages.pdf | tee badal_docAI.txt
```

<h2>Handling the processing response</h2>

The response to a processing request contains a document object that holds everything known about the processed document, including all of the structured information that Document AI was able to extract.

This page explains the layout of document object by providing sample documents and then mapping them to fields in the document object. It also provides Client Library code samples.

https://cloud.google.com/document-ai/docs/handle-response#python_2


<h2>Future inmprovements</h2>

_Specialized Processors - Dedicated models for the world's most common document types._

Specialized processros could be used to increase the accuracy. For example, 1003 Parser extracts over 50 fields from Fannie Mae Form 1003 (URLA). The 1003 Form is Fannie Mae's form number for the Uniform Residential Loan Application (URLA), a borrower’s application for a mortgage. Freddie Mac's form number is Form 65; both refer to the same form. 

(!) To use specialized Processors, GCP users shoud request private access

Demo tests have shown better accuracy for the same .pdf document. 
https://cloud.google.com/solutions/lending-doc-ai
