import streamlit as st

# Flow - Step 3 - Read data from a dictionary and display it as a set
# of radio buttons, adjusting the radio buttons to the user's rating
# Create seed data with a dictonary of foods organised by food type
# (fruit, vegetable, meat) and in each food type
# Have a list of associated foods (e.g. fruit = apple, banana, cherry)
# and a user rating for each food:
# e.g love, like, indefferent, dislike
#
# User choices are persisted in session state
#
# Step 3 specifically adds support for:
# - Adding new food items to the list
#
# Outcome:
# - A selection box automatically populated with the food types
# - A container that includes a set of radio buttons for each food type
# - Food type and rating is laid out in a column format, label is collapsed
#   to maintain row alignment with the food type
# - Each radio button is automatically set to the user's rating
# - Swapping between food types shows the correct ratings for each food
# - Updating a user rating persists between changes of food type
# - Adding a new food item to the list persists between changes of food type
#
# Known Issues:
# - Cannot output the user changes to a CSV file (step 4)
# - Note: Using a text_input and button means the text area has
#   "Hit enter to apply" which is meaningless for the use case. This is a
#   known limitation in Streamlit regardless of if forms or text_input and a
#   button is used.

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

st.set_page_config(page_title="Streamlit Step 3", layout="wide")

st.write("# Streamlit Step 3")
st.write("Allows the user to **add new foods** to each food category")

st.warning("Cannot output selections and updates to lists as CSV (see Step 4)")
st.info("Using a text_input and button means the text area has 'Hit enter to apply' which is meaningless for the use case. This is a known limitation in Streamlit regardless of if forms or text_input and a button is used.") # noqa E501

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

# Create a text input to add a new food item
add_food_ph = st.empty()
new_food = add_food_ph.text_input("Add a new food",
                                  key="new_food"+str(len(foods[food_type])))

if st.button("Add Food"):
    if new_food:
        with select_food_ph.container():
            with ft_col:
                st.write(new_food)
            with rt_col:
                foods[food_type][new_food] = st.radio(new_food,
                                                      ratings,
                                                      index=ratings.index(
                                                        "indifferent"
                                                        ),
                                                      horizontal=True,
                                                      label_visibility="collapsed", # noqa E501
                                                      key=new_food)

                # Reset the text input for the next entry
                add_food_ph.text_input("Add a new food", value="",
                                       key="new_food"+str(len(foods[food_type]))) # noqa E501

        st.write(f"{new_food} added to {food_type}")
    else:
        st.info("No food entered to add to the list")
