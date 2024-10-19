function updateFileName(input) {
    const fileName = input.files.length > 0 ? input.files[0].name : 'Choose a file or drag it here';
    document.getElementById('file-name').innerText = fileName;

    // Show the OCR options when a file is selected
    document.getElementById('ocr-options').style.display = 'block';
}

function submitForm() {
    const fileInput = document.getElementById('file-input');
    const contextText = document.getElementById('context-box').value;
    const ocrType = document.querySelector('input[name="ocr-type"]:checked').value;

    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        document.getElementById('output-field').innerHTML = `
            <p>File: "${fileName}"</p>
            <p>Context: "${contextText}"</p>
            <p>OCR Type: "${ocrType}"</p>`;
    } else {
        alert("Please select a file.");
    }
}

function viewOCR() {
    alert("OCR View feature is not implemented yet.");
}
