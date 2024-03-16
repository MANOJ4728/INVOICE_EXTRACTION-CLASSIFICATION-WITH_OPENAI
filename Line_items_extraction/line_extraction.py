import requests
import pandas as pd
import json

excel_file_path = 'E:/textract_codes/detected_text.xlsx'
df = pd.read_excel(excel_file_path)

output_data = []

# Define the format before using it in the prompt
format = [{"description": ""},{"quanity":""},{"unit_price":""},{"total_price":""}]

for index, row in df.iterrows():
    ocr_text = row['ocr_text']

    if not isinstance(ocr_text, list):
        ocr_text = [ocr_text]

    ocr_text_str = "\n".join(ocr_text)

    prompt = f"""Extract the correct invoice line items if they are present in the provided text {ocr_text_str} in the required format {format} and dont include total and sub total related items in invoice line items a line item should contain description and amount consider only those items as line items dont give extra sentence or words other than the format that i have asked for if values for keys provided in format{format} are not preseent give NA as value"""

    key =""

    result = requests.post(url='https://api.openai.com/v1/chat/completions',
                        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {key}'},
                        json={
                            "model": "text-davinci-003",
                            "messages": [
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.2  # changed now to get same result every time for response
                        }
                    )

    try:
        result_json = json.loads(result.text)
        extracted_info = result_json['choices'][0]['message']['content']
        output_data.append(extracted_info)
    except KeyError as e:
        print(f"KeyError: {e}. Could not find the expected structure in the API response.")
    except json.JSONDecodeError as json_error:
        print(f"JSONDecodeError: {json_error}. Could not decode the JSON response.")

output_df = pd.DataFrame(output_data)
output_excel_file_path = 'E:/textract_codes/correct_descriptions.xlsx'
output_df.to_excel(output_excel_file_path, index=False)
print(f"Output saved to: {output_excel_file_path}")
