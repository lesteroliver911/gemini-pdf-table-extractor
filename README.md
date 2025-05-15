# 🔎 Google Gemini PDF to Table Extractor in HTML

**Transform PDF tables into perfect HTML with the power of Gemini 2.5**

This experimental tool leverages Google's Gemini 2.5 Flash Preview model to parse complex tables from PDF documents and convert them into clean HTML that preserves the exact layout, structure, and data.


https://github.com/user-attachments/assets/e5d66cd4-edcd-49ee-8dcb-3b8bf2b3113b


[![Watch the video](https://raw.githubusercontent.com/username/repository/branch/path/to/thumbnail.jpg)](https://raw.githubusercontent.com/username/repository/branch/path/to/video.mp4)

## ✨ Why This Matters

PDF tables are notoriously difficult to extract accurately. Standard conversion tools often produce:
- Misaligned columns and rows
- Lost formatting and merged cells
- Garbled text and numbers
- Completely broken layouts

This tool achieves ~80% layout accuracy while maintaining nearly 100% data accuracy for most tables.

## 🚀 Key Features

- **Preserves Complex Table Structures** - Handles merged cells, nested headers, and multi-line content
- **Maintains Visual Fidelity** - Recreates the visual appearance of tables with proper CSS
- **Extracts Text with High Accuracy** - Particularly effective with numerical data
- **Direct PDF Processing** - Sends PDF data directly to the model without intermediary conversions
- **Thinking Mode** - Uses Gemini's unique thinking capability for improved analysis
- **Token Usage Reporting** - Tracks processing efficiency

## 📊 Technical Approach

This project explores how AI models understand and parse structured PDF content. Rather than using OCR or traditional table extraction libraries, this tool gives the raw PDF to Gemini and uses specialized prompting techniques to optimize the extraction process.

## 📝 Installation

1. Clone this repository:
```bash
git clone https://github.com/lesteroliver911/gemini-pdf-table-extractor
cd gemini-pdf-table-extractor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google API key:
   - Create a `.env` file in the project root directory
   - Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`

## 💻 Usage

Basic usage:
```bash
python main.py path/to/your/document.pdf
```

This will generate an HTML file with the same name in the same directory.

Advanced options:
```bash
python main.py path/to/your/document.pdf --output custom_output.html --thinking-budget 24000
```

Arguments:
- `--output`: Specify a custom output file path
- `--thinking`: Enable thinking mode (default: True)
- `--thinking-budget`: Set the thinking token budget (default: 24000)
- `--prompt`: Provide a custom prompt for conversion

## 🧪 Experimental Status

This project is an exploration of AI-powered PDF parsing capabilities. While it achieves strong results for many tables, complex documents with unusual layouts may present challenges. The extraction accuracy will improve as the underlying models advance. 
