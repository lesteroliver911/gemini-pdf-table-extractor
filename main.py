#!/usr/bin/env python3
"""
🔎 PDF Table Extractor

Transform PDF tables into perfect HTML with the power of Gemini 2.5

This experimental tool extracts complex tables from PDFs and converts them
into clean HTML that preserves the exact layout, structure, and data.

Features:
- Handles merged cells, nested headers, and multi-line content
- Maintains visual fidelity with appropriate CSS
- Accurately extracts numerical data and text
- Uses Gemini's unique thinking capability for improved analysis
"""

import os
import argparse
import re
import base64
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Configure the Gemini API with your key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your environment variables or .env file")

# Initialize the Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

def clean_html_output(text):
    """
    Clean the output from Gemini to remove markdown code block markers.
    
    Args:
        text: The raw text from Gemini response
        
    Returns:
        Cleaned HTML without markdown code block markers
    """
    # Remove markdown code block markers (```html and ```)
    text = re.sub(r'^```html\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    # Also handle other possible variations
    text = re.sub(r'<html>\s*```html', '<html>', text, flags=re.IGNORECASE)
    text = re.sub(r'```\s*</html>', '</html>', text, flags=re.IGNORECASE)
    
    return text

def process_pdf_with_gemini(pdf_path, output_path=None, prompt=None, enable_thinking=True, thinking_budget=8000):
    """
    Process a PDF file with the Gemini model and convert it to HTML.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path to save the HTML output (optional)
        prompt: Optional prompt to provide additional instructions
        enable_thinking: Whether to enable Gemini's thinking capability
        thinking_budget: How much of the generation budget to allocate to thinking (tokens)
        
    Returns:
        The model's response containing HTML
    """
    # Validate file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Get file extension
    file_extension = Path(pdf_path).suffix.lower()
    if file_extension != ".pdf":
        raise ValueError(f"Expected a PDF file, got {file_extension}")
    
    # Read the PDF file as binary data
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    # Encode the PDF data as base64 (for storage/transfer if needed)
    encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")
    
    # Advanced prompt engineering for accurate table extraction 
    if prompt is None:
        prompt = """
        Convert this PDF to valid HTML code that preserves the exact layout of the original document.
        
        PAY SPECIAL ATTENTION TO TABLES:
        1. Preserve the exact table structure, including all rows and columns
        2. Use <table>, <tr>, <th>, and <td> elements properly
        3. Maintain all cell merges with rowspan and colspan attributes
        4. Keep header cells as <th> elements
        5. Preserve exact cell alignments (left, center, right) through CSS
        6. Maintain all cell borders and formatting
        7. Keep the exact text content of each cell with proper spacing
        
        ALSO IMPORTANT:
        - Text formatting: preserve fonts, sizes, and styles
        - Layout: maintain the exact spatial arrangement of elements
        - Images: include them in the HTML
        - Headers and footers: preserve document structure
        - CSS: use appropriate styling to match the original document appearance
        
        Analyze the document structure thoroughly before generating HTML.
        
        IMPORTANT: Return ONLY the raw HTML code WITHOUT any markdown formatting or code block markers (no ```html or ``` tags).
        The HTML should render in a browser to look identical to the PDF.
        """
    
    # Create content structure with the file and prompt
    contents = [
        types.Content(
            role="user",
            parts=[
                # Send the raw PDF data directly to Gemini
                types.Part.from_bytes(
                    mime_type="application/pdf", 
                    data=pdf_data
                ),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    # Configure generation parameters optimized for table extraction
    generate_content_config = types.GenerateContentConfig(
        temperature=0,       # Use 0 temperature for most deterministic output
        top_p=0.1,           # Lower top_p for more focused and precise results
        top_k=5,             # Lower top_k to limit token selection to the most likely options
        max_output_tokens=20000,  # Ensure enough tokens for complete HTML output
    )
    
    # Add explicit thinking configuration if enabled
    # This allocates tokens for the model's internal reasoning process
    if enable_thinking:
        generate_content_config.thinking_config = types.ThinkingConfig(
            thinking_budget=thinking_budget,
        )
    
    # Generate content with the file and prompt using Gemini 2.5 Flash
    model = "gemini-2.5-flash-preview-04-17"
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    # Clean the HTML output to remove any markdown code block markers
    cleaned_html = clean_html_output(response.text)
    
    # Save HTML to file if output path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_html)
        print(f"HTML output saved to: {output_path}")
    
    # Return cleaned response with access to original metadata
    class CleanedResponse:
        def __init__(self, original_response, cleaned_text):
            self._original = original_response
            self.text = cleaned_text
            
        def __getattr__(self, attr):
            return getattr(self._original, attr)
    
    return CleanedResponse(response, cleaned_html)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to HTML using Google's Gemini model")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument("--output", help="Path to save the HTML output", default=None)
    parser.add_argument("--prompt", help="Custom prompt for the conversion", default=None)
    parser.add_argument("--thinking", help="Enable thinking mode for better analysis", action="store_true", default=True)
    parser.add_argument("--thinking-budget", 
                      help="Tokens allocated for model's reasoning (higher values for complex tables)", 
                      type=int, 
                      default=24000)
    parser.add_argument("--stream", help="Stream the response", action="store_true", default=False)
    args = parser.parse_args()
    
    # If no output path specified, create one based on input filename
    if not args.output:
        output_path = Path(args.pdf_path).with_suffix('.html')
    else:
        output_path = args.output
    
    try:
        # Process the PDF and get the HTML response
        response = process_pdf_with_gemini(
            args.pdf_path, 
            output_path, 
            args.prompt, 
            enable_thinking=args.thinking, 
            thinking_budget=args.thinking_budget
        )
        print("\n=== CONVERSION COMPLETE ===\n")
        print(f"HTML saved to: {output_path}")
        
        # Display token usage statistics
        if args.thinking:
            try:
                print(f"Thinking tokens used: {response._original.usage_metadata.thoughts_token_count}")
                print(f"Total tokens used: {response._original.usage_metadata.total_token_count}")
            except AttributeError:
                print("Token usage information not available")
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    main() 
