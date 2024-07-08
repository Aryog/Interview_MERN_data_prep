import re
import json

def extract_qa_from_readme(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Pattern to match questions and answers
    pattern = r'(\d+)\.\s+###\s+(.*?)\n(.*?)(?=\n\d+\.\s+###|\Z)'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    qa_list = []
    for match in matches:
        question_number = match[0]
        question = match[1].strip()
        answer = match[2].strip()
        
        qa_list.append({
            "question_number": question_number,
            "question": question,
            "answer": answer
        })
    
    return qa_list

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

# Main execution
input_file = './data_readme.md'
output_file = './data.json'

qa_data = extract_qa_from_readme(input_file)
save_to_json(qa_data, output_file)

print(f"Data has been successfully extracted and saved to {output_file}")
