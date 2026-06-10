import streamlit as st

import task1
import task2
import task3
import task4
import task5
import task6

st.title(
    "Google Play Store Analytics Dashboard"
)

option = st.sidebar.selectbox(

    "Choose task",

    [

        "task 1",

        "task 2",

        "task 3",

        "task 4",

        "task 5",

        "task 6"
    ]
)


if option == "task 1":

    task1.show()

elif option == "task 2":

    task2.show()

elif option == "task 3":

    task3.show()

elif option == "task 4":

    task4.show()

elif option == "task 5":

    task5.show()

elif option == "task 6":

    task6.show()