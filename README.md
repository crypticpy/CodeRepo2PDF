# README

## CodeRepo2PDF

CodeRepo2PDF is a Python script that converts a code repository into a PDF file. It supports various project types, including Python, Node.js, Next.js, Django, and Flask. The script generates a PDF file with a hierarchical structure based on the directory and file structure, making it easier to navigate through the code.

### How to use

1. Install the required dependencies:

```bash
pip install reportlab colorama
```

2. Run the script in the root directory of your project:

```bash
python code_repo_2_pdf.py
```

3. Follow the prompts to select your project type. 

4. The script will generate a PDF and text document in the 'CodeRepo2PDF' folder within your project directory.

## Preparing for vector storage

Once you have generated the PDF file, you can use it to load your code repository into a vector storage system. This process typically involves converting the PDF file into a format that can be easily parsed and indexed by the storage system. The hierarchical structure in the generated PDF file will help AI navigate and organize your code repository more efficiently when working in conversational applications.

## Contributing

Contributions to CodeRepo2PDF are welcome! Please submit a pull request or create an issue to discuss proposed changes or report bugs.

## License

CodeRepo2PDF is released under the MIT License. See the `LICENSE` file for details.

