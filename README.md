# 🥗 Diet Recommendation System

A smart diet recommendation system built using machine learning that provides personalized meal suggestions based on user input like age, weight, height, dietary goals, and preferences. The system filters recipes based on nutritional needs and offers meal plans tailored to the user.

---

## 📊 Dataset Used

The project uses the **[Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)** dataset from Kaggle.

- 📂 Source: Kaggle (by Shuyang Li)
- 🗃️ Files included:
  - `RAW_recipes.csv` – Recipe information including ingredients and nutrition
  - `RAW_interactions.csv` – User interaction data (ratings, reviews)
- 🔗 Dataset URL: [https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

> **Note:** Due to GitHub’s 100MB file size limit, the dataset is **not included** in this repository. Please download it from Kaggle and place the required CSV files in the project directory.

---

## 🚀 Features

- Calculate BMR and TDEE based on user input
- Filter recipes based on:
  - Caloric needs
  - Dietary preferences (e.g., vegan, keto)
  - Allergies and ingredient restrictions
- Recommend top meals using cosine similarity on nutritional data

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy, Scikit-learn
- Streamlit (for UI)
- Cosine similarity for recommendation
- Git for version control

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ASTERNORONHA/Diet-recomendation-system.git
   cd Diet-recomendation-system
