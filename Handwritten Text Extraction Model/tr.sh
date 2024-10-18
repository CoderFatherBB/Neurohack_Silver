!/bin/bash

# Step 1: Generate .tr files
for img in processed_training/*.jpg; do
    base=$(basename "$img" .jpg)
    # Run Tesseract OCR on the image to generate the .tr file
    tesseract "$img" "processed_training/$base" -l eng --psm 6 nobatch box.train
done

# Step 2: Create font_properties file
echo "handwriting 0 0 0 0 0" > processed_training/font_properties

# Step 3: Generate unicharset
unicharset_extractor training_data/*.box

# Step 4: Extract features and train
# Create unicharset file
mftraining -F processed_training/font_properties -U unicharset -O processed_training/eng.unicharset processed_training/*.tr
cntraining processed_training/*.tr

Step 5: Combine training data into a single .traineddata file
mv inttemp eng.inttemp
mv normproto eng.normproto
mv pffmtable eng.pffmtable
mv shapetable eng.shapetable
combine_tessdata processed_training/eng.

# The final trained model will be in processed_training/eng.traineddata
echo "Training completed. The trained model is in processed_training/eng.traineddata"
