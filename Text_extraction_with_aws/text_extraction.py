import boto3
from botocore.exceptions import ClientError
import openpyxl


# Configure AWS credentials and region
aws_access_key = ''
aws_secret_key = ''
aws_region = ''
bucket_name = 'testingnimbleocr'#created by manoj contains pdf files of 100 
#pdf file key is the name of the pdf file
pdf_file_keys = [str(i) for i in range(1, 3)]  # since i stored all the pdf names as 1,2,3,4,5.pdf like this format

textract_client = boto3.client('textract', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Start Textract job for each PDF file
for pdf_file_key in pdf_file_keys:
    try:
        response = textract_client.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': f'{pdf_file_key}.pdf'}}
        )
        job_id = response['JobId']

        while True:
            response = textract_client.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            if status in ['SUCCEEDED', 'FAILED']:
                break

        if status == 'SUCCEEDED':
            detected_text = []
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    detected_text.append(item['Text'])

            # Process or print the extracted text for each file
            # print(f"Text extracted from {pdf_file_key}.pdf: {detected_text}")

            # Store the detected text in the Excel sheet
            sheet.append([f"{pdf_file_key}.pdf", ", ".join(detected_text)])

        else:
            print(f"Textract job for {pdf_file_key}.pdf failed with status: {status}")

    except ClientError as e:
        print(f"Error starting Textract job for {pdf_file_key}.pdf: {e}")

workbook.save('detected_text.xlsx')
