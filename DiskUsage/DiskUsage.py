import os
import csv
from collections import defaultdict

def get_size(start_path="."):
    """Returns the total size of a directory or file in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):  # Skip symbolic links
                try:
                    total_size += os.path.getsize(fp)
                except (OSError, FileNotFoundError):
                    pass  # Handle deleted or inaccessible files
    return total_size

def scan_folders(base_path):
    """Scans all folders in the given base directory and calculates their sizes."""
    folder_sizes = {}
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            folder_sizes[folder] = get_size(folder_path)
    
    return folder_sizes

def write_to_csv(folder_sizes, output_file):
    """Writes folder size data to a CSV file with percentage calculations."""
    total_size = sum(folder_sizes.values())
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Folder Name", "Size (GB)", "Percentage of Total Disk Usage (%)"])
        
        for folder, size in sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True):
            percentage = (size / total_size) * 100 if total_size > 0 else 0
            writer.writerow([folder, round(size / (1024**3), 2), round(percentage, 2)])

def main():
    base_path = "C:\\"  # Change this to any directory you want to scan
    output_file = "disk_usage_report.csv"
    
    print(f"Scanning {base_path} for large folders...")
    folder_sizes = scan_folders(base_path)
    
    print("Writing results to CSV...")
    write_to_csv(folder_sizes, output_file)
    
    print(f"Report saved as {output_file}")

if __name__ == "__main__":
    main()

