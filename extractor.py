import requests

class CanvasDataExtractor:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://{domain}/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_courses(self):
        url = f"{self.base_url}/courses"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_quiz_details(self, course_id, quiz_id):
        url = f"{self.base_url}/courses/{course_id}/quizzes/{quiz_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to fetch quiz details. Status code: {response.status_code}"

    def get_quiz_questions(self, course_id, quiz_id):
        url = f"{self.base_url}/courses/{course_id}/quizzes/{quiz_id}/questions"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to fetch quiz questions. Status code: {response.status_code}"

    def get_assignments(self, course_id):
        url = f"{self.base_url}/courses/{course_id}/assignments"
        response = requests.get(url, headers=self.headers)
        assignments = response.json()
        
        detailed_assignments = []
        for assignment in assignments:
            detailed_assignment = {
                "id": assignment.get("id"),
                "name": assignment.get("name"),
                "description": assignment.get("description"),
                "due_at": assignment.get("due_at"),
                "points_possible": assignment.get("points_possible"),
                "submission_types": assignment.get("submission_types"),
                "grading_type": assignment.get("grading_type"),
                "course_id": assignment.get("course_id"),
                "html_url": assignment.get("html_url"),
                "needs_grading_count": assignment.get("needs_grading_count"),
                "published": assignment.get("published"),
                "allowed_extensions": assignment.get("allowed_extensions"),
                "rubric": assignment.get("rubric")
            }
            
            if 'online_quiz' in assignment.get("submission_types", []):
                quiz_id = assignment.get("quiz_id")
                if quiz_id:
                    detailed_assignment["quiz_details"] = self.get_quiz_details(course_id, quiz_id)
                    detailed_assignment["quiz_questions"] = self.get_quiz_questions(course_id, quiz_id)
            
            detailed_assignments.append(detailed_assignment)
        
        return detailed_assignments

    def get_modules(self, course_id):
        url = f"{self.base_url}/courses/{course_id}/modules"
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

    def get_module_items(self, course_id, module_id):
        url = f"{self.base_url}/courses/{course_id}/modules/{module_id}/items"
        response = requests.get(url, headers=self.headers)
        items = response.json()
        
        detailed_items = []
        for item in items:
            detailed_item = item.copy()
            if item['type'] == 'Page':
                detailed_item['page_content'] = self.get_page_content(course_id, item['page_url'])
            elif item['type'] == 'Quiz':
                quiz_id = item['content_id']
                detailed_item['quiz_details'] = self.get_quiz_details(course_id, quiz_id)
                detailed_item['quiz_questions'] = self.get_quiz_questions(course_id, quiz_id)
            detailed_items.append(detailed_item)
        
        return detailed_items

    def extract_course_data(self, course_id):
        course_data = {
            "assignments": self.get_assignments(course_id),
            "modules": []
        }

        modules = self.get_modules(course_id)
        for module in modules:
            module_data = {
                "id": module["id"],
                "name": module["name"],
                "items": self.get_module_items(course_id, module["id"])
            }
            course_data["modules"].append(module_data)

        return course_data