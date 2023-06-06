import argparse
import os
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='D:/Steam/steamapps/common/assettocorsa/content/cars/', help='Assetto Corsa cars path.')
    parser.add_argument('--carname', type=str, help='name of the car folder to modify.')
    parser.add_argument('--initial_power', type=float, default=200, help='Initial power(hp) of the car, can be examined via content manager.')
    parser.add_argument('--target_power', type=float, default=300, help='desired power(hp) of the car.')
    args = parser.parse_args()

    st.title('Car Power Modifier')

    # Option to select a file in the directory
    data_path = st.selectbox('Select a car folder:', os.listdir(args.path))
    args.carname = data_path

    # Option to input initial and target power
    args.initial_power = st.number_input('Initial Power (HP):', min_value=0.0, value=200.0, step=1.0)
    args.target_power = st.number_input('Target Power (HP):', min_value=0.0, value=300.0, step=1.0)

    # Display the car preview image
    preview_path = os.path.join(args.path, args.carname, 'skins', get_first_folder(os.path.join(args.path, args.carname, 'skins')), 'preview.jpg')
    if os.path.exists(preview_path):
        st.image(Image.open(preview_path), caption='Car Preview')
    else:
        st.warning('Car preview image not found.')

    # Button to modify car power
    if st.button('Modify Car Power'):
        path = os.path.join(args.path, args.carname, 'data/power.lut')
        write_doc(path, args.initial_power, args.target_power)
