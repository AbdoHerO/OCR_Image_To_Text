import ocrmypdf

if __name__ == '__main__':  # To ensure correct behavior on Windows and macOS
    ocrmypdf.ocr('../data/new_bl.pdf', '../output_results/output_ocrmypdf.pdf', deskew=True)