import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader for multiple files
files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:  # ✅ Corrected variable name
    for file in files:
        ext = file.name.split(".")[-1]  # ✅ Use "." instead of ","

        # Read the file correctly
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")  # ✅ Add engine="openpyxl"

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())  # ✅ No syntax error


        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

            if st.checkbox(f"Fill Missing Values - {file.name}"):
                df= fillno (df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.success("Missing Values filled with mean")
                st.dataframe(df.head())

            selected_columns = st.multiselect(f"select columns - {file.name}", df.columns , default=df.columns)
            df=df(selected_columns)
            st.dataframe(df.head())

            if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include="number").empty:
               st.bar_chart(df.select_dtypes(includes="number").iloc[:,:2]) 

            format_choise = st.radio(f"convert {file.name} to:" , ["CSV" , "Excel"], key=file.name)  

            if st.button(f"Download {file.name} as {format_choise}"):
                output = BytesIO()
                if format_choise == "CSV":
                    df.to_CSV ("output, index=False")
                    mine ="text/csv"
                    new_name = file.name.replace(ext, "csv")

                else : 
                    df.to_excel(output, index=False, engine="openpyxl") 
                    mine= "application/vnd.openxmlformat.officedocument.spreadsheetml.sheet"
                    new_name=file.name.replace(ext, "xlsx")

                output.seek(0)
                st.set_download_button(new_name, data=output, minetype=mine) 

            st.success("Processing Complete!")  