import argparse
from extractor import CanvasDataExtractor
from preprocessor import preprocess_assignments, preprocess_modules
from utils import save_json
from config import load_config

def main():
    parser = argparse.ArgumentParser(description="Canvas Course Extractor: Extract and preprocess Canvas course data")
    parser.add_argument("course_id", help="The ID of the course to extract data from")
    parser.add_argument("--raw", action="store_true", help="Save the raw extracted data")
    parser.add_argument("--preprocessed", action="store_true", help="Save the preprocessed data")
    args = parser.parse_args()

    config = load_config()
    
    extractor = CanvasDataExtractor(config['api_key'], config['domain'])
    
    print(f"Extracting data for course {args.course_id}...")
    course_data = extractor.extract_course_data(args.course_id)

    if args.raw or not args.preprocessed:
        raw_filename = f"course_{args.course_id}_raw_data.json"
        save_json(course_data, raw_filename)
        print(f"Raw data saved to {raw_filename}")

    if args.preprocessed or not args.raw:
        preprocessed_assignments = preprocess_assignments(course_data['assignments'])
        preprocessed_modules = preprocess_modules(course_data['modules'])
        all_preprocessed = preprocessed_assignments + preprocessed_modules
        preprocessed_filename = f"course_{args.course_id}_preprocessed_data.json"
        save_json(all_preprocessed, preprocessed_filename)
        print(f"Preprocessed data saved to {preprocessed_filename}")

if __name__ == "__main__":
    main()
