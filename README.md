# L&T NEUROHACK - Silver Problem Statement Solution

## Offline Text Summarization Tool for Handwritten and Digital Texts

### Team Sonic Coder
- Bhavin Baldota - [LinkedIn - Bhavin Baldota](https://www.linkedin.com/in/bhavin-baldota-103553234)
- Aditya Chavan - [LinkedIn - Aditya Chavan](https://www.linkedin.com/in/aditya-chavan-5117aa268?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
- Saumya Shah - [LinkedIn - Saumya Shah](https://www.linkedin.com/in/saumya-shah-9b2579273?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
- Sharvari Korde - [LinkedIn - Sharvari Korde](https://www.linkedin.com/in/sharvari-korde-85b993268?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

## Running Flask Application 
- Using the 'Flask App' Folder just run 'app.py' file which contents complete end to end solution with UI and Offline Funtionality
- Output : ![alt text](<WhatsApp Image 2024-10-19 at 15.32.09_38a7af06.jpg>)
- Example Runs : ![alt text](<WhatsApp Image 2024-10-19 at 15.27.14_57278fb0.jpg>) ![alt text](<WhatsApp Image 2024-10-19 at 15.27.15_3802d5f3.jpg>)



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

For more information about the L&T NEUROHACK challenge, visit [L&T NEUROHACK Official Website](https://unstop.com/competitions/lt-neurohack-coep-mindspark-1177482?lb=NNlJdAID&fbclid=PAZXh0bgNhZW0CMTEAAabGJTa5pNxRyIzkXewlq3kVGnqpax2xh61YLwJ1QxBnCeNF_kHaOo0QtyI_aem_pgVH7177cRA2dyjworV-wQ).
