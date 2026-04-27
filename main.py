import argparse
import re
from collections import Counter

STOPWORDS = {
    "the","is","in","and","to","of","a","for","on",
    "with","as","by","an","are","this","that","it"
}


def load_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)


def keyword_frequency(text):
    words = re.findall(r'\\b[a-zA-Z]{4,}\\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return Counter(filtered).most_common(10)


def important_sentences(sentences):
    return [s for s in sentences if len(s.split()) > 8][:10]


def generate_revision_sheet(text):

    sentences = extract_sentences(text)
    keywords = keyword_frequency(text)
    highlights = important_sentences(sentences)

    report = []

    report.append("=== KEY SENTENCES ===\\n")
    report.extend(highlights)

    report.append("\\n=== TOP KEYWORDS ===\\n")
    for word, count in keywords:
        report.append(f"{word}: {count}")

    return "\\n".join(report)


def save_output(content):
    with open("revision_sheet.txt", "w") as f:
        f.write(content)


def main():

    parser = argparse.ArgumentParser(
        description="Generate revision summaries from study notes"
    )

    parser.add_argument(
        "file",
        help="input study notes (.txt)"
    )

    args = parser.parse_args()

    text = load_text(args.file)

    revision_sheet = generate_revision_sheet(text)

    save_output(revision_sheet)

    print("Revision sheet created: revision_sheet.txt")


if __name__ == "__main__":
    main()
