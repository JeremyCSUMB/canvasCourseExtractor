from utils import format_date
import re
import html


def clean_html(raw_html):
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Decode HTML entities
    cleantext = html.unescape(cleantext)
    return cleantext.strip()


def preprocess_assignments(assignments):
    preprocessed = []
    for assignment in assignments:
        assignment_info = f"""
Assignment: {assignment['name']}
Due Date: {format_date(assignment['due_at'])}
Points: {assignment['points_possible']}

Description:
{clean_html(assignment['description'])}

Submission Type: {', '.join(assignment['submission_types'])}

Key Information:
- This assignment is worth {assignment['points_possible']} points.
- The submission type(s) accepted are: {', '.join(assignment['submission_types'])}.
- Students should start working on this assignment well before the due date.
- Students should follow the submission guidelines carefully.
- If students have any questions, they should ask the instructor for clarification.
"""
        if 'quiz_details' in assignment and 'quiz_questions' in assignment:
            assignment_info += f"\nQuiz Details:\n"
            assignment_info += f"Description: {clean_html(assignment['quiz_details'].get('description', 'No description'))}\n"
            assignment_info += f"Time Limit: {assignment['quiz_details'].get('time_limit', 'No time limit')} minutes\n"
            assignment_info += f"Allowed Attempts: {assignment['quiz_details'].get('allowed_attempts', 'Unlimited')}\n"

            assignment_info += "\nQuiz Questions:\n"
            for question in assignment['quiz_questions']:
                assignment_info += f"- {question.get('question_name', 'Unnamed Question')}\n"
                assignment_info += f"  Type: {question.get('question_type', 'Unknown')}\n"
                assignment_info += f"  Text: {clean_html(question.get('question_text', 'No text'))}\n\n"

        preprocessed.append(assignment_info.strip())
    return preprocessed


def preprocess_modules(modules):
    preprocessed = []
    for module in modules:
        module_info = f"""
Module: {module['name']}

Contents:
"""
        key_points = []
        for item in module['items']:
            module_info += f"- {item['title']} (Type: {item['type']})\n"
            if item['type'] == 'Page' and 'page_content' in item:
                clean_content = clean_html(item['page_content'])
                module_info += f"  Page Content:\n{clean_content}\n\n"
                # Extract potential key points from the page content
                sentences = re.split(r'(?<=[.!?])\s+', clean_content)
                key_sentences = [s for s in sentences if any(keyword in s.lower(
                ) for keyword in ['important', 'key', 'essential', 'crucial', 'remember'])]
                # Add up to 2 key sentences
                key_points.extend(key_sentences[:2])
            elif item['type'] == 'Quiz' and 'quiz_details' in item and 'quiz_questions' in item:
                module_info += f"  Quiz Details:\n"
                module_info += f"    Description: {clean_html(item['quiz_details'].get('description', 'No description'))}\n"
                module_info += f"    Time Limit: {item['quiz_details'].get('time_limit', 'No time limit')} minutes\n"
                module_info += f"    Allowed Attempts: {item['quiz_details'].get('allowed_attempts', 'Unlimited')}\n\n"
                module_info += f"  Quiz Questions:\n"
                for question in item['quiz_questions']:
                    module_info += f"    - {question.get('question_name', 'Unnamed Question')}\n"
                    module_info += f"      Type: {question.get('question_type', 'Unknown')}\n"
                    module_info += f"      Text: {clean_html(question.get('question_text', 'No text'))}\n\n"
                # Add a key point about the quiz
                key_points.append(
                    f"Complete the quiz '{item['title']}' to assess your understanding of the module content.")

        module_info += "\nKey Points:\n"
        for i, point in enumerate(key_points[:5], 1):  # Limit to 5 key points
            module_info += f"{i}. {point}\n"

        module_info += """
Students should:
- Review all module contents carefully.
- Complete all assignments and quizzes within the module.
- Pay special attention to the key points highlighted above.
- Reach out to the instructor if they have any questions or need clarification.
"""
        preprocessed.append(module_info.strip())
    return preprocessed


def preprocess_course_data(course_data):
    preprocessed_assignments = preprocess_assignments(
        course_data['assignments'])
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
This course covers [main topics]. Students will learn [key skills/knowledge].

Course Structure:
- The course is divided into several modules, each focusing on specific topics.
- Assignments and quizzes are distributed throughout the modules to assess understanding.
- Students should complete all module contents, assignments, and quizzes by their respective due dates.

General Guidelines:
1. Regular participation and engagement with course materials is essential for success.
2. Students should reach out to the instructor or teaching assistants for any clarifications or additional help.
3. Time management is crucial - start assignments early and don't leave things to the last minute.
4. Collaborate with peers when appropriate, but ensure all submitted work is your own.

If you have any questions about the course structure, assignments, or expectations, please don't hesitate to ask!
"""

    return course_info
