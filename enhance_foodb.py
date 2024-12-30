import json
import time
import os
from openai import OpenAI
from typing import Dict, List, Any
import logging
import sys

# Configure more detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('foodb_enhancement.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_json_file(file_path: str) -> List:
    """Load JSON file and return its contents. Handles line-by-line JSON format."""
    try:
        logging.info(f"Attempting to load file: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        logging.error(f"Error parsing line in {file_path}: {str(e)}")
                        logging.error(f"Problematic line: {line[:100]}...")
                        continue
                        
        logging.info(f"Successfully loaded {len(data)} items from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading {file_path}: {str(e)}")
        raise

def save_json_file(data: List, file_path: str) -> None:
    """Save data to JSON file."""
    try:
        logging.info(f"Attempting to save file: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Successfully saved {file_path}")
    except Exception as e:
        logging.error(f"Error saving {file_path}: {str(e)}")
        raise

def get_translations_and_calories(food_name: str, description: str) -> Dict:
    """Get translations and calorie information using OpenAI API."""
    try:
        logging.info(f"Requesting translations for: {food_name}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional food and nutrition translator. Follow these rules strictly:
1. Provide accurate translations in their native scripts
2. For Chinese, use simplified Chinese characters (汉字) NOT pinyin
3. For Japanese, use a mix of kanji and kana as appropriate
4. Ensure all translations maintain the exact meaning of the original food name
5. For calories, provide realistic estimates based on nutritional databases"""
                },
                {
                    "role": "user",
                    "content": f"""Translate this food item accurately:

Food Name: {food_name}
Description: {description}

Return ONLY a JSON object with these exact fields:
- spanish: (Spanish translation in Spanish)
- french: (French translation in French)
- chinese: (Simplified Chinese characters ONLY, NO pinyin)
- japanese: (Japanese in kanji/kana)
- korean: (Korean in Hangul)
- german: (German translation in German)
- calories_per_100g: (realistic numeric value)

Example format:
{{
  "spanish": "manzana",
  "french": "pomme",
  "chinese": "苹果",
  "japanese": "りんご",
  "korean": "사과",
  "german": "Apfel",
  "calories_per_100g": 52
}}"""
                }
            ],
            temperature=0.3,  # Reduced temperature for more consistent outputs
            max_tokens=500,
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        logging.info(f"Received response for {food_name}: {content[:200]}...")  # Log first 200 chars of response
        
        parsed_response = json.loads(content)
        
        # Validate required fields
        required_fields = ['spanish', 'french', 'chinese', 'japanese', 'korean', 'german', 'calories_per_100g']
        missing_fields = [field for field in required_fields if field not in parsed_response]
        if missing_fields:
            logging.error(f"Missing required fields in API response for {food_name}: {missing_fields}")
            return None
            
        return parsed_response
            
    except Exception as e:
        logging.error(f"Error processing {food_name}: {str(e)}")
        if 'response' in locals():
            logging.error(f"Last API response: {getattr(response, 'choices', [])}")
        return None

def process_food_batch(food_data: List, start_idx: int, batch_size: int) -> List:
    """Process a batch of food items and return enhanced data."""
    end_idx = min(start_idx + batch_size, len(food_data))
    enhanced_data_list = []
    
    for i in range(start_idx, end_idx):
        food_item = food_data[i]
        try:
            logging.info(f"Processing item {i+1}/{len(food_data)}: {food_item.get('name', 'unknown')}")
            
            # Create a copy of the original item
            enhanced_item = food_item.copy()
            
            # Get translations and calories
            api_data = get_translations_and_calories(
                food_item.get('name', ''),
                food_item.get('description', '')
            )
            
            if api_data:
                # Only add new translations and calories
                enhanced_item['multilingual'] = {
                    'es': api_data['spanish'],
                    'fr': api_data['french'],
                    'zh': api_data['chinese'],
                    'ja': api_data['japanese'],
                    'ko': api_data['korean'],
                    'de': api_data['german']
                }
                enhanced_item['calories_per_100g'] = api_data['calories_per_100g']
            
            enhanced_data_list.append(enhanced_item)
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            logging.error(f"Error processing food item {food_item.get('name', 'unknown')}: {str(e)}")
            enhanced_data_list.append(food_item)  # Keep original item on error
            continue
    
    return enhanced_data_list

def enhance_food_data(input_dir: str, output_dir: str) -> None:
    """Enhance food data with translations and calories."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load Food.json
        input_file = os.path.join(input_dir, 'Food.json')
        output_file = os.path.join(output_dir, 'Food.json')
        
        food_data = load_json_file(input_file)
        
        if not isinstance(food_data, list):
            raise ValueError(f"Expected list in Food.json, got {type(food_data)}")
        
        logging.info(f"Processing {len(food_data)} food items")
        
        # Process in smaller batches and accumulate results
        BATCH_SIZE = 5
        all_enhanced_data = []
        
        for start_idx in range(0, len(food_data), BATCH_SIZE):
            batch_data = process_food_batch(food_data[start_idx:], start_idx, BATCH_SIZE)
            all_enhanced_data.extend(batch_data)
            
            # Save progress after each batch
            save_json_file(all_enhanced_data, output_file)
            logging.info(f"Saved progress: {len(all_enhanced_data)}/{len(food_data)} items processed")
            
        logging.info("Enhancement completed successfully")
        
    except Exception as e:
        logging.error(f"Error in enhance_food_data: {str(e)}")
        raise

def main():
    try:
        # Initialize OpenAI client
        global client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        client = OpenAI(api_key=api_key)
        
        # Get the current working directory
        current_dir = os.getcwd()
        
        # Define input and output directories
        input_dir = os.path.join(current_dir, "original_foodb_2020_04_07_json")
        output_dir = os.path.join(current_dir, "enhanced_foodb/list")
        
        logging.info(f"Current directory: {current_dir}")
        logging.info(f"Input directory: {input_dir}")
        logging.info(f"Output directory: {output_dir}")
        
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        enhance_food_data(input_dir, output_dir)
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 