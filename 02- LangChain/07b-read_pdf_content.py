import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader

def get_file_content():
    # 1. Initialize tkinter and hide the main window
    root = tk.Tk()
    root.withdraw()
    
    # 2. Open the file dialog
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not file_path:
        print("No file was selected.")
        return

    try:
        # 3. Load the PDF file
        reader = PdfReader(file_path)
        the_text = ""
        for i, page in enumerate(reader.pages):
                the_text += page.extract_text()
        return the_text
            
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    the_article_text = get_file_content()
    print(the_article_text)
    