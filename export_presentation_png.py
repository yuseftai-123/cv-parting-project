import os
import win32com.client

pptx_path = os.path.abspath(r"C:\Users\pc\Desktop\cv-parting-project\cv_parser_engine_presentation.pptx")
output_dir = os.path.abspath(r"C:\Users\pc\Desktop\cv-parting-project\slide_images")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

ppt = win32com.client.Dispatch("PowerPoint.Application")
# ppt.Visible = True # Keep hidden if possible or visible

try:
    pres = ppt.Presentations.Open(pptx_path, WithWindow=False)
    for idx, slide in enumerate(pres.Slides):
        img_path = os.path.join(output_dir, f"slide_{idx+1}.png")
        slide.Export(img_path, "PNG", 1920, 1080)
        print(f"Exported slide {idx+1} to {img_path}")
    pres.Close()
finally:
    ppt.Quit()

print("All slides exported to PNG successfully!")
