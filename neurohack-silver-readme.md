# L&T NEUROHACK - Silver Problem Statement Solution

## Offline Text Summarization Tool for Handwritten and Digital Texts

### Team Sonic Coder
- Bhavin Baldota
- Aditya Chavan
- Saumya Shah
- Sharvari Korde

## Project Overview

This project addresses the L&T NEUROHACK Silver Problem Statement by developing an innovative text summarization tool capable of efficiently processing and summarizing both handwritten and digital texts while operating entirely offline. Our solution caters to privacy-sensitive documents and remote areas lacking stable internet connectivity.

### Key Features

- Offline processing and summarization
- Support for handwritten and digital text
- Multiple file format handling (PDF, JSON, XML, TXT, images)
- High accuracy in text extraction and summarization
- Privacy-preserving local processing
- Optimized for devices with 16GB RAM or higher

## Repository Structure

```
NeurohackSilver/
│
├── OCR_Testing/
│   └── (Combined code for all file types and summary generation)
│
├── NLP_Model/
│   └── (Training code for the summarization model)
│
├── Handwritten_Model/
│   └── (Training code for handwritten text recognition)
│
├── Digital_Font_Model/
│   └── (Training code for digital font recognition)
│
├── Examples/
│   ├── Inputs/
│   │   └── (Sample input files of various types)
│   ├── Extracted_Text/
│       └── (Text files of extracted content)
│
└── README.md
```


## Technical Details

### PyTorch Foundation
Our solution is built on PyTorch, offering versatility in deep learning and compatibility with offline deployment.

### Multi-Model Framework
- **Handwritten Text Model:** Trained on 20,000 samples covering various handwriting styles.
- **Digital Text Extraction Model:** Trained on Google Fonts for diverse typeface recognition.
- **Specialized Models:** Fine-tuned for PDF, JSON, XML, Word, and Excel formats.

### Preprocessing Techniques
Advanced image processing to enhance text clarity and reduce OCR errors.

### OCR with Tesseract
Integrated Google's OCR technology for accurate text recognition.

### NLP-based Summarization
Utilizes PyTorch NLP models for both extractive and abstractive summarization.

## Future Improvements

- Enhance multi-language support
- Improve processing speed for large documents
- Develop a user-friendly GUI for easier interaction

## Acknowledgements

We thank L&T for organizing the NEUROHACK challenge and providing this opportunity to develop innovative solutions.

## License

[MIT License](LICENSE)

---

For more information about the L&T NEUROHACK challenge, visit [L&T NEUROHACK Official Website](https://www.larsentoubro.com/).
