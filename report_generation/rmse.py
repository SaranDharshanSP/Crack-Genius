import os
import numpy as np
from PIL import Image, ImageEnhance
import google.generativeai as genai

genai.configure(api_key="AIzaSyCvqE4MkOSUXkYLGRXDQSEHVvAwj9Vf3i8")
model = genai.GenerativeModel('gemini-pro-vision')


def generate_images(path):
    image = Image.open(path)
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(1.4)  # Increase brightness
    dark_image = enhancer.enhance(0.5)  # Decrease brightness
    rotated_images = []
    for angle in range(90, 360, 90):
        rotated = image.rotate(angle)
        rotated_images.append(rotated)
    return [image, bright_image, dark_image, rotated_images]

def get_length(img):
    question = "Based on the provided image showing a crack, measure its length considering the longest dimension. Please provide your answer in either integer or decimal format."
    response = model.generate_content([question, img])
    response.resolve()
    length = response.text
    return float(length)

def error(actual, given):
    return given-actual

def rmse(errors):
    squared_errors = np.array(errors) ** 2
    mse = np.mean(squared_errors)
    rmse = np.sqrt(mse)/len(squared_errors)
    
    return rmse

rmse_values = []
for file in os.listdir("report_generation\images"):
    print("VQA on ", file)
    errors = []
    images = generate_images(os.path.join("report_generation\images",file))
    lengths = {"actual": float(file.split("_")[-1].replace(".jpg", ""))}

    lengths["unedited"] = get_length(images[0])
    lengths["dark"] = get_length(images[2])
    lengths["bright"] = get_length(images[1])
    lengths["rot1"] = get_length(images[3][0])
    lengths["rot2"] = get_length(images[3][1])
    lengths["rot3"] = get_length(images[3][2])

    print(lengths)
    for leng in list(lengths.items())[1:]:
        errors.append(error(lengths["actual"],leng[1]))
    rmse_values.append(rmse(errors))

print("Mean of RMSE: ", np.mean(rmse_values))