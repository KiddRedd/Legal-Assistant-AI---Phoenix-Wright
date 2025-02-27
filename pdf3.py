import sys
import os
import glob
import pdfplumber  # Make sure this library is installed
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_pdf_to_markdown(input_pdf):
    """Converts a PDF file to Markdown text."""
    try:
        with pdfplumber.open(input_pdf) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        logging.error(f"PDF conversion error: {e}")
        return None

def save_to_file(markdown, output_path):
    """Saves Markdown text to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if markdown:
                f.write(markdown)
        logging.info(f"Saved to: {output_path}")
    except IOError as e:
        logging.error(f"Error saving file '{output_path}': {e}")

def process_pdfs(pdf_file_paths):
    """Processes PDF files and yields results for each."""
    all_pdfs = []

    # Collect all PDF files from specified paths
    for path in pdf_file_paths:
        if os.path.isfile(path) and path.lower().endswith('.pdf'):
            all_pdfs.append(path)
        elif os.path.isdir(path):
            all_pdfs.extend(glob.glob(os.path.join(path, '*.pdf')))
        else:
            logging.warning(f"Invalid path: {path}. Skipping.")

    total_files = len(all_pdfs)
    processed_count = 0

    if not all_pdfs:
        logging.info("No PDF files found to process.")
        return

    for pdf_path in all_pdfs:
        try:
            processed_count += 1
            base_name = os.path.basename(pdf_path)
            dir_name = os.path.dirname(pdf_path)
            output_dir = os.path.join(dir_name, "converted")
            os.makedirs(output_dir, exist_ok=True)
            output_name = os.path.splitext(base_name)[0] + ".md"
            output_path = os.path.join(output_dir, output_name)

            converted_text = convert_pdf_to_markdown(pdf_path)
            if converted_text:
                save_to_file(converted_text, output_path)
                yield f"Successfully processed: {base_name}"
            else:
                logging.error(f"Failed to process: {base_name}")
                yield f"Failed to process: {base_name}"

        except Exception as e:
            logging.exception(f"Exception during processing of file {pdf_path}: {e}")

    logging.info(f"\nProcessed {processed_count} files.")

def main():
    """Main function to convert PDF files in given paths to Markdown."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_markdown.py input1.pdf [input2.pdf] ...")
        return

    # Process each PDF and yield results
    for result in process_pdfs(sys.argv[1:]):
        print(result)

if __name__ == "__main__":
    main()
