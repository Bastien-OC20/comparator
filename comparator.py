"""Excel file comparison module."""

import pandas as pd


def compare_excel_files(file1, file2, sheet_name=0):
    """
    Compare two Excel files and return a summary of differences.
    
    Args:
        file1: First Excel file (path or file-like object)
        file2: Second Excel file (path or file-like object)
        sheet_name: Sheet name or index to compare (default: 0 for first sheet)
    
    Returns:
        dict containing:
            - column_diff: Dictionary with columns only in each file
            - value_diff: DataFrame with rows that have different values
            - summary: Summary statistics of differences
    """
    df1 = pd.read_excel(file1, sheet_name=sheet_name)
    df2 = pd.read_excel(file2, sheet_name=sheet_name)
    
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    
    column_diff = {
        "only_in_file1": list(cols1 - cols2),
        "only_in_file2": list(cols2 - cols1),
        "common": list(cols1 & cols2)
    }
    
    common_cols = column_diff["common"]
    
    if not common_cols:
        return {
            "column_diff": column_diff,
            "value_diff": pd.DataFrame(),
            "summary": {
                "total_rows_file1": len(df1),
                "total_rows_file2": len(df2),
                "rows_with_differences": 0,
                "columns_only_in_file1": len(column_diff["only_in_file1"]),
                "columns_only_in_file2": len(column_diff["only_in_file2"]),
            }
        }
    
    df1_common = df1[common_cols].reset_index(drop=True)
    df2_common = df2[common_cols].reset_index(drop=True)
    
    max_rows = max(len(df1_common), len(df2_common))
    df1_common = df1_common.reindex(range(max_rows))
    df2_common = df2_common.reindex(range(max_rows))
    
    differences = []
    for idx in range(max_rows):
        for col in common_cols:
            val1 = df1_common.at[idx, col] if idx < len(df1) else None
            val2 = df2_common.at[idx, col] if idx < len(df2) else None
            
            val1_is_nan = pd.isna(val1)
            val2_is_nan = pd.isna(val2)
            
            if val1_is_nan and val2_is_nan:
                continue
            if val1_is_nan != val2_is_nan or val1 != val2:
                differences.append({
                    "Row": idx + 1,
                    "Column": col,
                    "File 1 Value": val1,
                    "File 2 Value": val2
                })
    
    value_diff = pd.DataFrame(differences)
    
    summary = {
        "total_rows_file1": len(df1),
        "total_rows_file2": len(df2),
        "rows_with_differences": len(set(d["Row"] for d in differences)) if differences else 0,
        "total_cell_differences": len(differences),
        "columns_only_in_file1": len(column_diff["only_in_file1"]),
        "columns_only_in_file2": len(column_diff["only_in_file2"]),
    }
    
    return {
        "column_diff": column_diff,
        "value_diff": value_diff,
        "summary": summary
    }
