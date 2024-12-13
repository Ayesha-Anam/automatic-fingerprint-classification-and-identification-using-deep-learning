import streamlit as st
import os
from PIL import Image

# Function to authenticate user
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Function to rename and save the uploaded image
def rename_and_save_image(file, custom_name):
    file_name, file_extension = os.path.splitext(file.name)
    custom_name_with_extension = custom_name + file_extension
    image = Image.open(file)
    if not os.path.exists("images"):
        os.makedirs("images")
    image.save(os.path.join("images", custom_name_with_extension))
    return image, custom_name_with_extension

# Streamlit UI
def main():
    st.title("Admin Page")

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
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png","bmp"])

        if uploaded_file is not None:
            custom_name = st.text_input("Enter Custom Name for Image")
            if custom_name:
                if st.button("Rename and Save Image"):
                    try:
                        renamed_image, renamed_name = rename_and_save_image(uploaded_file, custom_name)
                        st.success(f"Image renamed and saved as {renamed_name}")
                        # Do something with the renamed image, like displaying it
                        st.image(renamed_image, caption=f"Renamed Image: {renamed_name}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a custom name for the image.")

        if st.button("Logout"):
            st.session_state['username'] = None

if __name__ == "__main__":
    main()
