import fitz
import docx

def cv_extractor(file):
   '''
   This tool reads user CV whether it is in pdf or docx format and returns its content.

   Args:
    file: pdf | docx -> CV file

   Return:
     content: text content of CV file
   '''

   if file.type == "application/pdf":
        doc = fitz.open(stream=file, filetype="pdf") 
        text = "\n".join([page.get_text() for page in doc])
        return text
   elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
   else:
        raise ValueError(f"Unsupported file type: {file.type}")