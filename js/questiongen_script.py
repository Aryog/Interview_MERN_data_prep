import subprocess
import argparse
import json
import time

def run_llama3(prompt):
    try:
        # Construct the command
        command = f'ollama run llama3 "{prompt}"'
        
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if there was an error
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        
        # Return the output
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_json(file_path):
    with open(file_path, 'r') as file:
        print(file)
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def generate_questions(data):
    for item in data:
        question = item['question']
        contextual_prompt = f"For this question you should generate the follow up question with high relevency. Don't give other than question. Give strictly only follow up question. Technical Interview Question: {question}"
        next_question = run_llama3(contextual_prompt)
        
        if next_question :
            item['followup_question'] = next_question.capitalize()
        else:
            item['followup_question'] = "Unknown"
        
        print(f"Classified question: {question}")
        print(f"Difficulty: {item['followup_question']}")
        print("---")
        
        # Add a delay to avoid overwhelming the LLaMA model
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Classify questions in data.json using LLaMA 3 model")
    parser.add_argument("input_file", nargs='?', default="./classified1_data.json", help="Input JSON file (default: classified1_data)")
    parser.add_argument("output_file", nargs='?', default="./questiongen_data.json", help="Output JSON file (default: questiongen_data.json)")
    
    args = parser.parse_args()

    # Load the JSON data
    data = load_json(args.input_file)

    # Classify the questions
    generate_questions(data)

    # Save the updated data
    save_json(data, args.output_file)
    print(f"Updated data saved to {args.output_file}")

if __name__ == "__main__":
    main()
