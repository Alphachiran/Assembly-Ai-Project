import json

# Function to format long text with line breaks
def format_text(text, max_length=80):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            lines.append(" ".join(current_line))
            current_line = []
            current_length = 0
        current_line.append(word)
        current_length += len(word) + 1

    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)

# Function to process and save JSON data
def process_and_save_json(file1_name, file2_name,filenamejson):
    # Load the first JSON file (structured as a list of dictionaries)
    with open(file1_name, 'r') as file1:
        data1 = json.load(file1)  # Load first JSON file

    # Load the second JSON file (structured as a single string)
    with open(file2_name, 'r') as file2:
        data2 = file2.read().strip()  # Load second JSON file as a raw string

    # Merge data into the result list
    result = []

    # Process the first JSON file (data1)
    for item in data1:
        result.append({
            "gist": item.get("gist", ""),
            "summary": item.get("summary", "")
        })

    # Process the second JSON file (data2)
    result.append({
        "summary": data2
    })

    # Save the result as a JSON file
    filename = "merge" + filenamejson + ".json"
    with open(filename, 'w') as output_file:
        json.dump(result, output_file, indent=4)

    print("Completed......")

