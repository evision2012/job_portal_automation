import os
import pandas as pd
import PyPDF2
import re
import json

from mylib import city_by_states, is_same

all_cities = [x for val in city_by_states.values() for x in val]
all_cities = [x for x in all_cities if len(x)>3]



# Define stub functions to be implemented later

def clean_text(word):
    if word[0].isalnum() and word[-1].isalnum():
        return word
    elif not word[0].isalnum():
        return clean_text(word[1:])
    elif not word[-1].isalnum():
        return clean_text(word[:-1])
    
    symbols=[',','.','#','/',':','!','%','&','(',')','$','-','+','*']
    for x in symbols:
        if word.endswith(x):
            return word[:-1]
        if word[0]==x:
            return word[1:]


def extract_name(text):
    return "NO_NAME"



def extract_email(text):
    return "NO_EMAIL"



def extract_phone(text):
    return "NO_PHONE"



def extract_city(text):
    return "NO_CITY"



def extract_experience(text):
    return "NO_EXPERIENCE"



def extract_degree(text):
    return "NO_DEGREE"


def load_valid_streams(json_path="Data_Files/stream.json"):
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading valid streams: {e}")
        return []

VALID_STREAMS = load_valid_streams()

def clean_stream(stream, banned):
    print(f" RAW stream input: {repr(stream)}")
    stream = re.sub(r'[\u200b\u200c\u200d\uFEFF]', '', stream)
    stream = re.sub(r"[^a-zA-Z0-9&/,.\-()' ]", '', stream)
    print(f" After regex clean: {stream}")
    stream = re.sub(r'\s{2,}', ' ', stream).strip()
    words = stream.lower().split()
    while words and words[-1] in banned:
        words.pop()
    cleaned = ' '.join(words).title()
    print(f" Final cleaned stream: {cleaned}")
    return cleaned

