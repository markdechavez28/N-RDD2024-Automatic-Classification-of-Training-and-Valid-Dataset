import os
import xml.etree.ElementTree as ET
import shutil

# For the base_dir, be reminded of the following file structure:
# Training and Validation Dataset > USA_voc
# The _voc file shall be unzipped for this program to work
# Change the value of the base_dir to the directory of your _voc file
base_dir = r''

# Since for this code, you will access the train directory of the _voc, point to the train directory
train_path = os.path.join(base_dir, 'train')  

def organize_images_by_defect():
    if not os.path.exists(train_path):
        print(f'Valid folder not found: {train_path}')
        return

    # These are arrays to store the jpeg and xml files in the _voc file
    image_filenames = []
    xml_filenames = []

    # Collect all image and XML files in the valid folder
    for file in os.listdir(train_path):
        if file.lower().endswith(('.jpg', '.png')):  
            image_filenames.append(file)
        elif file.lower().endswith('.xml'):
            xml_filenames.append(file)

    # Debug output
    print(f'Found {len(image_filenames)} images and {len(xml_filenames)} XML files.')  

    # Create directories for each defect type found
    defect_types = set()
    for xml_file in xml_filenames:
        xml_file_path = os.path.join(train_path, xml_file)

        # Parse the XML file
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f'Error parsing XML file {xml_file_path}: {e}')
            continue

        # Get the corresponding image file name from XML
        image_name = root.find('filename').text

        # Check if the corresponding image exists
        if image_name not in image_filenames:
            print(f'Warning: Image {image_name} not found in images directory.')
            continue

        # Extract defect types from the XML
        for obj in root.iter('object'):
            defect_type = obj.find('name').text
            defect_types.add(defect_type)

            # Create folder for defect type if it doesn't exist
            defect_folder = os.path.join(train_path, defect_type)
            os.makedirs(defect_folder, exist_ok=True)

            # Copy the image to the corresponding defect folder
            image_path_to_copy = os.path.join(train_path, image_name)
            shutil.copy(image_path_to_copy, defect_folder)
            print(f'Moved {image_name} to {defect_folder}')  # Debug output

    print(f'Defect types found: {defect_types}')

# Run the function to organize images
organize_images_by_defect()
