"""Streamlit application for comparing Excel files."""

import pandas as pd
import streamlit as st

from comparator import compare_excel_files


st.set_page_config(
    page_title="Excel File Comparator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel File Comparator")
st.markdown("Upload two Excel files to compare their contents and see the differences.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("File 1")
    file1 = st.file_uploader("Upload first Excel file", type=["xlsx", "xls"], key="file1")

with col2:
    st.subheader("File 2")
    file2 = st.file_uploader("Upload second Excel file", type=["xlsx", "xls"], key="file2")

if file1 and file2:
    try:
        result = compare_excel_files(file1, file2)
        
        st.header("📈 Summary")
        summary = result["summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows in File 1", summary["total_rows_file1"])
        with col2:
            st.metric("Rows in File 2", summary["total_rows_file2"])
        with col3:
            st.metric("Rows with Differences", summary["rows_with_differences"])
        with col4:
            st.metric("Cell Differences", summary["total_cell_differences"])
        
        st.header("📋 Column Differences")
        column_diff = result["column_diff"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Only in File 1")
            if column_diff["only_in_file1"]:
                for col in column_diff["only_in_file1"]:
                    st.write(f"• {col}")
            else:
                st.write("None")
        
        with col2:
            st.subheader("Only in File 2")
            if column_diff["only_in_file2"]:
                for col in column_diff["only_in_file2"]:
                    st.write(f"• {col}")
            else:
                st.write("None")
        
        with col3:
            st.subheader("Common Columns")
            if column_diff["common"]:
                for col in column_diff["common"]:
                    st.write(f"• {col}")
            else:
                st.write("None")
        
        st.header("🔍 Value Differences")
        value_diff = result["value_diff"]
        
        if not value_diff.empty:
            st.dataframe(value_diff, use_container_width=True)
        else:
            st.success("No value differences found in common columns!")
            
    except pd.errors.EmptyDataError:
        st.error("One or both files are empty. Please upload valid Excel files with data.")
    except ValueError as e:
        st.error(f"Invalid file format or structure: {e!s}")
    except Exception as e:
        st.error(f"Error comparing files: {e!s}")
else:
    st.info("Please upload both Excel files to start the comparison.")