def extract_stream(text):
    text = text.lower().replace('.', '')
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = text.replace('\n', ' ')
    text = text.replace('’', "'")

    pg_patterns = [
        r"master\s+of\s+\w+.*?",
        r"m\.?tech.*?",
        r"m\.?e.*?",
        r"mba.*?",
        r"pg\s+diploma.*?",
        r"postgraduate.*?",
        r"msc.*?",
    ]
    for pattern in pg_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    patterns = [
        r"\bb\.?\s?tech\b\s*\([^)]*\)\s*in\s+([a-z &]{3,60}?)(?=\s+from\b|\s*\n|,|$)",
        r"\bb\.?\s?tech\s+in\s+([a-zA-Z\s&]{2,60})",
        r"bachelor\s+of\s+(?:engineering|technology|science)\s*(?:\([^)]+\))?\s*in\s+([a-z &]{2,60})",
        r"bachelor(?:'s)?(?:\sdegree)?(?:\s+of\s+(?:engineering|technology|science))?\s+in\s+([a-z &]{2,40})",
        r"bachelor\s+in\s+([a-zA-Z &]{3,60})",
        r"bachelor'?s\s+\w+\s+in\s+([a-zA-Z\s&]{2,60})",
        r"bachelor\s+of\s+\w+\s*\(\s*([a-zA-Z\s&]{2,40})\s*\)",
        r"bachelor\s+of\s+\w+\s+in\s+([a-zA-Z\s&]+)\s+with\s+specialization\s+in\s+[a-zA-Z\s]+",
        r"bachelors?\s+in\s+([a-zA-Z &]{3,60})",
        r"engineer's\s+degree[,:\s]*([a-z &]{3,60})",
        r"engineer'?s\s+degree[:,]?\s*([a-zA-Z &]{3,60})",
        r"\bb\.?\s?e\.?\s*[:\-–]\s*([a-zA-Z &]{3,60})",
        r"bca\s*\(\s*([a-zA-Z\s&]{2,40})\s*\)",
        r"\bb\.?\s?com\s*\(\s*([a-zA-Z\s&]{2,40})\s*\)",
        r"b\.?\s?sc\s*\(?\s*([a-zA-Z\s]{2,}.*?)\s*\)?",
        r"\bb\.?\s?sc\.?\s*(?:in\s+|\()?([a-z &]{3,60}?)(?=\s+and\b|\s+with\b|[,.\n]|$)",
        r"\bb\.?\s?a\.?\s*,\s*([a-zA-Z\s&]{2,40})",
        r"(?:b\.?sc|bsc|b\.?tech|b\.?e|bca|b\.?com|bcom|b\.?a)\s*(?:in\s+|\()\s*([a-z &]{2,60})(?=\s+and\b|\s+with\b|[,.\n]|$)",
        r"bachelor\s+of\s+(?:engineering|technology|science)\s*[-–]\s*[a-z\s.,()]*,\s*([a-z &/,]{3,80})",
        r"(?:b\.?tech|b\.?e|bachelor\s+of\s+(?:technology|engineering))\s*[-–]\s*([a-z &]{2,60})",
        r"(?:specialization|stream|ug|graduation)\s+in\s+([a-z &]{2,40})",
        r"courses\s*[:\-]?\s*([a-z &]{2,40})",
        r"bachelors?\s+of\s+([a-z &]{3,60})",
        r"diploma\s+in\s+([a-z &]{3,60})",
        r"diploma\s*\(?[a-z\s&]{0,20}\)?\s*-\s*([a-z &]{3,60})",
        r"\bdiploma\b\s*\(?([a-z &]{3,60})\)?",
        r"polytechnic\s+diploma\s+in\s+([a-z &]{3,60})",
        r"\btechnical\s+diploma\s+in\s+([a-z &]{3,60})",
    ]

    banned = ['university', 'college', 'institute', 'academy', 'school',
              'kerala', 'india', 'hyderabad', 'tamil nadu', 'from','of']

    possible_streams = []

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            stream = clean_stream(match.group(1), banned)
            print(f"Stream found: {stream}")
            if stream and not any(bad in stream.lower() for bad in banned):
                possible_streams.append(stream)
                
    for stream in possible_streams:
        cleaned = stream.strip().title()
        for valid in VALID_STREAMS:
            if cleaned.lower() == valid.lower():
                print(f"Stream found: {valid}")
                return valid
        parts = re.split(r'\s+and\s+|\s*&\s*', stream)
        for part in parts:
            cleaned_part = part.strip().title()
            for valid in VALID_STREAMS:
                if cleaned_part.lower() == valid.lower():
                    print(f"Stream found: {valid}")
                    return valid

    return ""



def extract_college(text):
    return "NO_COLLEGE"



def extract_graduation_year(text):
    return "NO_YEAR"



def extract_pdf_text(file_path):
    """Extracts and returns all text from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
    return text



def process_resumes(folder_path="Resumes", excel_path="report_students.xlsx"):
    # Ensure resume folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Load existing data or create new DataFrame
    if os.path.exists(excel_path):
        output_df = pd.read_excel(excel_path)
    else:
        columns = [
            "Name", "Email ID", "Phone Number", "Current Location",
            "Total Experience", "Under Graduation degree",
            "UG Specialization", "UG University/institute Name", "UG Graduation year"
        ]
        output_df = pd.DataFrame(columns=columns)

    # Process PDF files one by one
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing: {file_path}")
            text = extract_pdf_text(file_path)

            # Prepare new row from extracted data
            new_row = pd.DataFrame([{
                "Name": extract_name(text),
                "Email ID": extract_email(text),
                "Phone Number": extract_phone(text),
                "Current Location": extract_city(text),
                "Total Experience": extract_experience(text),
                "Under Graduation degree": extract_degree(text),
                "UG Specialization": extract_stream(text),
                "UG University/institute Name": extract_college(text),
                "UG Graduation year": extract_graduation_year(text)
            }])

            # Append new row to the existing DataFrame
            output_df = pd.concat([output_df, new_row], ignore_index=True)

            # Save to Excel immediately
            output_df.to_excel(excel_path, index=False)
            print(f"Data appended for file: {filename}")



# Run the function
if __name__ == "__main__":
    pass
    #process_resumes()




