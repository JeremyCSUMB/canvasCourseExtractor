import argparse
from extractor import CanvasDataExtractor
import preprocessor_llm as preprocessor_llm
import preprocessor_gpt_builder as preprocessor_gpt_builder
from utils import save_json, save_text
from config import load_config

def main():
    parser = argparse.ArgumentParser(description="Canvas Course Extractor: Extract and preprocess Canvas course data")
    parser.add_argument("course_id", help="The ID of the course to extract data from")
    parser.add_argument("--raw", action="store_true", help="Save the raw extracted data")
    parser.add_argument("--preprocessed", choices=['llm', 'gpt_builder'], help="Preprocess data for LLM fine-tuning or GPT Builder")
    args = parser.parse_args()

    config = load_config()
    
    extractor = CanvasDataExtractor(config['api_key'], config['domain'])
    
    print(f"Extracting data for course {args.course_id}...")
    course_data = extractor.extract_course_data(args.course_id)

    if args.raw or not args.preprocessed:
        raw_filename = f"course_{args.course_id}_raw_data.json"
        save_json(course_data, raw_filename)
        print(f"Raw data saved to {raw_filename}")

    if args.preprocessed:
        if args.preprocessed == 'llm':
            preprocessed_assignments = preprocessor_llm.preprocess_assignments(course_data['assignments'])
            preprocessed_modules = preprocessor_llm.preprocess_modules(course_data['modules'])
            all_preprocessed = preprocessed_assignments + preprocessed_modules
            preprocessed_filename = f"course_{args.course_id}_preprocessed_llm.json"
            save_json(all_preprocessed, preprocessed_filename)
        elif args.preprocessed == 'gpt_builder':
            preprocessed_data = preprocessor_gpt_builder.preprocess_course_data(course_data)
            preprocessed_filename = f"course_{args.course_id}_preprocessed_gpt_builder.txt"
            save_text(preprocessed_data, preprocessed_filename)
        print(f"Preprocessed data saved to {preprocessed_filename}")

if __name__ == "__main__":
    main()