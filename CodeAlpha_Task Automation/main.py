"""
Task Automation Suite - Master Controller
CodeAlpha Task Automation with Python Scripts

Key Concepts Used:
- os (directory and path management)
- shutil (file operations and moving)
- re (regular expressions for email extraction and HTML parsing)
- requests (HTTP networking and web scraping)
- file handling (reading and writing text/binary files)
"""

import os
import sys
import argparse
from task1_move_jpg import move_jpg_files, create_sample_files
from task2_extract_emails import process_email_extraction, create_sample_text_file
from task3_scrape_title import scrape_and_save_title, DEFAULT_URL


def banner():
    print("""
======================================================================
           CODEALPHA - PYTHON TASK AUTOMATION SUITE
======================================================================
  Select an automation task to run:
  [1] Move all .jpg files to a new folder       (os, shutil)
  [2] Extract email addresses from a .txt file  (re, file handling)
  [3] Scrape title of a fixed webpage           (requests, re)
  [4] Run complete demo for all 3 tasks
  [5] Exit
======================================================================
""")


def run_task1():
    print("\n--- Running Task 1: Move .jpg Files ---")
    source = input("Source folder [default: 'sample_images']: ").strip() or "sample_images"
    dest = input("Destination folder [default: 'jpg_archive']: ").strip() or "jpg_archive"
    move_jpg_files(source, dest)


def run_task2():
    print("\n--- Running Task 2: Extract Emails ---")
    input_file = input("Input text file [default: 'sample_contacts.txt']: ").strip() or "sample_contacts.txt"
    output_file = input("Output file [default: 'extracted_emails.txt']: ").strip() or "extracted_emails.txt"
    process_email_extraction(input_file, output_file)


def run_task3():
    print("\n--- Running Task 3: Scrape Webpage Title ---")
    url = input(f"Target URL [default: '{DEFAULT_URL}']: ").strip() or DEFAULT_URL
    output_file = input("Output file [default: 'scraped_title.txt']: ").strip() or "scraped_title.txt"
    scrape_and_save_title(url, output_file)


def run_full_demo():
    print("\n" + "#" * 65)
    print("        EXECUTING AUTOMATED DEMO FOR ALL 3 AUTOMATIONS")
    print("#" * 65)

    # Demo 1
    demo_source = os.path.join("demo_data", "raw_photos")
    demo_dest = os.path.join("demo_data", "organized_jpgs")
    create_sample_files(demo_source)
    move_jpg_files(demo_source, demo_dest)

    print("\nPress Enter to continue to Task 2 demo...")
    # non-blocking or simple print for automated demo
    print("\n" + "-" * 65)

    # Demo 2
    demo_input_file = os.path.join("demo_data", "company_directory.txt")
    demo_output_file = os.path.join("demo_data", "unique_emails_output.txt")
    create_sample_text_file(demo_input_file)
    process_email_extraction(demo_input_file, demo_output_file)

    print("\n" + "-" * 65)

    # Demo 3
    demo_title_output = os.path.join("demo_data", "page_title_output.txt")
    scrape_and_save_title(DEFAULT_URL, demo_title_output)

    print("\n" + "#" * 65)
    print("             DEMO COMPLETED SUCCESSFULLY!")
    print(f"All demo outputs generated in: '{os.path.abspath('demo_data')}'")
    print("#" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Python Task Automation Suite")
    parser.add_argument("--task", type=int, choices=[1, 2, 3, 4], help="Task number to run directly (1, 2, 3, or 4 for demo)")
    args = parser.parse_args()

    if args.task:
        if args.task == 1:
            run_task1()
        elif args.task == 2:
            run_task2()
        elif args.task == 3:
            run_task3()
        elif args.task == 4:
            run_full_demo()
        return

    while True:
        banner()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            run_task1()
        elif choice == "2":
            run_task2()
        elif choice == "3":
            run_task3()
        elif choice == "4":
            run_full_demo()
        elif choice == "5":
            print("\nExiting Task Automation Suite. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
