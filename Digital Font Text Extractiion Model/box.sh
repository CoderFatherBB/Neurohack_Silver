#!/bin/bash

mkdir -p processed_training

for img in Preprocessed_Images/processed_TEST_*.jpg; do
    base=$(basename "$img" .jpg)
    
    tesseract "$img" "processed_training/$base" -l eng --psm 1 batch.nochop makebox
done
