import json
import re
import os

# Define file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, 'grouped_pois_detail.json')
log_file_path = os.path.join(current_dir, 'name_change_log.txt')

def clean_poi_names():
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"File not found: {json_file_path}")
        return

    print(f"Reading from {json_file_path}...")
    
    # Read JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    changed_count = 0
    
    # Regex to match suffix in parentheses (English and Chinese) at the end of the string
    # \s* matches optional leading whitespace
    # [\(\（] matches opening parenthesis
    # [^\)\）]* matches content that is NOT a closing parenthesis
    # [\)\）] matches closing parenthesis
    # $ matches end of string
    pattern = re.compile(r'\s*[\(\（][^\)\）]*[\)\）]$')

    try:
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            log_file.write("Modification Log\n")
            log_file.write("================\n")
            
            # Iterate through districts
            for district in data:
                if 'pois' in district and isinstance(district['pois'], list):
                    for poi in district['pois']:
                        if 'name' in poi:
                            original_name = poi['name']
                            
                            # Apply regex to remove suffix
                            new_name = pattern.sub('', original_name)
                            
                            # Check if changed
                            if new_name != original_name:
                                # Update the POI
                                poi['name'] = new_name
                                
                                # Log change
                                log_file.write(f"'{original_name}' -> '{new_name}'\n")
                                changed_count += 1
        
        # Save modified data back
        print(f"Writing updated data to {json_file_path}...")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Processing complete. {changed_count} names modified.")
        print(f"Log saved to {log_file_path}")
        
    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    clean_poi_names()
