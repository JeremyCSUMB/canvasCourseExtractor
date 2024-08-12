from utils import format_date

def preprocess_assignments(assignments):
    preprocessed = []
    for assignment in assignments:
        prompt = f"""
Assignment: {assignment['name']}
Due Date: {format_date(assignment['due_at'])}
Points: {assignment['points_possible']}

Description:
{assignment['description']}

Submission Type: {', '.join(assignment['submission_types'])}
"""
        completion = f"""
This assignment is worth {assignment['points_possible']} points and is due on {format_date(assignment['due_at'])}.
The submission type(s) accepted are: {', '.join(assignment['submission_types'])}.

Key points about the assignment:
1. [Extract 3-5 key points from the description]

Remember:
- Start working on this assignment well before the due date.
- Follow the submission guidelines carefully.
- If you have any questions, ask your instructor for clarification.
"""
        if 'quiz_details' in assignment and 'quiz_questions' in assignment:
            prompt += "\nQuiz Details:\n"
            prompt += f"Description: {assignment['quiz_details'].get('description', 'No description')}\n"
            prompt += f"Time Limit: {assignment['quiz_details'].get('time_limit', 'No time limit')} minutes\n"
            prompt += f"Allowed Attempts: {assignment['quiz_details'].get('allowed_attempts', 'Unlimited')}\n"
            
            prompt += "\nQuiz Questions:\n"
            for question in assignment['quiz_questions']:
                prompt += f"- {question.get('question_name', 'Unnamed Question')}\n"
                prompt += f"  Type: {question.get('question_type', 'Unknown')}\n"
                prompt += f"  Text: {question.get('question_text', 'No text')}\n\n"
            
            completion += "\nAdditional quiz information:\n"
            completion += "- Review the quiz details carefully, noting the time limit and number of allowed attempts.\n"
            completion += "- Familiarize yourself with the types of questions in the quiz.\n"
            completion += "- Prepare thoroughly for all topics covered in the quiz questions.\n"

        preprocessed.append({"prompt": prompt.strip(), "completion": completion.strip()})
    return preprocessed

def preprocess_modules(modules):
    preprocessed = []
    for module in modules:
        module_content = f"Module: {module['name']}\n\nContents:"
        for item in module['items']:
            module_content += f"\n- {item['title']} (Type: {item['type']})"
            if item['type'] == 'Page' and 'page_content' in item:
                module_content += f"\n  Page Content:\n{item['page_content']}"
            elif item['type'] == 'Quiz' and 'quiz_details' in item and 'quiz_questions' in item:
                module_content += f"\n  Quiz Details:"
                module_content += f"\n    Description: {item['quiz_details'].get('description', 'No description')}"
                module_content += f"\n    Time Limit: {item['quiz_details'].get('time_limit', 'No time limit')} minutes"
                module_content += f"\n    Allowed Attempts: {item['quiz_details'].get('allowed_attempts', 'Unlimited')}"
                module_content += f"\n  Quiz Questions:"
                for question in item['quiz_questions']:
                    module_content += f"\n    - {question.get('question_name', 'Unnamed Question')}"
                    module_content += f"\n      Type: {question.get('question_type', 'Unknown')}"
                    module_content += f"\n      Text: {question.get('question_text', 'No text')}"
        
        prompt = f"{module_content}\n\nSummarize this module's content and structure."
        completion = """
This module covers [main topics]. It is structured as follows:
1. [Key point about structure]
2. [Another key point]
3. [Another key point]

Learning Objectives:
1. [First learning objective]
2. [Second learning objective]
3. [Third learning objective]

Key points to remember:
- [Important point about the module content]
- [Another important point]
- [Another important point]
"""
        
        preprocessed.append({"prompt": prompt.strip(), "completion": completion.strip()})
    return preprocessed