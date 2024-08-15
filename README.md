# Canvas Course Extractor (CCE)

Canvas Course Extractor (CCE) is a powerful Python-based command-line tool designed to extract and preprocess course data from the Canvas Learning Management System. It's an invaluable resource for educators, researchers, and data scientists who want to analyze course content or prepare data for machine learning models, including GPT Builder.

## Features

- Extract comprehensive information about assignments and modules from Canvas courses
- Preprocess extracted data into formats suitable for:
  - Language Model (LLM) fine-tuning
  - GPT Builder projects
- User-friendly command-line interface
- Modular structure for easy maintenance and extensibility

## Prerequisites

- Python 3.7+
- A Canvas LMS account with API access

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/canvas-course-extractor.git
   cd canvas-course-extractor
   ```

2. Install the required Python packages:
   ```
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the project root directory with your Canvas API key and domain:
   ```
   CANVAS_API_KEY=your_api_key_here
   CANVAS_DOMAIN=your_canvas_domain.instructure.com
   ```

## Usage

Run the script from the command line using the following syntax:

```
python main.py <course_id> [--raw] [--preprocessed {llm,gpt_builder}]
```

Arguments:
- `course_id`: The ID of the course you want to extract data from (required)
- `--raw`: Save the raw extracted data
- `--preprocessed`: Preprocess the data, with options:
  - `llm`: Format data for LLM fine-tuning (JSON output)
  - `gpt_builder`: Format data for GPT Builder projects (text output)

Examples:
```
python main.py 12345 --raw
python main.py 12345 --preprocessed llm
python main.py 12345 --preprocessed gpt_builder
```

## Project Structure

- `main.py`: Entry point of the application
- `extractor.py`: Contains the `CanvasDataExtractor` class for fetching data from Canvas
- `preprocessor_llm.py`: Contains functions for preprocessing data for LLM fine-tuning
- `preprocessor_gpt_builder.py`: Contains functions for preprocessing data for GPT Builder
- `utils.py`: Contains utility functions used across the project
- `config.py`: Handles configuration and environment variables

## Output

- Raw data is saved as JSON files (e.g., `course_12345_raw_data.json`)
- LLM preprocessed data is saved as JSON files (e.g., `course_12345_preprocessed_llm.json`)
- GPT Builder preprocessed data is saved as text files (e.g., `course_12345_preprocessed_gpt_builder.txt`)

## Using Preprocessed Data with GPT Builder

After preprocessing your course data for GPT Builder, you can use it to create a custom GPT that acts as an AI tutor for your course. Here's how to set it up:

1. Go to the GPT Builder interface on the OpenAI platform.
2. Create a new custom GPT.
3. In the "Knowledge" section, upload the preprocessed text file (e.g., `course_12345_preprocessed_gpt_builder.txt`).
4. In the "Instructions" section, use the following prompt to guide the AI's behavior:

```
You are an AI tutor assistant for a specific course. Your knowledge comes from the uploaded course information, which includes details about assignments and modules. Your role is to:

1. Provide accurate information about assignments, including their names, due dates, point values, and submission types.
2. Explain the main objectives and key information for each assignment.
3. Offer an overview of course modules, their contents, and learning objectives.
4. Assist students in understanding assignment requirements and course structure.
5. Encourage good study habits and time management.
6. Remind students of important deadlines and submission guidelines.
7. Direct students to ask their instructor for clarification on any unclear points.

When asked about specific assignments or modules, refer to the provided course information. If a question is outside the scope of the provided information, politely explain that you can only assist with the information available in the course outline.

Never invent or assume information not present in the provided course data. If you're unsure about any details, ask the student to check with their instructor or the official course materials.

Remember, your goal is to support student learning and success in the course while maintaining academic integrity. Do not complete assignments for students or provide answers that would compromise the learning process.
```

5. Customize the instructions further based on your specific needs and the nature of your course.

## Contributing

We welcome contributions to the Canvas Course Extractor! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Canvas LMS team for providing a robust API
- Inspired by educators and researchers working to enhance online learning experiences
- Built with love for the educational community

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository. We'll do our best to provide timely support and address any concerns.

---

Happy extracting and may your courses be ever engaging!