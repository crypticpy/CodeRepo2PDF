import os
import sys
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from colorama import Fore, Style, init

init(autoreset=True)

def main():

    args = parse_arguments()

    input_dir = args.input_dir or os.getcwd()
    project_type = args.project_type
    output_file = args.output
    custom_allow_list_file = args.allow_list
    custom_ignore_list_file = args.ignore_list

    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory.")
        sys.exit(1)

    project_name = "CodeRepo2PDF"
    ignored_extensions = {".pdf", ".txt"}

    if project_type is None:
        project_type = prompt_project_type()

    if custom_allow_list_file or custom_ignore_list_file:
        allow_list, ignore_list = load_custom_lists(custom_allow_list_file, custom_ignore_list_file)
    else:
        allow_list, ignore_list = load_lists(project_type)

    output_folder = setup_output_folder(project_name)

    total_files = count_files(input_dir, allow_list, ignore_list)
    processed_files = 0

    print("Processing directory...")
    text_str, _ = process_directory(input_dir, ignored_extensions, allow_list, ignore_list, processed_files, total_files)

    text_output_path = os.path.join(output_folder, "index.txt")
    write_text_output(text_output_path, text_str)

    pdf_output_path = os.path.join(output_folder, "index.pdf")
    generate_pdf_from_text(text_output_path, pdf_output_path)
    print("Conversion completed. Check the output folder.")

def parse_arguments():

    parser = argparse.ArgumentParser(description="Generate documentation for a project in markdown format.")
    parser.add_argument("--input-dir", help="Path to the input directory containing the project files.", default=None)
    parser.add_argument("--project-type", help="Type of the project (e.g., python, nextjs, nodejs, django, flask).", default=None)
    parser.add_argument("-o", "--output", help="Path to the output markdown file.", default="output.md")
    parser.add_argument("--allow-list", help="Path to a custom allow list file.", default=None)
    parser.add_argument("--ignore-list", help="Path to a custom ignore list file.", default=None)
    return parser.parse_args()

def prompt_project_type():

    print("Select your project type:")
    project_types = {
        1: "python",
        2: "nodejs",
        3: "django",
        4: "flask",
        5: "nextjs"
    }

    for key, value in project_types.items():
        if value == "nextjs":
            print(f"{Fore.YELLOW}{key}. {value}{Style.RESET_ALL}")
        elif value == "nodejs":
            print(f"{Fore.GREEN}{key}. {value}{Style.RESET_ALL}")
        else:
            print(f"{key}. {value}")

    try:
        project_type = int(input("Enter the number corresponding to your project type: "))
        if project_type not in project_types:
            raise ValueError("Invalid selection.")
    except ValueError as e:
        print(f"{e} Exiting.")
        sys.exit(1)

    return project_types[project_type]

def load_custom_lists(allow_list_file, ignore_list_file):
    allow_list = set()
    ignore_list = set()

    if allow_list_file:
        with open(allow_list_file, "r") as f:
            for line in f:
                allow_list.add(line.strip())

    if ignore_list_file:
        with open(ignore_list_file, "r") as f:
            for line in f:
                ignore_list.add(line.strip())

    return allow_list, ignore_list

def setup_output_folder(project_name):

    cwd = os.getcwd()
    output_folder = os.path.join(cwd, project_name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def write_text_output(text_output_path, text_str):
    try:
        with open(text_output_path, "w", encoding="utf-8") as text_file:
            text_file.write(text_str)
        print("TXT file written.")
    except Exception as e:
        print(f"Error writing TXT file: {e}")
        sys.exit(1)

def generate_pdf_from_text(text_output_path, pdf_output_path):

    with open(text_output_path, "r", encoding="utf-8") as text_file:
        lines = text_file.readlines()

    pdf = canvas.Canvas(pdf_output_path, pagesize=letter)

    def set_font():
        pdf.setFont("Courier", 10)

    set_font()
    text_object = pdf.beginText(50, 750)

    for line in lines:
        text_object.textLine(line.rstrip())
        if text_object.getY() < 50:  
            pdf.drawText(text_object)
            pdf.showPage()
            set_font()
            text_object = pdf.beginText(50, 750)

    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()

def load_lists(project_type):
    
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

def print_progress(processed_files, total_files, item_path):
    
    progress = (processed_files / total_files) * 100
    bar_length = 30
    filled_length = int(bar_length * processed_files // total_files)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {progress:.1f}% ({processed_files}/{total_files}) Processing: {item_path[:50]}', end='', flush=True)

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

def process_file(file_path):

    text_code = ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            text_code = f"```\n{code}\n```"
    except UnicodeDecodeError:
        print(f"\nError processing file {file_path}: UnicodeDecodeError. Trying with 'ISO-8859-1' encoding.")
        try:
            with open(file_path, "r", encoding="ISO-8859-1") as f:
                code = f.read()
                text_code = f"```\n{code}\n```"
        except Exception as e:
            print(f"\nError processing file {file_path}: {e}")
    except Exception as e:
        print(f"\nError processing file {file_path}: {e}")

    return text_code

if __name__ == "__main__":
    main()
