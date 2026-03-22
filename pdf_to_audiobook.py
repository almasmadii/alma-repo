import sys
import argparse
import pyttsx3
from pypdf import PdfReader


# ──────────────────────────────────────────────
# STEP 1: Extract text from PDF
# ──────────────────────────────────────────────
def extract_text_from_pdf(pdf_path: str, start_page: int = 1, end_page: int = None) -> str:
    """
    Opens a PDF file and extracts all readable text.
    Returns a single string with the full content.
    """
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    print(f"[INFO] PDF loaded: '{pdf_path}' ({total_pages} pages)")

    # Default to all pages if no range is specified
    start = max(0, start_page - 1)  # Convert 1-based to 0-based index
    end = min(end_page or total_pages, total_pages)

    print(f"[INFO] Reading pages {start + 1} to {end} ...")

    extracted_text = ""
    for page_num in range(start, end):
        page = reader.pages[page_num]
        page_text = page.extract_text()
        if page_text:
            extracted_text += f"\n\n--- Page {page_num + 1} ---\n\n"
            extracted_text += page_text

    if not extracted_text.strip():
        print("[WARNING] No text could be extracted. The PDF may be scanned/image-based.")
        print("          Try an OCR tool like pytesseract for scanned documents.")
        sys.exit(1)

    print(f"[INFO] Extracted {len(extracted_text)} characters of text.")
    return extracted_text


# ──────────────────────────────────────────────
# STEP 2: Convert text to speech
# ──────────────────────────────────────────────
def speak_text(text: str, save_path: str = None, rate: int = 175, volume: float = 1.0):
    """
    Converts the given text to speech using pyttsx3.

    Args:
        text      : the text to read aloud
        save_path : if provided, saves audio to this file instead of playing it
        rate      : speaking speed in words per minute (default 175)
        volume    : volume from 0.0 (silent) to 1.0 (full, default)
    """
    engine = pyttsx3.init()

    # Configure the voice engine
    engine.setProperty('rate', rate)  # Speed of speech
    engine.setProperty('volume', volume)  # Volume level

    # Optional: list and pick a voice
    voices = engine.getProperty('voices')
    # Uncomment the next line to use a female voice if available:
    # engine.setProperty('voice', voices[1].id)

    if save_path:
        print(f"[INFO] Saving audio to '{save_path}' ...")
        engine.save_to_file(text, save_path)
        engine.runAndWait()
        print(f"[INFO] Done! Audio saved to '{save_path}'")
    else:
        print("[INFO] Speaking now... (press Ctrl+C to stop)")
        engine.say(text)
        engine.runAndWait()
        print("[INFO] Done!")


# ──────────────────────────────────────────────
# STEP 3: Parse arguments & run
# ──────────────────────────────────────────────
def parse_page_range(page_arg: str):
    """Parses a page range like '1-5' into (start, end) integers."""
    if '-' in page_arg:
        parts = page_arg.split('-')
        return int(parts[0]), int(parts[1])
    else:
        page = int(page_arg)
        return page, page


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to speech (a free audiobook maker)."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--pages", help="Page range to read, e.g. '1-10'", default=None)
    parser.add_argument("--save", help="Save audio to file instead of playing it", default=None)
    parser.add_argument("--rate", type=int, help="Speech rate in WPM (default: 175)", default=175)
    parser.add_argument("--volume", type=float, help="Volume 0.0–1.0 (default: 1.0)", default=1.0)
    args = parser.parse_args()

    # Parse page range
    start_page, end_page = 1, None
    if args.pages:
        start_page, end_page = parse_page_range(args.pages)

    # --- Run the pipeline ---
    text = extract_text_from_pdf(args.pdf_file, start_page, end_page)
    speak_text(text, save_path=args.save, rate=args.rate, volume=args.volume)


if __name__ == "__main__":
    text = extract_text_from_pdf("book.pdf")
    speak_text(text)
    main()