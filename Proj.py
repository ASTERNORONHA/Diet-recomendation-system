import numpy as np
import pandas as pd
import streamlit as st
import re
import string
from sklearn.metrics.pairwise import cosine_similarity

# Load preprocessed dataset
file_path = r"C:\Users\Aster\OneDrive\Documents\Downloads\RS Project\recipes.csv"  # Update this path if needed
selected_columns = ['Name', 'Calories', 'FatContent', 'SaturatedFatContent',
                    'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
                    'FiberContent', 'SugarContent', 'ProteinContent', 'RecipeInstructions']

# Use 'on_bad_lines="skip"' instead of 'error_bad_lines=False'
diet = pd.read_csv(file_path, usecols=selected_columns, on_bad_lines='skip')

# 🔹 Preprocessing functions
def preprocess_text(text):
    """Lowercase, remove special characters, and clean whitespace"""
    text = re.sub(r'[@#$%^&*!`~]', '', text.lower()).strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_instructions(text):
    """Remove extra symbols and punctuation from RecipeInstructions"""
    text = text.lstrip('c("').rstrip('",)').replace(',', '')
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

diet['Name'] = diet['Name'].apply(preprocess_text)
diet['RecipeInstructions'] = diet['RecipeInstructions'].apply(clean_instructions)

# 🔹 Streamlit UI
st.title("🍽️ Diet Recommendation System")

# UI Layout: Two columns for better input arrangement
col1, col2 = st.columns(2)

# Left column inputs
with col1:
    age = st.number_input("Enter your age", min_value=1, max_value=100, value=25)
    weight = st.number_input("Enter your weight (kg)", min_value=30, max_value=200, value=60)
    height = st.number_input("Enter your height (cm)", min_value=100, max_value=250, value=165)
    goal = st.selectbox("Select your goal", ["weight_loss", "weight_gain", "maintenance"])

# Right column inputs
with col2:
    sex = st.selectbox("Select your gender", ["male", "female"])
    activity_level = st.selectbox("Select your activity level", 
                                  ["sedentary", "lightly_active", "moderate", "very_active", "extra_active"])
    diet_preference = st.selectbox("Select your diet preference", ["vegetarian", "vegan", "none"])
    allergies = st.text_input("Enter any allergies (comma-separated)").split(",")

# 🔹 Step 1: Calculate BMR using Mifflin-St Jeor Formula
def calculate_bmr(weight, height, age, sex):
    if sex == "male":
        return (9.99 * weight) + (6.25 * height) - (4.92 * age) + 5
    else:
        return (9.99 * weight) + (6.25 * height) - (4.92 * age) - 161

# 🔹 Step 2: Calculate TDEE
def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "sedentary": 1.2, "lightly_active": 1.375, "moderate": 1.55,
        "very_active": 1.725, "extra_active": 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

# 🔹 Step 3: Adjust Calories Based on Goal
def adjust_calories(tdee, goal):
    return tdee - 500 if goal == "weight_loss" else tdee + 500 if goal == "weight_gain" else tdee

# 🔹 Step 4: Macronutrient Distribution
def calculate_macros(calories, goal):
    ratios = {
        "weight_loss": (0.3, 0.3, 0.4),
        "weight_gain": (0.25, 0.3, 0.45),
        "maintenance": (0.3, 0.3, 0.4)
    }
    protein_ratio, fat_ratio, carb_ratio = ratios[goal]
    
    protein = (calories * protein_ratio) / 4
    fat = (calories * fat_ratio) / 9
    carbs = (calories * carb_ratio) / 4
    return protein, fat, carbs

# 🔹 Compute User Profile Nutritional Needs
bmr = calculate_bmr(weight, height, age, sex)
tdee = calculate_tdee(bmr, activity_level)
target_calories = adjust_calories(tdee, goal)
target_protein, target_fat, target_carbs = calculate_macros(target_calories, goal)

# 🔹 Step 6: Filter Recipes
filtered_diet = diet.copy()
if diet_preference in ["vegetarian", "vegan"]:
    filtered_diet = filtered_diet[filtered_diet["RecipeInstructions"].str.contains(diet_preference, case=False, na=False)]

for allergen in allergies:
    filtered_diet = filtered_diet[~filtered_diet["RecipeInstructions"].str.contains(allergen.strip(), case=False, na=False)]

# 🔹 Step 7: Content-Based Recommendation
def recommend_meals(user_calories, user_fat, user_carbs, user_protein, top_n=5):
    user_profile_vector = np.array([[user_calories, user_fat, user_carbs, user_protein, 0, 0, 0, 0, 0]])
    similarities = cosine_similarity(user_profile_vector, filtered_diet.iloc[:, 1:10].values)
    
    filtered_diet["Similarity"] = similarities[0]
    top_recommendations = filtered_diet.sort_values(by="Similarity", ascending=False).head(top_n)
    
    return top_recommendations[["Name", "Calories", "ProteinContent", "FatContent", "CarbohydrateContent", "SodiumContent", "RecipeInstructions"]]

# 🔹 Step 8: Get Recommendations
if st.button("🔍 Get Diet Recommendations"):
    recommendations = recommend_meals(target_calories, target_fat, target_carbs, target_protein, top_n=5)
    st.write("### 🍽️ Recommended Meals:")
    st.dataframe(recommendations)
