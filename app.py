
import streamlit as st
import pandas as pd
import os

st.title("Student Record Management System")

file = "students.csv"

# Load existing records
if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["ID", "Name", "Age", "Course", "Marks"])

# Menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add New Student")

    id = st.number_input("Student ID", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Add Student"):
        if name and course:
            if id not in df["ID"].values:
                new_student = pd.DataFrame([{
                    "ID": id,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                df = pd.concat([df, new_student], ignore_index=True)
                df.to_csv(file, index=False)

                st.success("Student Added Successfully!")
            else:
                st.error("Student ID already exists")
        else:
            st.warning("Please enter Name and Course")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No student records found")

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Record")

    if not df.empty:
        student_id = st.selectbox("Select Student ID", df["ID"])

        student = df[df["ID"] == student_id].iloc[0]

        name = st.text_input("Name", student["Name"])
        age = st.number_input("Age", value=int(student["Age"]))
        course = st.text_input("Course", student["Course"])
        marks = st.number_input("Marks", value=int(student["Marks"]))

        if st.button("Update Record"):
            df.loc[df["ID"] == student_id, "Name"] = name
            df.loc[df["ID"] == student_id, "Age"] = age
            df.loc[df["ID"] == student_id, "Course"] = course
            df.loc[df["ID"] == student_id, "Marks"] = marks

            df.to_csv(file, index=False)

            st.success("Student Updated Successfully!")
            st.rerun()
    else:
        st.info("No records available")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    if not df.empty:
        student_id = st.selectbox("Select Student ID", df["ID"])

        if st.button("Delete Student"):
            df = df[df["ID"] != student_id]

            df.to_csv(file, index=False)

            st.success("Student Deleted Successfully!")
            st.rerun()
    else:
        st.info("No records available")
