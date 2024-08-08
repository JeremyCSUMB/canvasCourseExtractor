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
        preprocessed.append({"prompt": prompt.strip(), "completion": completion.strip()})
    return preprocessed

def preprocess_modules(modules):
    preprocessed = []
    for module in modules:
        module_content = f"Module: {module['name']}\n\nContents:"
        for item in module['items']:
            module_content += f"\n- {item['title']} (Type: {item['type']})"
        
        prompt = f"{module_content}\n\nSummarize this module's content and structure."
        completion = "This module covers [main topics]. It is structured as follows:\n1. [Key point about structure]\n2. [Another key point]\n3. [Another key point]"
        
        preprocessed.append({"prompt": prompt.strip(), "completion": completion.strip()})
    return preprocessed
