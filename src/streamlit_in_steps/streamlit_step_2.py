import streamlit as st

# Flow - Step 2 - Read data from a dictionary and display it as a set
# of radio buttons, adjusting the radio buttons to the user's rating
# Create seed data with a dictonary of foods organised by food type
# (fruit, vegetable, meat) and in each food type
# Have a list of associated foods (e.g. fruit = apple, banana, cherry)
# and a user rating for each food:
# e.g love, like, indefferent, dislike
#
# Step 2 specifically adds support for:
# - persisting the user's ratings in the dictionary using session state.
# - State of radio buttons is maintained between food selections.
# - UI is enhanced to show columns for food type and rating
#
# Outcome:
# - A selection box automatically populated with the food types
# - A container that includes a set of radio buttons for each food type
# - Food type and rating is laid out in a column format, label is collapsed
#   to maintain row alignment with the food type
# - Each radio button is automatically set to the user's rating
# - Swapping between food types shows the correct ratings for each food
# - Updating a user rating persists between changes of food type
#
# Known Issues:
# - Cannot add new foods (Step 3)

if "foods" not in st.session_state:
    st.session_state.foods = {
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

st.set_page_config(page_title="Streamlit Step 2", layout="wide")

st.write("# Streamlit Step 2")
st.write("**Persisting the user's ratings** in the dictionary using session state") # noqa E501
st.write("UI is enhanced to **show columns for food type and rating**")

st.warning("Cannot add new foods (see Step 3)")

# Create a reference to the session state dictionary
foods = st.session_state.foods

# Create a selectbox to choose a food type
food_type = st.selectbox("Select a food type", list(foods.keys()), index=0)

# create a placeholder to display the food list
select_food_ph = st.empty()

with select_food_ph.container():
    # Create a column for the food type and a column for the ratings
    ft_col, rt_col = st.columns([0.3, 0.7])

    # List through the food type and display the food list as a
    # set of radio buttons that are automatically set to the user's rating
    for food, rating in foods[food_type].items():
        with ft_col:
            st.write(food)
        with rt_col:
            foods[food_type][food] = st.radio(food,
                                              ratings,
                                              index=ratings.index(rating),
                                              horizontal=True,
                                              label_visibility="collapsed",
                                              key=food)
