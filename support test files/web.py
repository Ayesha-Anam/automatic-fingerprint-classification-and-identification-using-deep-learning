import os
import cv2
import streamlit as st
from gtts import gTTS
from playsound import playsound
from PIL import Image
import numpy as np
import random

# Generate a random name for the audio file
def name_generator():
    ran = random.randint(1, 5000)
    return str(ran)

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang="en")
    new_name = name_generator() + ".mp3"
    tts.save(new_name)
    playsound(new_name)
    try:
        os.remove(new_name)
    except:
        pass

# Function to perform image matching
def image_matching(sample_bytes, images_folder):
    # Convert BytesIO object to numpy array
    sample = np.array(Image.open(BytesIO(sample_bytes)))
    best_score = 0
    filename = None
    image = None
    kp1, kp2, mp = None, None, None

    for file in os.listdir(images_folder):
        fingerprint_image = cv2.imread(os.path.join(images_folder, file))
        sift = cv2.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)

        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = min(len(keypoints_1), len(keypoints_2))

        match_score = len(match_points) / keypoints * 100

        if match_score > best_score:
            best_score = match_score
            filename = file
            image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    return filename, best_score, image, kp1, kp2, mp

# Streamlit app
def main():
    st.title("Image Matching App")
    st.write("Welcome to the Image Matching App!")

    sample_bytes = st.file_uploader("Upload Sample Image", type=["jpg", "jpeg", "png",'bmp'])

    if sample_bytes is not None:
        st.image(sample_bytes, caption="Sample Image", use_column_width=True)
        st.write("Performing image matching...")

        # Perform image matching
        filename, best_score, image, kp1, kp2, mp = image_matching(sample_bytes.getvalue(), "images/")

        st.write("-----RESULTS-----")
        if filename is not None:
            st.write(f"Best Match: {filename.split('.')[0]}")
            st.write(f"Score: {best_score}")
        else:
            st.write("No match found.")

        st.write("-----MATCHING POINTS-----")
        show_output = st.radio("Do you want to see the output?", ("Yes", "No"))

        if show_output == "Yes":
            result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
            st.image(result, caption="Matching Points", use_column_width=True)

            save_output = st.radio("Do you want to save the output?", ("Yes", "No"))

            if save_output == "Yes":
                st.write("Output saved as match.png.")
                cv2.imwrite("match.png", result)

        # Convert results to text for text-to-speech
        tts_text = f"The best match is {filename.split('.')[0]} with a score of {best_score}"
        speak(tts_text)

# Run the app
if __name__ == "__main__":
    main()
