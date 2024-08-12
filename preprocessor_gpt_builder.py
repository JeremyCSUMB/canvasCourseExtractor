from utils import format_date

def preprocess_assignments(assignments):
    preprocessed = []
    for assignment in assignments:
        assignment_info = f"""
Assignment Name: {assignment['name']}
Due Date: {format_date(assignment['due_at'])}
Points: {assignment['points_possible']}
Submission Type: {', '.join(assignment['submission_types'])}

Description:
{assignment['description']}

Key Information:
- This assignment is worth {assignment['points_possible']} points.
- The submission type(s) accepted are: {', '.join(assignment['submission_types'])}.
- Students should start working on this assignment well before the due date.
- Students should follow the submission guidelines carefully.
- If students have any questions, they should ask the instructor for clarification.

Main Objectives:
1. [First main objective extracted from the description]
2. [Second main objective extracted from the description]
3. [Third main objective extracted from the description]
"""
        if 'quiz_details' in assignment and 'quiz_questions' in assignment:
            assignment_info += f"\nQuiz Details:\n"
            assignment_info += f"Description: {assignment['quiz_details'].get('description', 'No description')}\n"
            assignment_info += f"Time Limit: {assignment['quiz_details'].get('time_limit', 'No time limit')} minutes\n"
            assignment_info += f"Allowed Attempts: {assignment['quiz_details'].get('allowed_attempts', 'Unlimited')}\n"
            
            assignment_info += "\nQuiz Questions:\n"
            for question in assignment['quiz_questions']:
                assignment_info += f"- {question.get('question_name', 'Unnamed Question')}\n"
                assignment_info += f"  Type: {question.get('question_type', 'Unknown')}\n"
                assignment_info += f"  Text: {question.get('question_text', 'No text')}\n\n"

        preprocessed.append(assignment_info.strip())
    return preprocessed

def preprocess_modules(modules):
    preprocessed = []
    for module in modules:
        module_info = f"""
Module Name: {module['name']}

Contents:
"""
        for item in module['items']:
            module_info += f"- {item['title']} (Type: {item['type']})\n"
            if item['type'] == 'Page' and 'page_content' in item:
                module_info += f"  Page Content:\n{item['page_content']}\n\n"
            elif item['type'] == 'Quiz' and 'quiz_details' in item and 'quiz_questions' in item:
                module_info += f"  Quiz Details:\n"
                module_info += f"    Description: {item['quiz_details'].get('description', 'No description')}\n"
                module_info += f"    Time Limit: {item['quiz_details'].get('time_limit', 'No time limit')} minutes\n"
                module_info += f"    Allowed Attempts: {item['quiz_details'].get('allowed_attempts', 'Unlimited')}\n\n"
                module_info += f"  Quiz Questions:\n"
                for question in item['quiz_questions']:
                    module_info += f"    - {question.get('question_name', 'Unnamed Question')}\n"
                    module_info += f"      Type: {question.get('question_type', 'Unknown')}\n"
                    module_info += f"      Text: {question.get('question_text', 'No text')}\n\n"
        
        module_info += """
Summary:
This module covers [main topics]. It is structured as follows:
1. [Key point about structure]
2. [Another key point]
3. [Another key point]

Learning Objectives:
1. [First learning objective]
2. [Second learning objective]
3. [Third learning objective]
"""
        preprocessed.append(module_info.strip())
    return preprocessed

def preprocess_course_data(course_data):
    preprocessed_assignments = preprocess_assignments(course_data['assignments'])
    preprocessed_modules = preprocess_modules(course_data['modules'])
    
    course_info = f"""
Course Information:

Assignments:
{'-' * 40}
""" + "\n\n".join(preprocessed_assignments) + f"""

Modules:
{'-' * 40}
""" + "\n\n".join(preprocessed_modules)

    return course_info