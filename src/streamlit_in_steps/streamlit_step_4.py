import streamlit as st
import pandas as pd
import os

# Flow - Step 4 - Read data from a dictionary and display it as a set
# of radio buttons, adjusting the radio buttons to the user's rating
# Create seed data with a dictonary of foods organised by food type
# (fruit, vegetable, meat) and in each food type
# Have a list of associated foods (e.g. fruit = apple, banana, cherry)
# and a user rating for each food:
# e.g love, like, indefferent, dislike
#
# User choices are persisted in session state
# Users can add new food items which are persisted in state
#
# Step 4 specifically adds support for:
# - Saving the user decisions as a CSV file
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
# - Users can save their data to a CSV file
#
# Known Issues:
# - Cannot load data from a CSV file (step 5)
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

output_file_prefix = "output/food_ratings"

st.set_page_config(page_title="Streamlit Step 4", layout="wide")

st.write("# Streamlit Step 4")
st.write("Allows the user to **save decisions to a CSV file** in long or horizontal format") # noqa E501

st.warning("Cannot load data from a CSV (see Step 4)")


def write_csv(file_path, dataframe):
    success = False
    error = ""
    try:
        if os.path.exists(file_path):
            raise FileExistsError
        # Use dataframe.csv to save the data
        dataframe.to_csv(file_path, index=False)
        success = True
    except FileNotFoundError:
        error = f"File {file_path} not found"
    except FileExistsError:
        error = f"File {file_path} already exists"
    except Exception as e:
        error = f"An error occurred: {e}"
    return success, error


def format_data(type, data):
    formatted_data = []

    # Long type format is a list of lists
    # food_type, food, rating
    # e.g.
    # fruit, apple, like
    # vegetable, carrot, dislike
    if type == "long":
        data_tuples = []
        for food_type, food_ratings in data.items():
            for food, rating in food_ratings.items():
                data_tuples.append((food_type, food, rating))

        # Create DataFrame
        formatted_data = pd.DataFrame(data_tuples,
                                      columns=['food_type',
                                               'food',
                                               'rating'])

    elif type == "horizontal":
        # horizontal type format is a shorter condensed format
        # <food_type>, <food_type>_rating, <food_type>, <food_type>_rating etc
        # e.g.
        # fruit, fruit_rating, vegetable, vegetable_rating, meat, meat_rating
        # orange, like, cabbage, dislike, beef, indifferent
        #
        # When categories have unequal lists of items empty cells are written
        # e.g.
        # apple, love,,, chicken, like
        # Determine the maximum length of the lists in all categories
        max_length = max(
            len(data["fruit"]),
            len(data["vegetable"]),
            len(data["meat"])
        )

        formatted_data = pd.DataFrame(
            {
                "fruit": list(data["fruit"].keys()) +
                [""] * (max_length - len(data["fruit"])),
                "fruit_rating": list(data["fruit"].values()) +# noqa E501
                [""] * (max_length - len(data["fruit"])),
                "vegetable": list(data["vegetable"].keys()) +
                [""] * (max_length - len(data["vegetable"])),
                "vegetable_rating": list(data["vegetable"].values()) +
                [""] * (max_length - len(data["vegetable"])),
                "meat": list(data["meat"].keys()) +# noqa E501
                [""] * (max_length - len(data["meat"])),
                "meat_rating": list(data["meat"].values()) +# noqa E501
                [""] * (max_length - len(data["meat"])),
            }
        )

    return formatted_data


# Create a reference to the session state dictionary
foods = st.session_state.foods

# Create a selectbox to choose a food type
food_type = st.selectbox("Select a food type", list(foods.keys()), index=0)

# create a placeholder to display the food list
select_food_ph = st.empty()

with select_food_ph.container(border=True):
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
        with select_food_ph.container(border=True):
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
    else:
        st.warning("No food entered")

st.divider()

wf_col, space_col, lg_col = st.columns(3)
csv_written = None

csv_output_ph = st.empty()

with lg_col:
    # Create a button to save the user's data to a CSV file
    if st.button("Save CSV - Long Format"):
        # Format the data from the dictionary
        dataframe = format_data(type="long", data=foods)

        # Save the data to a CSV file
        csv_written, error = write_csv(f"{output_file_prefix}.csv", dataframe)

with wf_col:
    # Create a button to save the user's data to a CSV file
    if st.button("Save CSV - Horizontal Format"):
        dataframe = format_data(type="horizontal", data=foods)

        # Save the data to a CSV file
        csv_written, error = write_csv(f"{output_file_prefix}.csv", dataframe)

if csv_written is not None and csv_written is True:
    csv_output_ph.success(f"Data saved to {output_file_prefix}.csv")
elif csv_written is not None and csv_written is False:
    csv_output_ph.error(error)
