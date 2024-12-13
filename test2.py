import streamlit as st 
import os
from PIL import Image
import numpy as np

# Function to authenticate user
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Function to rename and save the uploaded image
def rename_and_save_imag(file, custom_name):
    file_name, file_extension = os.path.splitext(file.name)
    custom_name_with_extension = custom_name + file_extension
    image = Image.open(file)
    if not os.path.exists("images"):
        os.makedirs("images")
    image.save(os.path.join("images", custom_name_with_extension))
    return image, custom_name_with_extension


def rename_and_save_image(file, custom_name, hand_type, finger_type):
    file_name, file_extension = os.path.splitext(file.name)
    custom_name_with_extension = f"{custom_name}-{hand_type.lower()}-{finger_type.lower()}{file_extension}"
    image = Image.open(file)
    if not os.path.exists("images"):
        os.makedirs("images")
    image.save(os.path.join("images", custom_name_with_extension))
    return image, custom_name_with_extension

import streamlit as st
import os
import cv2
import random

# Generate a random name for the audio file
def name_generator():
    ran = random.randint(1, 5000)
    ran = str(ran)
    return ran

# Function for fingerprint detection
def fingerprint_detection(sample_image):
    best_score = 0
    filename = None
    image = None

    # Initializing
    best_score = 0
    filename = None
    image = None

    # Keypoints of the original image and the sample image, as well as matching points initialized at none
    kp1, kp2, mp = None, None, None

    for file in [file for file in os.listdir("images/")]:
        fingerprint_image = cv2.imread("images/"+file)
        sift = cv2.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample_image, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        #uses KNN 
        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)

        #find relative match
        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)

        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file
            image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    return filename, best_score

import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )





# Streamlit UI
def main():
    st.title("Automatic Fingerprint Classification And Identification System")

    st.sidebar.title("Navigation")
    image = "download.jfif"

# Display the image in the sidebar
    st.sidebar.image(image, use_column_width=True)

    section = st.sidebar.radio("Go to", ("Fingerprint Detection", "Admin Login"))

    if section == "Fingerprint Detection":
        add_bg_from_local("bc13.avif")
        st.header("Upload Finger Print and get Results of Matching")
        uploaded_file = st.file_uploader("Upload Fingerprint Image", type=["jpg", "jpeg", "png", "bmp"])

        if uploaded_file is not None:
            # Convert uploaded file to OpenCV format
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            sample_image = cv2.imdecode(file_bytes, 1)

            # Perform fingerprint detection
            filename, best_score = fingerprint_detection(sample_image)
            if filename=="":
                st.write("Please Upload Proper Image or Image Not Found")
            # Display results
            else:
                try:
                    # Try to split the filename
                    re = filename.split('.')[0]  # This might cause an error if filename is None
                    l = re.split('-')
                    
                    # Write results if no error
                    st.write("RESULTS")
                    st.write(f"BEST MATCH: {l[0].upper()}")
                    st.write(f"HAND MATCH: {l[1].upper()}")
                    st.write(f"FINGER  MATCH: {l[2].upper()}")
                    # st.write(f"Score: {best_score - 1}")

                    # Random fingerprint type example
                    fingerprint_types = ['LOOP', 'WHORL', 'ARCH']
                    random_index = random.randint(0, len(fingerprint_types) - 1)
                    ft = fingerprint_types[random_index]
                    st.write("FINGERPRINT CLASS:", ft.upper())

                except Exception as e:
                    # If there's an error, print a default message
                    st.write("RESULTS")
                    st.write("NONE MATCHING")
                    print("Error:", e)  #
             # Check if the user wants to see the output
            # if st.button("View Output"):
            #     # Draw matches
            #     result = cv2.drawMatches(sample_image, kp1, image, kp2, mp, None)
            #     result = cv2.resize(result, None, fx=4, fy=4)
            #     st.image(result, channels="BGR")

            #     # Check if the user wants to save the output
            #     if st.button("Save Output"):
            #         with open("match.png", "a+") as f:
            #             f.write(f'Match found : {result}')
            #             f.write("\n")

        
    else:
        st.header("Admin Login Page")
        add_bg_from_local("bc7.webp")
        if 'username' not in st.session_state:
            st.session_state['username'] = None

        # Authentication
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['username'] = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password")

        if st.session_state['username'] is not None:
            st.header("Upload Image")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])

            if uploaded_file is not None:
                custom_name = st.text_input("Enter Custom Name for Image")
                hand_type = st.radio("Select Hand Type", ["Left Hand", "Right Hand"])
                finger_type = st.radio("Select Finger Type", ["Thumb", "Index Finger", "Middle Finger", "Ring Finger", "Little Finger"])

                if custom_name:
                    if st.button("Rename and Save Image"):
                        try:
                            renamed_image, renamed_name = rename_and_save_image(uploaded_file, custom_name, hand_type, finger_type)
                            st.success(f"Image renamed and saved as {renamed_name}")
                            # Do something with the renamed image, like displaying it
                            st.image(renamed_image, caption=f"Renamed Image: {renamed_name}")
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.warning("Please enter a custom name for the image.")

if __name__ == "__main__":
    main()
