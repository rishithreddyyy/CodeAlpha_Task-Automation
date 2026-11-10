"""
Task 2: Extract all email addresses from a .txt file and save them to another file
Key Concepts: re (Regular Expressions), file handling, os

This script reads arbitrary text content from a .txt file, extracts all valid email
addresses using regular expressions, eliminates duplicates, and saves the cleaned
email list to a designated output file.
"""

import os
import re
import sys
import argparse
from datetime import datetime


SAMPLE_TEXT_CONTENT = """
Hello Team,

Please find below the updated contact list for our project contributors:
- Project Manager: alice.smith@techcorp.com
- Lead Architect: bob_builder123@domain.org
- Support: support@customerservice.co.uk (Official helpdesk)
- General Inquiry: info@example.com

Secondary and external contacts:
- Charlie: charlie.dev+filters@gmail.com
- Duplicate entry test: alice.smith@techcorp.com
- Another duplicate: info@example.com
- Marketing: Sarah_O'Connor@media-agency.net -> will match valid characters: sarah_o@media-agency.net or sarah.oconnor@agency.io

Please ignore invalid formats such as:
- user@.com (missing domain name)
- @missinguser.com (missing username)
- plainaddress (not an email)
- user@domain (missing TLD)

For urgent escalation, reach out to emergency-contact@service247.io or admin@sub.network.org.

Best regards,
Admin
"""


def create_sample_text_file(filepath: str):
    """Creates a sample text file with various email formats for testing."""
    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(SAMPLE_TEXT_CONTENT.strip())
    print(f"[+] Sample file created at '{filepath}' with test content.\n")


def extract_emails_from_text(text: str) -> list[str]:
    """
    Extracts all valid email addresses from text using regular expressions.
    Returns a sorted list of unique, lowercase email addresses.
    """
    # Regex pattern matching standard email formats:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    raw_matches = re.findall(email_pattern, text)

    # Normalize to lowercase and remove trailing dots if any
    cleaned_emails = set()
    for email in raw_matches:
        cleaned = email.strip().strip(".").lower()
        if cleaned:
            cleaned_emails.add(cleaned)

    # Return sorted list for consistent, clean output
    return sorted(cleaned_emails)


def process_email_extraction(input_path: str, output_path: str, auto_create_samples: bool = False) -> dict:
    """
    Reads an input text file, extracts emails, and writes them to an output file.

    Returns:
        dict: Summary of extracted emails count.
    """
    print("=" * 60)
    print("  EMAIL ADDRESS EXTRACTOR")
    print("=" * 60)
    print(f"Input File : {os.path.abspath(input_path)}")
    print(f"Output File: {os.path.abspath(output_path)}")
    print("-" * 60)

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"[!] Input file '{input_path}' not found.")
        if auto_create_samples:
            create_sample_text_file(input_path)
        else:
            try:
                response = input("Would you like to generate a sample text file? (y/n): ").strip().lower()
                if response == 'y':
                    create_sample_text_file(input_path)
                else:
                    print("[!] Operation aborted.")
                    return {"total_found": 0, "unique_emails": []}
            except EOFError:
                create_sample_text_file(input_path)

    # Read input file
    try:
        with open(input_path, "r", encoding="utf-8", errors="replace") as infile:
            content = infile.read()
    except Exception as e:
        print(f"[ERROR] Failed to read input file: {e}")
        return {"total_found": 0, "unique_emails": []}

    # Extract unique emails
    emails = extract_emails_from_text(content)

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Write results to output file
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(f"# Extracted Email Addresses\n")
            outfile.write(f"# Source File: {os.path.basename(input_path)}\n")
            outfile.write(f"# Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"# Total Unique Emails: {len(emails)}\n")
            outfile.write("-" * 50 + "\n\n")

            for email in emails:
                outfile.write(f"{email}\n")

        print(f"[+] Successfully extracted {len(emails)} unique email addresses:\n")
        for idx, email in enumerate(emails, start=1):
            print(f"  {idx:2d}. {email}")

        print("\n" + "-" * 60)
        print(f"[SAVED] Results saved to '{os.path.abspath(output_path)}'")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}")

    return {
        "total_found": len(emails),
        "unique_emails": emails
    }


def main():
    parser = argparse.ArgumentParser(description="Extract all email addresses from a .txt file.")
    parser.add_argument("--input", "-i", type=str, default=None, help="Input text file path")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output file path for extracted emails")
    parser.add_argument("--create-samples", action="store_true", help="Automatically generate sample text file if missing")
    args = parser.parse_args()

    default_input = "sample_contacts.txt"
    default_output = "extracted_emails.txt"

    if args.input and args.output:
        input_file = args.input
        output_file = args.output
    else:
        print("Task Automation - Option 2: Extract Emails from Text File")
        input_file = args.input or input(f"Enter input .txt file path [default: '{default_input}']: ").strip() or default_input
        output_file = args.output or input(f"Enter output file path [default: '{default_output}']: ").strip() or default_output

    process_email_extraction(input_file, output_file, auto_create_samples=args.create_samples)


if __name__ == "__main__":
    main()
