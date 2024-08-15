import json
import requests
from config import load_config

class CanvasDataExtractor:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://{domain}/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_course_data(self, course_id):
        course_data = {
            "assignments": self.get_assignments(course_id),
            "modules": self.get_modules(course_id)
        }
        return course_data

    def get_assignments(self, course_id):
        url = f"{self.base_url}/courses/{course_id}/assignments"
        response = requests.get(url, headers=self.headers)
        assignments = response.json()
        
        for assignment in assignments:
            if 'online_quiz' in assignment.get("submission_types", []):
                quiz_id = assignment.get("quiz_id")
                if quiz_id:
                    assignment["quiz_details"] = self.get_quiz_details(course_id, quiz_id)
                    assignment["quiz_questions"] = self.get_quiz_questions(course_id, quiz_id)
        
        return assignments

    def get_modules(self, course_id):
        url = f"{self.base_url}/courses/{course_id}/modules"
        response = requests.get(url, headers=self.headers)
        modules = response.json()
        
        for module in modules:
            module['items'] = self.get_module_items(course_id, module['id'])
        
        return modules

    def get_module_items(self, course_id, module_id):
        url = f"{self.base_url}/courses/{course_id}/modules/{module_id}/items"
        response = requests.get(url, headers=self.headers)
        items = response.json()
        
        for item in items:
            if item['type'] == 'Page':
                item['page_content'] = self.get_page_content(course_id, item['page_url'])
            elif item['type'] == 'Quiz':
                quiz_id = item['content_id']
                item['quiz_details'] = self.get_quiz_details(course_id, quiz_id)
                item['quiz_questions'] = self.get_quiz_questions(course_id, quiz_id)
        
        return items

    def get_quiz_details(self, course_id, quiz_id):
        url = f"{self.base_url}/courses/{course_id}/quizzes/{quiz_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_quiz_questions(self, course_id, quiz_id):
        url = f"{self.base_url}/courses/{course_id}/quizzes/{quiz_id}/questions"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_page_content(self, course_id, page_url):
        url = f"{self.base_url}/courses/{course_id}/pages/{page_url}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            page_data = response.json()
            return page_data.get('body', '')
        else:
            return f"Failed to fetch page content. Status code: {response.status_code}"

def extract_course_data(course_id):
    config = load_config()
    extractor = CanvasDataExtractor(config['api_key'], config['domain'])
    
    course_data = extractor.get_course_data(course_id)
    
    with open(f'course_{course_id}_raw_data.json', 'w') as f:
        json.dump(course_data, f, indent=2)
    
    print(f"Raw data for course {course_id} has been saved to course_{course_id}_raw_data.json")
    
    return course_data

if __name__ == "__main__":
    course_id = input("Enter the course ID: ")
    extract_course_data(course_id)