"""
Manual CV Testing Helper Script
Run: venv\\Scripts\\python.exe test_my_cv.py <path_to_cv.pdf_or_docx>
"""
import sys
import json
from app.services.pipeline import process_cv_pipeline

def test_cv(file_path: str):
    print(f"\n==================================================")
    print(f" TESTING CV MANUALLY: {file_path}")
    print(f"==================================================\n")
    
    filename = file_path.replace("\\", "/").split("/")[-1]
    result = process_cv_pipeline(file_path, filename)
    
    # Convert Pydantic object to dictionary
    result_dict = result.model_dump()
    print(json.dumps(result_dict, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: venv\\Scripts\\python.exe test_my_cv.py <path_to_cv_file>")
        print("Example: venv\\Scripts\\python.exe test_my_cv.py cv_set\\cv_1.pdf")
        sys.exit(1)
    
    path = sys.argv[1]
    test_cv(path)
