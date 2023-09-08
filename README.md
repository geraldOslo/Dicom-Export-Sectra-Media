# Dicom-Export-Sectra-Media
Theese files may be usefull if you are using a Sectra PACS of have received media from a Sectra PACS. The scripts extract DICOM files from a Sectra media export structure. 
Files are stored in directories named PatiendID and filenames created from StudyDate, StudyTime and Modality tag. Mainly for use to export images for analysis in non-DICOM applications.

# Versions
- DicomExportSectra.py (base version)
- DicomExportSectraSelectedModalities.py (lets you select which modalities to include in export)
- DicomExportSectraSelectedModalitiesAnonymize.py (also allows for anonymized storage providing a key file)

# Instructions
1) Export examinations from one ore more patients to a folder or CD (Sectra media export)
2) Run the script in a Python environment
3) Point to the DICOM directory in the Sectra media export
4) Point to an empty directory as target for the exported files

You have to modify the scripts for choices like file format.
