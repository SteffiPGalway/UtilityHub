from PyPDF2 import PdfReader, PdfMerger

def merge_pdfs(pdf_list, output):
    """Merge multiple PDF files into a single PDF.
    Args:
        pdf_list (list): List of file-like objects representing PDFs
        output (str): Output file path for merged PDF
    Returns:
        None
    """
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output)
