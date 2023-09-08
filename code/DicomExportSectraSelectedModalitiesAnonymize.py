# =============================================================================
# Script to extract every DICOM image from a Sectra media export
# Files are stored in folder with foldername PatientID and the filename 
# is created from the StudyDate, StudyTime and Modality tag
# Only images from modalities in modality_include will be exported
# 
# Written by Gerald Torgersen gerald@odont.uio.no
# License: CC0 1.0 Universal (CC0 1.0) 
# https://creativecommons.org/publicdomain/zero/1.0/
# =============================================================================

import os
import csv
import pydicom
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

modality_include = ["IO", "DX"]  # List of modalities to include
num_digits = 4 # Format of the serie number

def process_files(source_dir, target_dir, id_map, num_digits=3):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, target_dir, id_map, num_digits)

def process_file(file_path, target_dir, id_map, num_digits):
    try:
        ds = pydicom.dcmread(file_path)
    except Exception as e:
        print(f"Error reading file: {file_path} with exception {e}")
        return
    
    modality = ds.Modality if "Modality" in ds else "None"
    
    if modality not in modality_include:
        return
    
    image_date = ds.StudyDate if "StudyDate" in ds else "None"
    image_time = ds.StudyTime if "StudyTime" in ds else "None"
    ssn = ds.PatientID if "PatientID" in ds else "None"

    # Create anonymous serial number for image storage:
    series_number = id_map.setdefault(ssn, len(id_map) + 1)
    series_number_str = str(series_number).zfill(num_digits)
    
    target_path = os.path.join(target_dir, series_number_str)
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    target_file = f"{image_date}-{image_time}-{modality}.tif"
    target_file_path = os.path.join(target_path, target_file)
    
    img_array = ds.pixel_array
    img_array = ((img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255).astype(np.uint8)
    
    im = Image.fromarray(img_array)
    im.save(target_file_path)

# Writes the keyfile for anonymization
def save_id_map_to_csv(id_map, csv_path, num_digits=3):
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['PatientID', 'SeriesNumber'])
        for k, v in id_map.items():
            series_number_str = str(v).zfill(num_digits)
            csvwriter.writerow([k, series_number_str])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    source_dir = filedialog.askdirectory(title="Choose source directory")
    target_dir = filedialog.askdirectory(title="Choose target directory")
    csv_path = os.path.join(target_dir, "keyfile.csv")

    id_map = defaultdict(int)  # Dictionary to map PatientID to SeriesNumber

    process_files(source_dir, target_dir, id_map, num_digits)

    save_id_map_to_csv(id_map, csv_path, num_digits)
    print("Finished")
