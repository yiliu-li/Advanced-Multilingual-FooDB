# Advanced Multilingual FooDB Food Data

This project enhances the FooDB food dataset by adding multilingual translations and nutritional information using OpenAI's GPT API. The enhanced dataset includes accurate translations in multiple languages and estimated calorie content, while preserving all original data.

## Data Sources and Disclaimers

### Original FooDB Data
- **Source**: The original data comes from FooDB (https://foodb.ca/), Canada's food composition database
- **Repository Data**: This repository includes the required `Food.json` file in `original_foodb_2020_04_07_json/`
- **Full Dataset**: If needed, the complete FooDB dataset (including Compounds, Nutrients, etc.) can be downloaded from:
  - Official Website: https://foodb.ca/downloads
  - Direct JSON Download: https://foodb.ca/public/system/downloads/foodb_2020_4_7_json.tar.gz

### Enhanced Data
- **Translations**: Generated using OpenAI's GPT API with careful prompt engineering
- **Quality Control**:
  - Translations are AI-generated and reviewed for food-specific terminology
  - Calorie estimates are approximations based on nutritional databases
  - Data is provided for research and educational purposes only
  - For professional use, please verify with official sources

## Overview

The project focuses on enriching the FooDB food entries with:
- Professional translations in 6 languages (Spanish, French, Chinese, Japanese, Korean, German)
- Estimated calories per 100g based on nutritional databases
- All original food data fields are preserved unchanged

## Project Structure

```
Advanced-Multilingual-FooDB/
├── original_foodb_2020_04_07_json/    # Original FooDB food data
│   └── Food.json                      # Original food entries (line-by-line JSON)
├── enhanced_foodb/                    # Enhanced dataset output
│   ├── list/                         # JSON array format output
│   │   └── Food.json                # Enhanced data in array format
│   └── line/                        # Line-by-line format output
│       └── Food.json                # Enhanced data in line format
├── enhance_foodb.py                  # Main enhancement script
├── convert_to_lines.py               # JSON format converter
└── README.md                         # This documentation
```

## Scripts

### 1. enhance_foodb.py
Main processing script that:
- Reads food entries from the original Food.json
- Processes each food item through OpenAI's GPT API
- Adds translations and calorie information
- Saves enhanced data to `enhanced_foodb/list/Food.json`

Key Features:
- Batch processing (5 items per batch)
- Comprehensive error handling and logging
- API rate limiting (1 request/second)
- Progress tracking and resumable processing
- Validates API responses for required fields

### 2. convert_to_lines.py
Utility script that:
- Converts array format to line-by-line format
- Reads from `enhanced_foodb/list/Food.json`
- Saves to `enhanced_foodb/line/Food.json`
- Preserves all data fields and formatting

## Setup and Usage

1. **Prerequisites**
   ```bash
   pip install openai>=1.0.0
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

4. **Convert Format (Optional)**
   ```bash
   python convert_to_lines.py
   ```

## Output Format

Each enhanced food entry contains:

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
  - Calorie estimates are approximations based on nutritional databases

- **API Usage**:
  - Rate limited to 1 request per second
  - Approximately 1000 tokens per request
  - Each food item requires one API call
  - Progress is automatically saved between batches

## Contact

For questions about this enhanced dataset or the translation process, please contact:
- Yiliu (Aiden) Li (yiliu.li@outlook.com)

For questions about the original FooDB data, please contact the FooDB team through their website.

## License

This project enhances food data from FooDB (https://foodb.ca/). The original food data is subject to FooDB's terms and conditions. The enhanced translations and calorie data are provided for research and educational purposes only. For professional or commercial use, please verify data accuracy with official sources and comply with FooDB's licensing terms.
