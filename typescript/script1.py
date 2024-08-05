from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def scrape_typescript_questions():
    url = "https://www.turing.com/interview-questions/typescript"
    
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        
        # Wait for the questions to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "turing-interview-question-item"))
        )
        
        # Give some time for all elements to load
        time.sleep(5)
        
        # Find all question containers
        question_containers = driver.find_elements(By.CLASS_NAME, "turing-interview-question-item")
        
        questions = []
        for container in question_containers:
            try:
                question_elem = container.find_element(By.XPATH, "/html/body/div[2]/div/div/div[6]/section/div/div[2]/div[1]/div[4]/div")
                answer_elem = container.find_element(By.CLASS_NAME, "turing-interview-question-item-answer")
                
                question_text = question_elem.text.strip()
                answer_text = answer_elem.text.strip()
                
                questions.append({
                    "question": question_text,
                    "answer": answer_text
                })
            except Exception as e:
                print(f"Error extracting question/answer: {e}")
        
        # Save questions to a JSON file
        with open('typescript_interview_questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        
        print(f"Scraped {len(questions)} questions and saved to typescript_interview_questions.json")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Here's a sample of the page source:")
        print(driver.page_source[:1000])  # Print first 1000 characters of the page source

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_typescript_questions()
