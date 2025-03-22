import streamlit as st
import requests
from pint import UnitRegistry

# Initialize unit registry
ureg = UnitRegistry()

# Custom function for temperature conversion
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "celsius" and to_unit == "kelvin":
        return value + 273.15
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return (value - 32) * 5/9 + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        return value - 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        return (value - 273.15) * 9/5 + 32
    else:
        return "Invalid Temperature Conversion"

# Function to convert general units
def convert_units(value, from_unit, to_unit):
    try:
        from_quantity = value * ureg(from_unit)
        to_quantity = from_quantity.to(to_unit)
        return to_quantity.magnitude
    except Exception as e:
        return str(e)

# Function to convert currency using ExchangeRate-API
def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    
    if "rates" in data and to_currency in data["rates"]:
        converted_amount = amount * data["rates"][to_currency]
        return round(converted_amount, 2)
    else:
        return "Invalid Currency Code"

# Streamlit App
def main():
    # CSS for styling
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #ff9a9e, #fad0c4);
            font-family: Arial, sans-serif;
        }
        .stApp {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

    # App Title
    st.markdown("<h1 style='text-align: center; color: black;'>🌍 Unit Converter by Mahrukh</h1>", unsafe_allow_html=True)
    
    # Conversion Type Selection
    option = st.selectbox("Select conversion type", ["Length", "Weight", "Temperature", "Currency"])
    
    value = st.number_input("Enter value:", min_value=0.0, format="%.2f")
    
    if option == "Length":
        from_unit = st.selectbox("From", ["meter", "kilometer", "mile", "yard", "inch", "foot"])
        to_unit = st.selectbox("To", ["meter", "kilometer", "mile", "yard", "inch", "foot"])
    elif option == "Weight":
        from_unit = st.selectbox("From", ["gram", "kilogram", "pound", "ounce"])
        to_unit = st.selectbox("To", ["gram", "kilogram", "pound", "ounce"])
    elif option == "Temperature":
        from_unit = st.selectbox("From", ["celsius", "fahrenheit", "kelvin"])
        to_unit = st.selectbox("To", ["celsius", "fahrenheit", "kelvin"])
    elif option == "Currency":
        from_unit = st.text_input("From Currency (e.g., USD)", value="USD").upper()
        to_unit = st.text_input("To Currency (e.g., EUR)", value="EUR").upper()
    
    if st.button("Convert 🔄"):
        if option == "Currency":
            converted_value = convert_currency(value, from_unit, to_unit)
        elif option == "Temperature":
            converted_value = convert_temperature(value, from_unit, to_unit)
        else:
            converted_value = convert_units(value, from_unit, to_unit)
        
        st.markdown(
    f'<div style="background-color:#d4edda; padding:10px; border-radius:5px;">'
    f'<p style="color:black; font-size:20px; font-weight:bold;">✅ {value} {from_unit} = {converted_value} {to_unit}</p>'
    f'</div>', 
    unsafe_allow_html=True)

if __name__ == "__main__":
    main()