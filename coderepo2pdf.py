import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    project_name = "CodeRepo2PDF"
    ignored_extensions = {".pdf", ".txt"}

    # Define supported project types
    project_types = {
        1: "python",
        2: "nodejs",
        3: "django",
        4: "flask",
        5: "nextjs"
    }

    # Prompt user to select project type
    print("Select your project type:")
    for key, value in project_types.items():
        if value == "nextjs":
            print(f"{Fore.YELLOW}{key}. {value}{Style.RESET_ALL}")
        elif value == "nodejs":
            print(f"{Fore.GREEN}{key}. {value}{Style.RESET_ALL}")
        else:
            print(f"{key}. {value}")

    project_type = int(input("Enter the number corresponding to your project type: "))
    if project_type not in project_types:
        print("Invalid selection. Exiting.")
        sys.exit(1)

    # Load allow and ignore lists for the selected project type
    allow_list, ignore_list = load_lists(project_types[project_type])

    # Set up output folder
    cwd = os.getcwd()
    output_folder = os.path.join(cwd, project_name)
    os.makedirs(output_folder, exist_ok=True)

    # Count total files to process
    total_files = count_files(cwd, allow_list, ignore_list)
    processed_files = 0

    # Process directory and generate text output
    print("Processing directory...")
    text_str, _ = process_directory(cwd, ignored_extensions, allow_list, ignore_list, processed_files, total_files)

    # Write text output to file
    text_output_path = os.path.join(output_folder, "index.txt")
    with open(text_output_path, "w", encoding="utf-8") as text_file:
        text_file.write(text_str)
    print("TXT file written.")

    # Generate PDF from text output
    pdf_output_path = os.path.join(output_folder, "index.pdf")
    generate_pdf_from_text(text_output_path, pdf_output_path)

    print("Conversion completed. Check the output folder.")

def generate_pdf_from_text(text_output_path, pdf_output_path):
    # Read text file
    with open(text_output_path, "r", encoding="utf-8") as text_file:
        lines = text_file.readlines()

    # Set up PDF canvas
    pdf = canvas.Canvas(pdf_output_path, pagesize=letter)

    def set_font():
        pdf.setFont("Courier", 10)

    set_font()
    text_object = pdf.beginText(50, 750)

    # Add lines to PDF
    for line in lines:
        text_object.textLine(line.rstrip())
        if text_object.getY() < 50:  # Add a new page when reaching the bottom
            pdf.drawText(text_object)
            pdf.showPage()
            set_font()
            text_object = pdf.beginText(50, 750)

    # Save PDF
    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()
    
# Load allow and ignore lists for different project types
def load_lists(project_type):
    # Define allow and ignore lists for each project type
    if project_type.lower() == 'python':
        allow_list = {".py"}
        ignore_list = {"__pycache__", ".git", "*.pyc", "*.pyo", "*.egg-info", "*.dist-info"}
    elif project_type.lower() == 'nextjs':
        allow_list = {".js", ".jsx", ".ts", ".tsx", ".json", ".css", ".scss"}
        ignore_list = {".next", ".git", "node_modules", "package-lock.json"}
    elif project_type.lower() == 'nodejs':
        allow_list = {".js", ".ts", ".json", ".css", ".scss"}
        ignore_list = {".git", "node_modules", "package-lock.json", "yarn.lock"}
    elif project_type.lower() == 'django':
        allow_list = {".py", ".html", ".css", ".js", ".json"}
        ignore_list = {"__pycache__", ".git", "*.pyc", "*.pyo", "*.egg-info", "*.dist-info", "db.sqlite3", "migrations", "static", "media"}
    elif project_type.lower() == 'flask':
        allow_list = {".py", ".html", ".css", ".js", ".json"}
        ignore_list = {"__pycache__", ".git", "*.pyc", "*.pyo", "*.egg-info", "*.dist-info", "instance", "static", "templates"}
    else:
        print("Unsupported project type. Exiting.")
        sys.exit(1)

    return allow_list, ignore_list

# Print progress bar and percentage for processed files
def print_progress(processed_files, total_files, item_path):
    progress = (processed_files / total_files) * 100
    bar_length = 30
    filled_length = int(bar_length * processed_files // total_files)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {progress:.1f}% ({processed_files}/{total_files}) Processing: {item_path[:50]}', end='', flush=True)

# Count the total number of files in the input directory, considering the allow and ignore lists
def count_files(input_dir, allow_list, ignore_list):
    total_files = 0
    for item in os.listdir(input_dir):
        if item in ignore_list:
            continue

        item_path = os.path.join(input_dir, item)

        if os.path.isdir(item_path):
            total_files += count_files(item_path, allow_list, ignore_list)
        elif os.path.isfile(item_path) and (os.path.splitext(item)[1] in allow_list):
            total_files += 1

    return total_files

# Process the input directory recursively, generating a markdown-formatted string with code snippets
def process_directory(input_dir, ignored_extensions, allow_list, ignore_list, processed_files, total_files, depth=0, root_dir=None):
    if root_dir is None:
        root_dir = input_dir

    text_str = f"{'#' * (depth + 1)} {os.path.basename(input_dir)}\n\n"

    for item in os.listdir(input_dir):
        if item in ignore_list:
            continue

        item_path = os.path.join(input_dir, item)

        if os.path.isdir(item_path):
            subdir_text, processed_files = process_directory(item_path, ignored_extensions, allow_list, ignore_list, processed_files, total_files, depth + 1, root_dir)
            text_str += subdir_text

        elif os.path.isfile(item_path) and (os.path.splitext(item)[1] in allow_list):
            processed_files += 1
            print_progress(processed_files, total_files, item_path)
            file_text = process_file(item_path)
            relative_path = os.path.relpath(item_path, root_dir).replace('\\', '/')
            text_str += f"{'#' * (depth + 3)} {relative_path}\n{file_text}\n\n"

    return text_str, processed_files

# Read the content of a file and return it as a markdown-formatted code block
def process_file(file_path):
    text_code = ""

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        text_code = f"```\n{code}\n```"

    return text_code

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
