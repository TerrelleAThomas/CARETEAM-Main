import shutil
import os

source_file = "/kaggle/input/dfdc-datatset/labeled_metadata.json"
destination_dir = '/kaggle/working/dfdc_annotated'
destination_file = os.path.join(destination_dir, 'labeled_metadata.json')

os.makedirs(destination_dir, exist_ok=True)
shutil.copy(source_file, destination_file)

print (f"Copied metadata to working directory: {destination_file}")
import os
import json
import cv2
from matplotlib import pyplot as plt

def load_metadata(metadata_path):
    with open(metadata_path, "r") as file:
        return json.load(file)

def save_metadata(metadata, output_file):
    # Save updated metadata
        with open(output_file, "w") as file:
            json.dump(metadata, file, indent=4)
        print(f"Updated metadata saved to {output_file}.")

def display_frame(frame): 
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

def process_videos(video_paths, metadata):
    for video_path in video_paths:
        video_name = os.path.basename(video_path)
        if video_name not in metadata:
            print(f"{video_name} not found in metadata.")
            continue
        
        if 'race' in metadata[video_name] and 'gender' in metadata[video_name]:
            print(f"{video_name} already has race and gender attributes.")
            continue
            
        # Open video and display the first frame
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video: {video_path}")
            continue
    
        ret, frame = cap.read()
        if ret:
            # Display the frame using Matplotlib
            display_frame(frame)
    
        cap.release()
        
        # Display the video name and prompt user for input
        print(f"Displaying video: {video_name}")
        race_input = input("Enter race (b for black, w for white, n for null): ").strip().lower()
        race_map = {"b": "black", "w": "white", "n": None}
        race_value = race_map.get(race_input, None)
        
        # Update metadata for provided race values
        if race_value is not None and 'race' not in metadata[video_name]:
            metadata[video_name]["race"] = race_value

        gender_input = input("Enter gender (m for male, f for female, n for null): ").strip().lower()
        gender_map = {"m":"male", "f": "female", "n": None}
        gender_value = gender_map.get(gender_input, None)

        if gender_value is not None and 'gender' not in metadata[video_name]:
            metadata[video_name]["gender"] = gender_value
# Preferred order of keys
key_order = ['label', 'split', 'race', 'gender', 'original']

# Reorder keys
def reorder_keys(data, key_order):
    ordered_data = {key: data[key] for key in key_order if key in data}
    for key in data:
        if key not in ordered_data:
            ordered_data[key] = data[key]
    return ordered_data

# Count demograhic make up
def count_demographics(metadata):
    demographics = {
        "black_female": 0,
        "white_female": 0,
        "black_male": 0,
        "white_male": 0,
    }

    for video_name, attributes in metadata.items():
        race = attributes.get("race")
        gender = attributes.get("gender")

        if race == "black" and gender == "female":
            demographics["black_female"] += 1
        elif race == "white" and gender == "female":
            demographics["white_female"] += 1
        elif race == "black" and gender == "male":
            demographics["black_male"] += 1
        elif race == "white" and gender == "male":
            demographics["white_male"] += 1
    
    return demographics

def main():            
    # File paths
    input_file = "/kaggle/input/dfdc-annotated/metadata.json"
    input_file_2 = '/kaggle/working/dfdc_annotated/metadata.json' #continuing annotation
    input_file_3 = '/kaggle/input/dfdc-datatset/labeled_metadata.json' #3rd try annotating
    input_file_4 = '/kaggle/working/labeled_metadata2.json' #reorder json keys
    output_file = "/kaggle/working/labeled_metadata2.json"
    video_directory = "/kaggle/input/deepfake-detection-challenge/test_videos"
    video_directory2 = "/kaggle/input/deepfake-detection-challenge/train_sample_videos"
    video_paths = [os.path.join(video_directory, filename) for filename in os.listdir(video_directory)]
    video_paths2 = [os.path.join(video_directory2, filename) for filename in os.listdir(video_directory2)]
    

    # Load metadata
    metadata = load_metadata(input_file_4)
    
    # Process videos
    #process_videos(video_paths2, metadata)

    #Reorder keys in metadata
    #for video_name in metadata:
        #metadata[video_name] = reorder_keys(metadata[video_name], key_order)
    
    # Save updated metadata
    #save_metadata(metadata, output_file)

    # demographics counts
    demographic_counts = count_demographics(metadata)

    print("Demographic Counts: ")
    for demographic, count in demographic_counts.items():
        print(f"{demographic}: {count}")

if __name__ == "__main__":
    main()

'''
Demographic Counts: 
black_female: 204
white_female: 132
black_male: 18
white_male: 46
'''
