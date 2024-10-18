


TRAINEDDATA_PATH="/Users/adityachavan/Desktop/Acc/processed_training/eng.traineddata"


TEST_IMAGES_DIR="/Users/adityachavan/Desktop/Acc/test_images"


OUTPUT_DIR="/Users/adityachavan/Desktop/Acc/ocr_results"


if [ ! -f "$TRAINEDDATA_PATH" ]; then
    echo "Trained data file not found at $TRAINEDDATA_PATH"
    exit 1
fi


if [ ! -d "$TEST_IMAGES_DIR" ]; then
    echo "Test images directory not found at $TEST_IMAGES_DIR"
    exit 1
fi


mkdir -p "$OUTPUT_DIR"


export TESSDATA_PREFIX=$(dirname "$TRAINEDDATA_PATH")


for img in "$TEST_IMAGES_DIR"/*.jpg; do
    base=$(basename "$img" .jpg)
    
    tesseract "$img" "$OUTPUT_DIR/$base" -l eng --psm 6
done

echo "OCR processing completed. Results are saved in $OUTPUT_DIR"
