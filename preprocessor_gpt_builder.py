import json
import re
import html
from datetime import datetime, timedelta

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html.unescape(cleantext)
    return cleantext.strip()

def format_date(date_string):
    if date_string:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        pacific_offset = timedelta(hours=-7)
        dt_pacific = dt + pacific_offset
        return dt_pacific.strftime('%Y-%m-%d %I:%M:%S %p PT')
    return 'No due date'

def preprocess_assignments(assignments):
    preprocessed = []
    for assignment in assignments:
        assignment_info = f"""
Assignment: {assignment['name']}
Due Date: {format_date(assignment.get('due_at'))}
Points: {assignment['points_possible']}

Description:
{clean_html(assignment.get('description', 'No description provided'))}

Submission Type: {', '.join(assignment.get('submission_types', ['Not specified']))}

Key Information:
- This assignment is worth {assignment['points_possible']} points.
- The submission type(s) accepted are: {', '.join(assignment.get('submission_types', ['Not specified']))}.
- Students should start working on this assignment well before the due date.
- Students should follow the submission guidelines carefully.
- If students have any questions, they should ask the instructor for clarification.
"""
        if 'quiz_details' in assignment:
            assignment_info += process_quiz_details(assignment['quiz_details'])
        
        preprocessed.append(assignment_info.strip())
    return preprocessed

def preprocess_modules(modules):
    preprocessed = []
    for module in modules:
        module_info = f"""
Module: {module['name']}

Contents:
"""
        for item in module['items']:
            due_date = format_date(item.get('due_at'))
            item_type = item.get('type', 'Unknown')
            module_info += f"- {item['title']} (Type: {item_type}, Due: {due_date})\n"
            
            if item_type == 'Page' and 'page_url' in item:
                module_info += f"  Page URL: {item['url']}\n"
                if 'page_content' in item:
                    module_info += f"  Page Content: {clean_html(item['page_content'])}\n"
            elif item_type in ['Assignment', 'Quiz', 'Discussion']:
                module_info += process_assignment_or_quiz(item)

        key_points = extract_key_points(module_info)
        module_info += f"""
Key Points:
{key_points}

Students should:
- Review all module contents carefully.
- Complete all assignments and quizzes within the module.
- Pay special attention to the key points highlighted above.
- Reach out to the instructor if they have any questions or need clarification.
"""
        preprocessed.append(module_info.strip())
    return preprocessed

def process_assignment_or_quiz(item):
    item_info = "  Details:\n"
    item_info += f"    Points: {item.get('content', {}).get('points_possible', 'Not specified')}\n"
    item_info += f"    Submission Type: {', '.join(item.get('content', {}).get('submission_types', ['Not specified']))}\n"
    if 'content' in item and 'description' in item['content']:
        item_info += f"    Description: {clean_html(item['content']['description'])}\n"
    if 'quiz_details' in item:
        item_info += process_quiz_details(item['quiz_details'])
    return item_info

def process_quiz_details(quiz_details):
    quiz_info = f"  Quiz Details:\n"
    quiz_info += f"    Quiz ID: {quiz_details.get('id', 'Not specified')}\n"
    quiz_info += f"    Title: {quiz_details.get('title', 'Not specified')}\n"
    quiz_info += f"    Description: {clean_html(quiz_details.get('description', 'No description provided'))}\n"
    quiz_info += f"    Time Limit: {quiz_details.get('time_limit', 'No time limit')} minutes\n"
    quiz_info += f"    Allowed Attempts: {quiz_details.get('allowed_attempts', 'Unlimited')}\n"
    quiz_info += f"    Due Date: {format_date(quiz_details.get('due_at'))}\n"
    quiz_info += f"    Points Possible: {quiz_details.get('points_possible', 'Not specified')}\n"
    
    if 'quiz_questions' in quiz_details:
        quiz_info += "    Questions:\n"
        for question in quiz_details['quiz_questions']:
            quiz_info += f"      - Type: {question['question_type']}\n"
            quiz_info += f"        Text: {clean_html(question['question_text'])}\n"
            if question['question_type'] == 'multiple_choice_question':
                quiz_info += "        Options:\n"
                for answer in question.get('answers', []):
                    quiz_info += f"          * {clean_html(answer['text'])}\n"
    
    return quiz_info

def extract_key_points(module_info):
    lines = module_info.split('\n')
    key_points = []
    for line in lines:
        if any(keyword in line.lower() for keyword in ['important', 'key', 'essential', 'crucial', 'remember']):
            key_points.append(line.strip())
    return "\n".join(key_points[:5]) if key_points else "No specific key points identified."

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

    course_info += """

Course Overview:
This course covers various topics related to effective learning strategies and time management. Students will learn how to set goals, manage their time effectively, take strategic notes, prepare for exams, and adapt their learning techniques to new contexts.

Course Structure:
- The course is divided into several milestones, each focusing on specific skills and techniques.
- Assignments, discussions, and quizzes are distributed throughout the modules to assess understanding and promote active learning.
- Students should complete all module contents, assignments, and quizzes by their respective due dates.

General Guidelines:
1. Regular participation and engagement with course materials is essential for success.
2. Students should reach out to the instructor or teaching assistants for any clarifications or additional help.
3. Time management is crucial - start assignments early and don't leave things to the last minute.
4. Collaborate with peers when appropriate, but ensure all submitted work is your own.
5. Apply the learning techniques and strategies discussed in the course to your other academic pursuits.

If you have any questions about the course structure, assignments, or expectations, please don't hesitate to ask!
"""

    return course_info

def preprocess_from_raw_data(course_id):
    # Load raw data
    with open(f'course_{course_id}_raw_data.json', 'r') as f:
        raw_data = json.load(f)
    
    # Preprocess data
    preprocessed_data = preprocess_course_data(raw_data)
    
    # Save preprocessed data
    with open(f'course_{course_id}_preprocessed_gpt_builder.txt', 'w', encoding='utf-8') as f:
        f.write(preprocessed_data)
    
    print(f"Preprocessed data for course {course_id} has been saved to course_{course_id}_preprocessed_gpt_builder.txt")

if __name__ == "__main__":
    course_id = input("Enter the course ID: ")
    preprocess_from_raw_data(course_id)