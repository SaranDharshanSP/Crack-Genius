**Crack Report Generation using Generative AI Models**

---

**Description:**

This project focuses on generating crack reports utilizing Generative AI Models. The system uses a Visual Question Answering (VQA) model and a Large Language Model (LLM) to extract information about cracks from images and generate detailed reports based on the extracted data.

---

**File Structure:**

- **main.py**: This file contains the code for generating crack reports. It utilizes the VQA model and LLM to extract crack details and generate markdown reports.

---

**Dependencies:**

- Python 3.x
- pandas
- Pillow
- dotenv
- google.generativeai
- streamlit

---

**Setup Instructions:**

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Ensure that the necessary Gemini API keys are provided in the `.env` file for accessing generative AI models.
3. Place the images of cracks in the designated path (`IMG_PATH`).

---

**Usage:**

1. Run the `main.py` file using the command `streamlit run main.py`.
2. The script will extract crack details from the provided images using the VQA model.
3. It will then generate a markdown report containing crack details and descriptions using the LLM.
4. The generated report will be displayed using Streamlit.

