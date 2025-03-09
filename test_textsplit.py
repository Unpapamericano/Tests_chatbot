import os
import unittest
from langchain.schema import Document
from chatbot_rag.textsplit import load_documents, split_documents, load_documents_from_folder

class TestTextSplit(unittest.TestCase):
    def setUp(self):
        # Path to the test PDF file
        self.pdf_path = "test.pdf"
        # Create the test PDF file
        self.create_test_pdf(self.pdf_path)

    def tearDown(self):
        # Remove the test PDF file if it exists
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

    def create_test_pdf(self, path):
        # Helper method to create a test PDF file
        with open(path, "w") as f:
            f.write("Test PDF content")

    def test_load_documents(self):
        # Test loading documents from a PDF file
        documents = load_documents(self.pdf_path)
        self.assertGreater(len(documents), 0)

    def test_split_documents(self):
        # Test splitting a document into chunks
        documents = [Document(page_content="This is a test document.")]
        chunks = split_documents(documents)
        self.assertGreater(len(chunks), 0)

    def test_load_documents_from_folder(self):
        # Test loading documents from a folder
        folder_path = "test_folder"
        os.makedirs(folder_path, exist_ok=True)
        pdf_path = os.path.join(folder_path, "test.pdf")
        self.create_test_pdf(pdf_path)
        
        try:
            documents = load_documents_from_folder(folder_path)
            self.assertGreater(len(documents), 0)
        finally:
            # Clean up the created files and folder
            os.remove(pdf_path)
            os.rmdir(folder_path)

    def test_split_large_document(self):
        # Test splitting a large document into chunks
        large_content = "This is a large test document. " * 1000
        documents = [Document(page_content=large_content)]
        chunks = split_documents(documents)
        self.assertGreater(len(chunks), 1)

    def test_load_multiple_documents(self):
        # Test loading multiple documents from a folder
        folder_path = "test_folder"
        os.makedirs(folder_path, exist_ok=True)
        pdf_path1 = os.path.join(folder_path, "test1.pdf")
        pdf_path2 = os.path.join(folder_path, "test2.pdf")
        self.create_test_pdf(pdf_path1)
        self.create_test_pdf(pdf_path2)
        
        try:
            documents = load_documents_from_folder(folder_path)
            self.assertGreater(len(documents), 1)
        finally:
            # Clean up the created files and folder
            os.remove(pdf_path1)
            os.remove(pdf_path2)
            os.rmdir(folder_path)

if __name__ == "__main__":
    unittest.main()
