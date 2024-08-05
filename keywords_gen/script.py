import subprocess
import argparse
import json
import time

def run_ollama(prompt):
    try:
        command = f'ollama run llama3 "{prompt}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def generate_keywords(data):
    for item in data:
        question = item['question']
        answer = item['answer']
        contextual_prompt = f"Generate 3-5 relevant keywords for this technical interview question and answer. Provide only the keywords, separated by commas. Question: {question} Answer: {answer}"
        
        keywords_response = run_ollama(contextual_prompt)
        
        if keywords_response:
            keywords = [kw.strip() for kw in keywords_response.split(',')]
            item['keywords'] = keywords
        else:
            item['keywords'] = []
        
        print(f"Processed question: {question}")
        print(f"Generated keywords: {', '.join(item['keywords'])}")
        print("---")
        
        # Add a delay to avoid overwhelming the Ollama model
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Generate keywords for questions in JSON data using Ollama")
    parser.add_argument("input_file", nargs='?', default="./100_days_learning_data.json", help="Input JSON file (default: ./100_days_learning_data.json)")
    parser.add_argument("output_file", nargs='?', default="./100_days_final_data.json", help="Output JSON file (default: ./100_days_final_data.json)")
    
    args = parser.parse_args()
    
    # Load the JSON data
    data = load_json(args.input_file)
    
    # Generate keywords for the questions
    generate_keywords(data)
    
    # Save the updated data
    save_json(data, args.output_file)
    print(f"Updated data with keywords saved to {args.output_file}")

if __name__ == "__main__":
    main()
