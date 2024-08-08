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
            detailed_assignments.append(detailed_assignment)
        
        return detailed_assignments

    def get_modules(self, course_id):
        url = f"{self.base_url}/courses/{course_id}/modules"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_module_items(self, course_id, module_id):
        url = f"{self.base_url}/courses/{course_id}/modules/{module_id}/items"
        response = requests.get(url, headers=self.headers)
        return response.json()

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
