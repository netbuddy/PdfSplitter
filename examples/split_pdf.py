from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_path, page_ranges):
    pdf_reader = PdfReader(input_path)
    pdf_writer = PdfWriter()
    
    for start, end in page_ranges:
        for page in range(start - 1, min(end, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

if __name__ == "__main__":
    input_path="/data/download/faq/faq.pdf"
    output_path="/data/download/faq/1.pdf"
    page_ranges=[(41,52)]
    split_pdf(input_path, output_path, page_ranges)