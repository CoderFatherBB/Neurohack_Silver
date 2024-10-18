#!/bin/bash

# Step 1: Generate box files
for img in training_data/*.png; do
    tesseract $img ${img%.png} -l eng --psm 6 batch.nochop makebox
done

# Step 2: Create training data
for img in training_data/*.png; do
    base=$(basename $img .png)
    tesseract $img $base nobatch box.train
done

# Step 3: Compute the character set
unicharset_extractor training_data/*.box

# Step 4: Create font properties file
for img in training_data/*.png; do
    base=$(basename $img .png)
    echo "$base 0 0 0 0 0" >> font_properties
done

# Step 5: Clustering
shapeclustering -F font_properties -U unicharset training_data/*.tr

# Step 6: MFTraining
mftraining -F font_properties -U unicharset -O eng.unicharset training_data/*.tr

# Step 7: CNTraining
cntraining training_data/*.tr

# Step 8: Move the generated files
mv inttemp eng.inttemp
mv normproto eng.normproto
mv pffmtable eng.pffmtable
mv shapetable eng.shapetable

# Step 9: Combine the trained data files into a traineddata file
combine_tessdata eng.
