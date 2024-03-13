import streamlit as st

# Flow - Step 1 - Read data from a dictionary and display it as a set
# of radio buttons, adjusting the radio buttons to the user's rating
# Create seed data with a dictonary of foods organised by food type
# (fruit, vegetable, meat) and in each food type
# Have a list of associated foods (e.g. fruit = apple, banana, cherry)
# and a user rating for each food:
# e.g love, like, indefferent, dislike
#
# Outcome:
# - A selection box automatically populated with the food types
# - A container that includes a set of radio buttons for each food type
# - Each radio button is automatically set to the user's rating
# - Swapping between food types shows the correct ratings for each food
#
# Known Issues:
# - Setting a new value for a radio button does not update the
#   dictionary (Step 2)
foods = {
    "fruit": {
        "apple": "like",
        "banana": "love",
        "cherry": "dislike"
    },
    "vegetable": {
        "carrot": "dislike",
        "pea": "love",
        "potato": "dislike"
    },
    "meat": {
        "beef": "indifferent",
        "chicken": "like",
        "pork": "love"
    }
}

ratings = ["love", "like", "indifferent", "dislike"]

st.set_page_config(page_title="Streamlit Step 1", layout="wide")

st.write("# Streamlit Step 1")
st.write("Read data from a dictionary and display it as a set of radio buttons, adjusting the radio buttons to the user's rating") # noqa
st.warning("Setting a new value for a radio button does not update the dictionary (see Step 2)") # noqa

# Create a selectbox to choose a food type
food_type = st.selectbox("Select a food type", list(foods.keys()), index=0)

# create a placeholder to display the food list
select_food_ph = st.empty()

with select_food_ph.container():
    # List through the food type and display the food list as a
    # set of radio buttons that are automatically set to the user's rating
    for food, rating in foods[food_type].items():
        foods[food_type][food] = st.radio(food,
                                          ratings,
                                          index=ratings.index(rating),
                                          horizontal=True,
                                          key=food)
