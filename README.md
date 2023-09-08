# Dicom-Export-Sectra-Media
Theese files may be usefull if you are using a Sectra PACS of have received media from a Sectra PACS. The scripts extract DICOM files from a Sectra media export structure. 
Files are stored in directories named PatiendID and filenames created from StudyDate, StudyTime and Modality tag. Mainly for use to export images for analysis in non-DICOM applications.

# Versions
- DicomExportSectra.py (base version)
  - Extracts all DICOM files to directories named by PatientID (not anonymous)
  - edit file_format variable to choose output file format
- DicomExportSectraSelectedModalities.py (lets you select which modalities to include in export)
  - As base version but lets you choose to only export files from selected modalities
  - Edit list modality_include to choose modalities  
- DicomExportSectraSelectedModalitiesAnonymize.py (also allows for anonymized storage providing a key file)
  - As version over, but supports anonymized export
  - Key file in csv format mapping anonymized serie number to PatientID is saved
  - Edit variable num_digits to specify output format of serie number    

# Instructions
1) Export examinations from one ore more patients to a folder or CD (Sectra media export)
2) Run the script in a Python environment
3) Point to the DICOM directory in the Sectra media export
4) Point to an empty directory as target for the exported files

You have to modify the scripts for choices like file format.
