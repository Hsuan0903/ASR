import json  
  
# Replace 'your_file.json' with the actual JSON file path  
json_file_path = 'real_data_V2/annotations.json'  
  
# Open and read the JSON file line by line  
with open(json_file_path, 'r', encoding='utf-8') as file:  
    for line in file:  
        # Parse the JSON line into a Python dictionary  
        data = json.loads(line.strip())  
          
        # Extract the 'sentence' field which contains the reference text  
        reference_text = data.get('sentence', '').strip()  
          
        # Extract the file name from the 'path' field  
        file_name = data['audio']['path'].split('/')[-1]  
        file_name = file_name[:-4]
        # Print the file name and its corresponding reference text  
        print(f"{file_name}: {reference_text}")  
