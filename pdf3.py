import fitz  # PyMuPDF
import argparse
import os
import re

def convert_pdf_to_markdown(pdf_path):
    """
    Convert a PDF file to Markdown format.
    """
    markdown = []
    
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, 1):
            # Extract text and its coordinates
            text = page.get_text("text")
            
            # Clean the text: remove special characters and extra spaces
            text = re.sub(r'\s+', ' ', text)
            text = text.replace("\n", " ")
            text = re.sub(r' +', ' ', text)
            text = re.sub(r'-', '', text)
            text = re.sub(r'[.!?]+', '. ', text).strip()
            
            # Add page number and cleaned text to markdown
            markdown.append(f"### Page {page_num}")
            markdown.append(text)
    
    return '\n'.join(markdown)

def chunk_legal_document(document_text, chunk_size=500, overlap=200):
    """
    Split a legal document into chunks with specified size and overlap.
    """
    # Split the text into paragraphs
    paragraphs = re.findall(r'[^.?!]+[.?!]*', document_text)
    
    # Process each paragraph to create chunks
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # Add paragraph to current chunk
        new_content = current_chunk + " " + para
        
        # Check if the new content exceeds the chunk size
        if len(new_content) > chunk_size:
            # Split into smaller parts
            words = new_content.split()
            
            # Create chunks with overlap
            for i in range(0, len(words), chunk_size):
                end = min(i + chunk_size, len(words))
                
                # Ensure there's overlap between chunks
                if end - i > overlap:
                    end = max(end - (overlap // 2) + 1, i)
                
                chunk = ' '.join(words[i:end])
                chunks.append(chunk)
            
            current_chunk = ""  # Reset for next paragraph
            
        else:
            current_chunk = new_content
    
    return chunks

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown with legal document post-processing.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input PDF file')
    parser.add_argument('-o', '--output', default='output.md', help='Name of the output Markdown file')
    
    args = parser.parse_args()
    
    # Convert PDF to Markdown
    markdown_text = convert_pdf_to_markdown(args.input)
    
    # Apply chunking and overlapping for legal documents
    chunks = chunk_legal_document(markdown_text)
    
    # Save the chunks to a file
    with open(args.output, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"### Chunk {i+1}\n\n{chunk}\n")
    
    print(f"Conversion completed. Output saved to '{args.output}'")

if __name__ == "__main__":
    main()