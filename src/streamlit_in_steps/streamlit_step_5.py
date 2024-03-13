import streamlit as st
import pandas as pd
import os

# Flow - Step 5 - Read data from a dictionary and display it as a set
# of radio buttons, adjusting the radio buttons to the user's rating
# Create seed data with a dictonary of foods organised by food type
# (fruit, vegetable, meat) and in each food type
# Have a list of associated foods (e.g. fruit = apple, banana, cherry)
# and a user rating for each food:
# e.g love, like, indefferent, dislike
#
# User choices are persisted in session state
# Users can add new food items which are persisted in state
# Users can save changes as a CSV file in either a long or horizontal format
#
# Step 5 specifically adds support for:
# - Loading data from a CSV file, CSV support is limited to horizontal format
# - Resetting session state when CSV file is changed
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
# - Users can load their data from a CSV file that is in horizontal format
#
# Known Issues:
# - Long format CSVs are not supported for loading
# - Note: Using a text_input and button means the text area has
#   "Hit enter to apply" which is meaningless for the use case. This is a
#   known limitation in Streamlit regardless of if forms or text_input and a
#   button is used.

if "foods" not in st.session_state:
    st.session_state.foods = {
    }

if "build_food_dict" not in st.session_state:
    st.session_state.build_food_dict = True

if 'csv_file_name' not in st.session_state:
    st.session_state.csv_file_name = None

ratings = ["love", "like", "indifferent", "dislike", "review"]

output_file_prefix = "output/food_ratings"

st.set_page_config(page_title="Streamlit Step 5", layout="wide")

st.write("# Streamlit Step 5")
st.write("Allows the user to **load data in horizontal format**") # noqa E501

st.warning("CSV file must be **Horizontal** format to load data")


def reset_session_state():
    st.session_state.foods = {}
    st.session_state.build_food_dict = True
    st.session_state.csv_file_name = None


# This function assumes the loaded file is in the horizontal format
# and the columns are named "fruit", "fruit_rating", "vegetable",
# "vegetable_rating", "meat", "meat_rating"
# It caters for the scenario where only the food columns are present
def build_foods_dict(df):
    # Initialise a foods dictionary which
    # is a nested dictionary by food type and then food/rating
    foods_dict = {
        "fruit": {},
        "vegetable": {},
        "meat": {},
    }

    # Check if the adoption columns already exist and create them if not
    if "fruit_rating" not in df.columns:
        df["fruit_rating"] = "review"
    if "vegetable_rating" not in df.columns:
        df["vegetable_rating"] = "review"
    if "meat_rating" not in df.columns:
        df["meat_rating"] = "review"

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        fruit = row.get("fruit")
        vegetable = row.get("vegetable")
        meat = row.get("meat")

        # Get the rating for each food
        fruit_rating = row.get("fruit_rating")
        vegetable_rating = row.get("vegetable_rating")
        meat_rating = row.get("meat_rating")

        # If a food exists in the column but the rating does not
        # default the rating to "Review"
        if pd.notna(fruit) and pd.isna(fruit_rating):
            fruit_rating = "Review"
        if pd.notna(vegetable) and pd.isna(vegetable_rating):
            vegetable_rating = "Review"
        if pd.notna(meat) and pd.isna(meat_rating):
            meat_rating = "Review"

        # Add the food and rating to the dictionary
        if pd.notna(fruit):
            foods_dict["fruit"][fruit] = fruit_rating
        if pd.notna(vegetable):
            foods_dict["vegetable"][vegetable] = vegetable_rating
        if pd.notna(meat):
            foods_dict["meat"][meat] = meat_rating

    # Indicate the dictionary does not need building
    st.session_state.build_food_dict = False

    return foods_dict


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

    elif type == "wide":
        # Wide type format is a shorter condensed format
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


# Add a sidebar that allows the user to upload a CSV file
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Ensure all persistent data is reset when a new file is uploaded
    if st.session_state.csv_file_name != uploaded_file.name:
        reset_session_state()
        st.session_state.csv_file_name = uploaded_file.name

    # Read the CSV into a DataFrame
    df = pd.read_csv(uploaded_file)

    with st.expander("**Original CSV Dataframe**"):
        st.dataframe(data=df, use_container_width=True)

    # Build a dictionary from the data in the uploaded CSV
    # Only do this the first time a CSV is loaded
    if st.session_state.build_food_dict:
        st.session_state.foods = build_foods_dict(df)

    # Create a reference to the session state dictionary
    foods = st.session_state.foods

    with st.expander("**Dictionary**"):
        st.write(foods)

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
                                      key="new_food"+str(len(foods[food_type]))) # noqa E501

    if st.button("Add Food"):
        if new_food:
            with select_food_ph.container(border=True):
                with ft_col:
                    st.write(new_food)
                with rt_col:
                    foods[food_type][new_food] = st.radio(new_food,
                                                          ratings,
                                                          index=ratings.index(
                                                            "review"
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
            csv_written, error = write_csv(f"{output_file_prefix}.csv",
                                           dataframe)

    with wf_col:
        # Create a button to save the user's data to a CSV file
        if st.button("Save CSV - Wide Format"):
            dataframe = format_data(type="wide", data=foods)

            # Save the data to a CSV file
            csv_written, error = write_csv(f"{output_file_prefix}.csv",
                                           dataframe)

    if csv_written is not None and csv_written is True:
        csv_output_ph.success(f"Data saved to {output_file_prefix}.csv")
    elif csv_written is not None and csv_written is False:
        csv_output_ph.error(error)
