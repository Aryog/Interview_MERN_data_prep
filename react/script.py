import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
url = "https://flexiple.com/react/interview-questions"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all question elements
questions = soup.find_all('details')

# List to store all question-answer pairs
qa_list = []

# Iterate through each question
for question in questions:
    # Extract the question text
    question_text = question.find('summary').text.strip()
    
    # Check if the details tag has the 'open' attribute
    is_open = 'open' in question.attrs
    
    # Extract the answer text (if available)
    answer = question.find('div', class_='answer')
    answer_text = answer.text.strip() if answer else "Answer not available"
    
    # Create a dictionary for this Q&A pair
    qa_pair = {
        "question": question_text,
        "answer": answer_text
    }
    
    # Add the Q&A pair to the list
    qa_list.append(qa_pair)

# Convert the list to JSON
json_output = json.dumps(qa_list, indent=2)

# Print the JSON output
print(json_output)

# Optionally, save the JSON to a file
with open('react_questions.json', 'w') as f:
    json.dump(qa_list, f, indent=2)
