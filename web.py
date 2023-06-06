import os
from zipfile import ZipFile
from PIL import Image
import streamlit as st

def load_doc(path):
    with open(path, 'r') as file:
        return file.read().split()

def write_doc(path, current_pr, target_pr):
    rpm_file = load_doc(path)
    rpm_list = read_rpm(rpm_file)
    multiplier = get_modifier(current_pr, target_pr)
    power_list = get_rpm(rpm_list, multiplier)
    final_file = final_power(rpm_file, power_list)
    with open(path, 'w') as file:
        file.writelines('%s\n' % item for item in final_file)
    st.success('Car power modified successfully!')

def read_rpm(file):
    return [float(line.split('|')[1]) for line in file]

def get_modifier(current_power, target_power):
    return target_power / current_power

def get_rpm(power, multiplier):
    return [round(x * multiplier) for x in power]

def final_power(initial_list, power_list):
    return [f'{line.split("|")[0]}|{power}' for line, power in zip(initial_list, power_list)]

def get_first_folder(path):
    for folder in os.listdir(path):
        if '.' not in folder:
            return folder
    return None

st.title('Car Power Modifier')

uploaded_file = st.file_uploader('Upload a car folder:', type='zip')
if uploaded_file is not None:
    # Extract the uploaded zip file to a temporary directory
    temp_dir = st._get_session_state().temp_dir
    with ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Get the name of the extracted car folder
    data_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Option to input initial and target power
    initial_power =
