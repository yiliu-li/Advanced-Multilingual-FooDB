import json
import os

def convert_json_to_lines(input_file: str, output_file: str) -> None:
    """Convert array JSON to line-by-line format."""
    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")
    
    try:
        # Read the JSON array
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Input file must contain a JSON array")
            
        print(f"Found {len(data)} items to convert")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write each object as a separate line
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                json_line = json.dumps(item, ensure_ascii=False)
                f.write(json_line + '\n')
        
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.getcwd()
    
    # Define input and output files
    input_file = os.path.join(current_dir, "enhanced_foodb/list", "Food.json")
    output_file = os.path.join(current_dir, "enhanced_foodb/line", "Food.json")
    
    convert_json_to_lines(input_file, output_file) 