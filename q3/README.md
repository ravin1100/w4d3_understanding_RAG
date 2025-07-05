# RAG Chunking Strategy Visualizer

A Streamlit web application that helps users understand different text chunking strategies used in Retrieval-Augmented Generation (RAG) pipelines. This tool allows users to upload PDF documents, extract text, and visualize how different chunking strategies would split the text.

## Features

- **PDF Document Upload & Processing**
  - Upload any PDF document
  - Extract text with metadata
  - Preview document content

- **Multiple Chunking Strategies**
  - Fixed-size chunking
  - Sliding window with configurable stride
  - Sentence-based chunking
  - Recursive chunking based on document structure

- **Interactive Visualization**
  - Strategy explanation and comparison
  - Configurable parameters for each strategy
  - Detailed chunk metadata
  - Expandable chunk previews

- **Export Options**
  - Download chunks as JSON
  - Download chunks as CSV
  - Complete chunk metadata included

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rag-chunking-visualizer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Upload a PDF document using the file uploader

4. Select a chunking strategy and configure its parameters

5. Click "Process Text" to see the results

6. Explore the chunks and download the results if desired

## Chunking Strategies

### Fixed Size
- Splits text into chunks of equal size
- Configurable chunk size and overlap
- Best for uniform content distribution

### Sliding Window
- Creates overlapping chunks with fixed stride
- Maintains context across chunk boundaries
- Ideal for tasks requiring context preservation

### Sentence Based
- Respects sentence boundaries
- Configurable number of sentences per chunk
- Perfect for maintaining semantic coherence

### Recursive
- Splits based on document structure
- Adapts to content patterns
- Great for well-structured documents

## Project Structure

```
├── app.py                 # Main Streamlit app
├── chunking/             # Chunking strategy implementations
│   ├── __init__.py
│   ├── base.py          # Base class for chunkers
│   ├── fixed_size.py    # Fixed-size chunking
│   ├── sliding_window.py # Sliding window chunking
│   ├── sentence_based.py # Sentence-based chunking
│   └── recursive_split.py # Recursive chunking
├── utils/               # Utility functions
│   ├── pdf_utils.py    # PDF processing utilities
│   └── visualization.py # Visualization helpers
└── sample_docs/        # Sample documents for testing
    └── example.pdf
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 