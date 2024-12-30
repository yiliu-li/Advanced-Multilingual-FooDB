# Advanced Multilingual FooDB

This project enhances the FooDB dataset by adding multilingual translations and nutritional information using OpenAI's GPT API. The enhanced dataset includes accurate translations in multiple languages and estimated calorie content, while preserving all original data.

## Data Sources and Disclaimers

- **FooDB Data**: This project builds upon the FooDB dataset (https://foodb.ca/). All original data is subject to FooDB's terms and conditions. FooDB is Canada's food composition database, containing detailed nutritional information about foods, their chemistry, and their biology.

- **Generated Translations**: The multilingual translations and calorie estimates are generated using OpenAI's GPT API. While efforts have been made to ensure quality:
  - These translations are AI-generated and may not be 100% accurate
  - The data should not be used for professional, medical, or commercial purposes
  - Calorie estimates are approximations and should not be relied upon for dietary planning
  - For accurate nutritional information, please consult official food databases or nutritionists

## Overview

The project processes the original FooDB food entries to add:

- Professional translations in 6 languages (Spanish, French, Chinese, Japanese, Korean, German)
- Estimated calories per 100g based on nutritional databases
- All original data fields are preserved unchanged

## Project Structure

```
Advanced-Multilingual-FooDB/
├── foodb_2020_04_07_json/    # Original FooDB dataset directory
│   ├── Food.json             # Main food data (line-by-line JSON format)
│   └── ...                   # Other data (line-by-line JSON format)
├── enhanced_foodb/           # Enhanced dataset output directory
│   ├── list/                 # JSON array format output
│   │   └── Food.json        # Enhanced data in array format
│   └── line/                 # Line-by-line format output
│       └── Food.json  # Enhanced data in line format
├── enhance_foodb.py          # Main enhancement script
├── convert_to_lines.py       # JSON format converter
└── README.md                 # This documentation
```

## Scripts

### 1. enhance_foodb.py

Main processing script that:

- Reads the original Food.json file from `original_foodb_2020_04_07_json`
- Processes each food item through OpenAI's GPT API
- Adds translations and calorie information
- Saves enhanced data to `enhanced_foodb/list/Food.json`

Key Features:

- Batch processing (5 items per batch) with automatic progress saving
- Comprehensive error handling and logging
- API rate limiting (1 request/second)
- Progress tracking and resumable processing
- Validates API responses for required fields

### 2. convert_to_lines.py

Utility script that:

- Reads the enhanced array JSON from `enhanced_foodb/list/Food.json`
- Converts to line-by-line format
- Saves output to `enhanced_foodb/line/Food.json`
- Preserves all data fields and formatting

## Setup and Usage

1. **Prerequisites**

   ```bash
   # Install required Python package
   pip install openai
   ```
2. **Set OpenAI API Key**

   ```bash
   # For temporary use
   export OPENAI_API_KEY="your-api-key-here"

   # For permanent use (add to ~/.zshrc)
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```
3. **Run Enhancement Script**

   ```bash
   python enhance_foodb.py
   ```

   - Creates enhanced data in `enhanced_foodb/list/Food.json`
   - Check `foodb_enhancement.log` for progress and any errors
4. **Convert Format (Optional)**

   ```bash
   python convert_to_lines.py
   ```

   - Converts array format to line-by-line format
   - Saves output to `enhanced_foodb/line/Food.json`

## Output Format

The enhanced data maintains all original fields and adds two new ones:

```json
{
  "id": 1,
  "name": "Original Name",
  "description": "Original description",
  ... (all original fields preserved) ...,
  "multilingual": {
    "es": "Spanish Name",
    "fr": "French Name",
    "zh": "Chinese Name (汉字)",
    "ja": "Japanese Name (漢字/かな)",
    "ko": "Korean Name (한글)",
    "de": "German Name"
  },
  "calories_per_100g": 123
}
```

## Error Handling and Logging

- **Log File**: `foodb_enhancement.log` contains:

  - Detailed processing information
  - API response data
  - Error messages and stack traces
  - Progress updates
- **Error Recovery**:

  - Failed items retain original data
  - Script can be safely interrupted and resumed
  - Automatic progress saving every 5 items
  - Validation of API responses

## Important Notes

- **Data Quality**:
  - Chinese translations use simplified characters (汉字), never pinyin
  - Japanese translations use appropriate kanji/kana mix
  - All translations are contextually appropriate for food items
  - Calorie estimates based on standard nutritional databases
  - Translations are AI-generated and may not be 100% accurate
  - Data should not be used for professional, medical, or commercial purposes
  - Calorie estimates are approximations and should not be relied upon for dietary planning

- **API Usage**:
  - Rate limited to 1 request per second
  - Approximately 1000 tokens per request
  - Each food item requires one API call

- **Performance**:
  - Processes 5 items per batch
  - ~3600 items per hour (with rate limiting)
  - Progress automatically saved between batches

## Contact

For questions about this enhanced dataset or the translation process, please contact:
- Yiliu (Aiden) Li (yiliu.li@outlook.com)

For questions about FooDB data usage, please contact the FooDB team directly through their website.

## License

This project enhances the FooDB dataset (https://foodb.ca/). The original FooDB data is subject to FooDB's terms and conditions as Canada's food composition database. The enhanced translations and calorie data are provided for research and educational purposes only, with no warranty of accuracy or fitness for any particular purpose. Commercial use of the enhanced data requires compliance with FooDB's licensing terms.
