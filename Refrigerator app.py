# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_AK6sM-9yXTzoJAwoDlF6GetnMA5gDUt
"""

import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import io
import streamlit.components.v1 as components

def extract_ingredients_from_receipt(image):
    """Simulated OCR extraction of ingredients from receipt image."""
    return ["Milk", "Eggs", "Butter", "Flour", "Sugar"]  # Dummy data

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

st.markdown("""
    <style>
        .expiration-list {
            background-color: #FFFBF2;
            padding: 10px;
            border-radius: 10px;
        }
        .exp-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            font-weight: bold;
        }
        .exp-red { background-color: #FF6B6B; color: white; }
        .exp-orange { background-color: #FFA94D; color: white; }
        .exp-yellow { background-color: #FFD43B; color: black; }
        .exp-green { background-color: #A9E34B; color: black; }
        .fab {
            position: fixed;
            bottom: 70px;
            right: 20px;
            background-color: #FFA94D;
            color: white;
            padding: 12px;
            border-radius: 50%;
            font-size: 20px;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Smart Refrigerator App 🍽️")

# Upload Receipt Section
st.header("📄 Upload Receipt")
uploaded_file = st.file_uploader("Upload your receipt image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    ingredients = extract_ingredients_from_receipt(image)
    shelf_life_days = {"Milk": 7, "Eggs": 14, "Butter": 30, "Flour": 180, "Sugar": 365}  # Sample shelf life data

    today = datetime.date.today()
    inventory_items = [
        {"Ingredient": ing, "Expiration Date": today + datetime.timedelta(days=shelf_life_days.get(ing, 7))}
        for ing in ingredients
    ]

    st.session_state.inventory.extend(inventory_items)
    st.success("Ingredients added to inventory!")

# Display Inventory Section
st.header("🥕 Food Expiration Dates")
inventory_df = pd.DataFrame(st.session_state.inventory)
if not inventory_df.empty:
    inventory_df = inventory_df.sort_values("Expiration Date")

    st.markdown('<div class="expiration-list">', unsafe_allow_html=True)

    for index, row in inventory_df.iterrows():
        days_remaining = (row["Expiration Date"] - datetime.date.today()).days
        if days_remaining <= 0:
            color_class = "exp-red"
        elif days_remaining == 1:
            color_class = "exp-orange"
        elif days_remaining <= 7:
            color_class = "exp-yellow"
        else:
            color_class = "exp-green"

        st.markdown(
            f'<div class="exp-item {color_class}">{row["Ingredient"]} - {row["Expiration Date"].strftime("%d %b")} <button style="border: none; background: transparent; cursor: pointer;">🗑️</button></div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("No ingredients available.")

# Floating Action Button
st.markdown('<div class="fab">+</div>', unsafe_allow_html=True)

# Bottom Navigation Bar
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #FFEECF; padding: 10px; display: flex; justify-content: space-around;">
        <span>ℹ️ About this app</span>
        <span>📋 List</span>
        <span>⚙️ Settings</span>
    </div>
""", unsafe_allow_html=True)