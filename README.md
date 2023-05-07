# CodeRepo2PDF

CodeRepo2PDF is a Python-based tool that converts source code repositories into HTML, PDF, and a single text file format. It is particularly useful for developers who want to analyze and discuss their projects using natural language processing tools like OpenAI's GPT-4.

## Features

- Convert source code files in various formats into HTML and PDF
- Generate a single text file containing the entire project, with file names presented before the code
- Robust error handling and logging for failed and successful file conversions
- Progress indicator to track total, successful, and failed conversions
- Generate an ASCII map of the project structure

## Requirements

- Python 3.6 or later
- Pygments library: `pip install pygments`
- WeasyPrint library: `pip install WeasyPrint`

## Usage

1. Clone the repository and navigate to the project directory.
2. Make sure the required libraries are installed.
3. Run the script using `python code_repo_2_pdf.py`.
4. When prompted, enter the output folder name. The output folder will be created at the root of the project.
5. Monitor the progress as the script processes each file.
6. Once the script has finished, you will find the generated HTML, PDF, single text file, project structure, and logs in the output folder.

## Customization

To tailor CodeRepo2PDF to your specific project, you may need to modify the following variables in the script:

- `supported_extensions`: Add or remove file extensions to process.
- `ignored_files`: Add or remove specific files you want to ignore during the conversion process.

Additionally, you can adjust the HTML formatting options within the `HtmlFormatter` to improve the readability of the generated PDFs.

## Contributing

Contributions to CodeRepo2PDF are welcome! Please submit a pull request or create an issue to discuss proposed changes or report bugs.

## License

CodeRepo2PDF is released under the MIT License. See the `LICENSE` file for details.

