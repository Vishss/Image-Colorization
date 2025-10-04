import os
from colorizers import eccv16, siggraph17, preprocess_img, postprocess_tens, load_img
import torch
import matplotlib.pyplot as plt

input_folder = "imgs"  # Change as needed
output_folder = "imgs_out"
os.makedirs(output_folder, exist_ok=True)

model = eccv16(pretrained=True).eval()  # or siggraph17(pretrained=True).eval()

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_folder, filename)
        img = load_img(img_path)
        tens_l_orig, tens_l_rs = preprocess_img(img, HW=(256,256))
        out_img = postprocess_tens(tens_l_orig, model(tens_l_rs).cpu())
        out_path = os.path.join(output_folder, f"color_{filename}")
        plt.imsave(out_path, out_img)
        print(f"Saved: {out_path}")