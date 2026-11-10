"""
Task 1: Move all .jpg files from a folder to a new folder
Key Concepts: os, shutil, file handling

This script scans a source directory for JPEG images (.jpg, .jpeg, case-insensitive)
and automates moving them into a designated destination directory.
Handles duplicate filenames, folder creation, and generates sample files if needed.
"""

import os
import shutil
import sys
import argparse
from datetime import datetime


def create_sample_files(source_dir: str):
    """Creates sample dummy files in source_dir for demonstration/testing."""
    os.makedirs(source_dir, exist_ok=True)
    sample_files = [
        "nature.jpg",
        "portrait.jpeg",
        "VACATION.JPG",
        "document.pdf",
        "notes.txt",
        "logo.png",
        "sunset.jpg"
    ]
    print(f"\n[+] Generating sample files in '{source_dir}' for testing...")
    for filename in sample_files:
        filepath = os.path.join(source_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Sample dummy content for {filename} created at {datetime.now()}")
            print(f"    - Created: {filename}")
        else:
            print(f"    - Exists: {filename}")
    print("[+] Sample files generated successfully.\n")


def resolve_duplicate_filename(dest_dir: str, filename: str) -> str:
    """
    If a file with the same name already exists in destination,
    appends an incrementing counter: e.g. photo.jpg -> photo_1.jpg.
    """
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    return new_filename


def move_jpg_files(source_dir: str, dest_dir: str, auto_create_samples: bool = False) -> dict:
    """
    Moves all .jpg and .jpeg files from source_dir to dest_dir.

    Returns:
        dict: Summary of operations (scanned, moved, skipped).
    """
    # Validate source directory
    if not os.path.exists(source_dir):
        print(f"[!] Source folder '{source_dir}' does not exist.")
        if auto_create_samples:
            create_sample_files(source_dir)
        else:
            try:
                response = input("Would you like to create it with sample files? (y/n): ").strip().lower()
                if response == 'y':
                    create_sample_files(source_dir)
                else:
                    print("[!] Operation aborted.")
                    return {"scanned": 0, "moved": 0, "skipped": 0, "moved_files": []}
            except EOFError:
                create_sample_files(source_dir)

    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    summary = {
        "scanned": 0,
        "moved": 0,
        "skipped": 0,
        "moved_files": []
    }

    # Allowed extensions for JPG files
    valid_extensions = {".jpg", ".jpeg"}

    print("=" * 60)
    print("  IMAGE FILE ORGANIZER (JPG / JPEG)")
    print("=" * 60)
    print(f"Source Directory     : {os.path.abspath(source_dir)}")
    print(f"Destination Directory: {os.path.abspath(dest_dir)}")
    print("-" * 60)

    # Scan the source directory
    entries = os.listdir(source_dir)
    if not entries:
        print("[!] Source directory is empty. Nothing to move.")
        return summary

    for item in entries:
        source_path = os.path.join(source_dir, item)

        # Process only files (skip subfolders)
        if not os.path.isfile(source_path):
            continue

        summary["scanned"] += 1
        _, ext = os.path.splitext(item)

        # Check if extension matches .jpg or .jpeg (case-insensitive)
        if ext.lower() in valid_extensions:
            # Resolve potential duplicate in destination
            final_filename = resolve_duplicate_filename(dest_dir, item)
            dest_path = os.path.join(dest_dir, final_filename)

            try:
                shutil.move(source_path, dest_path)
                rename_notice = f" (renamed to {final_filename})" if final_filename != item else ""
                print(f"[MOVED]   {item} -> {dest_path}{rename_notice}")
                summary["moved"] += 1
                summary["moved_files"].append((item, final_filename))
            except Exception as e:
                print(f"[ERROR]   Failed to move '{item}': {e}")
        else:
            print(f"[SKIPPED] {item} (Non-JPG file)")
            summary["skipped"] += 1

    print("-" * 60)
    print("SUMMARY:")
    print(f"  Total Files Scanned : {summary['scanned']}")
    print(f"  JPG Files Moved     : {summary['moved']}")
    print(f"  Other Files Skipped : {summary['skipped']}")
    print("=" * 60)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Move all .jpg/.jpeg files from source to destination folder.")
    parser.add_argument("--source", "-s", type=str, default=None, help="Source directory containing images")
    parser.add_argument("--dest", "-d", type=str, default=None, help="Destination directory for JPG images")
    parser.add_argument("--create-samples", action="store_true", help="Automatically generate sample images for testing")
    args = parser.parse_args()

    default_source = "sample_images"
    default_dest = "jpg_archive"

    if args.source and args.dest:
        source = args.source
        dest = args.dest
    else:
        print("Task Automation - Option 1: Move .jpg Files")
        source = args.source or input(f"Enter source directory path [default: '{default_source}']: ").strip() or default_source
        dest = args.dest or input(f"Enter destination directory path [default: '{default_dest}']: ").strip() or default_dest

    move_jpg_files(source, dest, auto_create_samples=args.create_samples)


if __name__ == "__main__":
    main()
