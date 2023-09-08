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
import pydicom
from PIL import Image
import numpy as np

import tkinter as tk
from tkinter import filedialog

modality_include = ["IO", "DX"]  # List of modalities to include

def process_files(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, target_dir)

def process_file(file_path, target_dir):
    try:
        ds = pydicom.dcmread(file_path)
    except Exception as e:
        print(f"Error reading file: {file_path} with exception {e}")
        return
    
    #print(ds)  # This will print the DICOM tags, useful for debugging

    modality = ds.Modality if "Modality" in ds else "None"
    
    if modality not in modality_include:
        return
    
    image_date = ds.StudyDate if "StudyDate" in ds else "None"
    image_time = ds.StudyTime if "StudyTime" in ds else "None"
    ssn = ds.PatientID if "PatientID" in ds else "None"

    # print(f"SSN: {ssn}")

    target_path = os.path.join(target_dir, str(ssn))
    print(target_path)
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    target_file = f"{image_date}-{image_time}-{modality}.tif"
    target_file_path = os.path.join(target_path, target_file)
    
    img_array = ds.pixel_array
    img_array = ((img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255).astype(np.uint8)
    
    im = Image.fromarray(img_array)
    im.save(target_file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    source_dir = filedialog.askdirectory(title="Choose source directory")
    target_dir = filedialog.askdirectory(title="Choose target directory")
    process_files(source_dir, target_dir)
    print("Finished")
