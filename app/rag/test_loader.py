from document_loader import load_pdf


pdf_path = "D:\\Learning_Projects\\AI Knowledge Assistant\\documents\\leave_policy_sample.pdf"

pages = load_pdf(pdf_path)

for page in pages:

    print(f"\n--- Page {page['page']} ---")

    print(page["text"])