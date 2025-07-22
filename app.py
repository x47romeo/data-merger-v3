"""
Data Merger V3 - The Interactive Data Workflow Assistant
A Streamlit application for advanced data merging, transformation, and export.
Supports multiple file formats with interactive data cleaning and multi-format export.
VERSION: 3.0 - INTERACTIVE WORKFLOW WITH POLARS
"""

import streamlit as st
import polars as pl
import pandas as pd
import logging
import json
from io import BytesIO, StringIO

# Configure logging
def setup_logging():
    """Configure logging to write to app.log file with INFO level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

def apply_custom_css():
    """Apply custom CSS for modern, professional styling."""
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding-top: 2rem;
    }

    /* Title styling */
    .main-title {
        text-align: center;
        color: #0047AB;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }

    /* Step indicators */
    .step-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Instructions styling */
    .instructions {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0047AB;
        margin-bottom: 2rem;
    }
    
    /* File upload sections */
    .upload-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 2px solid #f0f2f6;
        transition: border-color 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #0047AB;
    }
    
    /* Success message styling */
    .success-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FFA500 0%, #ff8c00 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,165,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,165,0,0.4);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76,175,80,0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76,175,80,0.4);
    }
    
    /* Data preview styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Transformation studio styling */
    .transform-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
    }

    /* Format info styling */
    .format-info {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
        font-size: 0.9rem;
    }

    /* Workflow step styling */
    .workflow-step {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

def detect_file_format(file):
    """Detect file format based on file extension."""
    if file is None:
        return 'unknown'

    filename = file.name.lower()

    if filename.endswith('.csv'):
        return 'csv'
    elif filename.endswith(('.xlsx', '.xls')):
        return 'excel'
    elif filename.endswith('.tsv'):
        return 'tsv'
    elif filename.endswith('.txt'):
        return 'txt'
    else:
        return 'unknown'

def read_file_with_polars(file, file_format):
    """
    Read file with Polars for superior performance.
    Enhanced error handling for all file formats.

    Args:
        file: Uploaded file object
        file_format: Detected file format

    Returns:
        polars.DataFrame: Loaded data
    """
    try:
        file.seek(0)  # Always reset file pointer

        if file_format == 'excel':
            # For Excel files, use multiple approaches
            try:
                # First try with openpyxl engine
                df_pandas = pd.read_excel(file, engine='openpyxl')
                logger.info("Excel file read successfully with openpyxl engine")
            except Exception as e1:
                try:
                    # Reset and try with xlrd engine for older files
                    file.seek(0)
                    df_pandas = pd.read_excel(file, engine='xlrd')
                    logger.info("Excel file read successfully with xlrd engine")
                except Exception as e2:
                    # Reset and try without specifying engine
                    file.seek(0)
                    df_pandas = pd.read_excel(file)
                    logger.info("Excel file read successfully with default engine")

            # Convert to Polars
            return pl.from_pandas(df_pandas)

        elif file_format == 'csv':
            # Try multiple encoding approaches for CSV
            encodings = ['utf-8', 'utf-8-lossy', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    file.seek(0)
                    df = pl.read_csv(file, encoding=encoding, ignore_errors=True)
                    logger.info(f"CSV file read successfully with {encoding} encoding")
                    return df
                except Exception:
                    continue

            # If all encodings fail, try with pandas then convert
            file.seek(0)
            df_pandas = pd.read_csv(file, encoding='utf-8', errors='replace')
            return pl.from_pandas(df_pandas)

        elif file_format == 'tsv':
            # Try multiple encoding approaches for TSV
            encodings = ['utf-8', 'utf-8-lossy', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    file.seek(0)
                    df = pl.read_csv(file, separator='\t', encoding=encoding, ignore_errors=True)
                    logger.info(f"TSV file read successfully with {encoding} encoding")
                    return df
                except Exception:
                    continue

            # If all encodings fail, try with pandas then convert
            file.seek(0)
            df_pandas = pd.read_csv(file, sep='\t', encoding='utf-8', errors='replace')
            return pl.from_pandas(df_pandas)

        elif file_format == 'txt':
            # Try different separators and encodings for text files
            separators = [',', '\t', ';', '|']
            encodings = ['utf-8', 'utf-8-lossy', 'latin-1', 'cp1252']

            for sep in separators:
                for encoding in encodings:
                    try:
                        file.seek(0)
                        df = pl.read_csv(file, separator=sep, encoding=encoding, ignore_errors=True)
                        if len(df.columns) > 1:  # Valid separator found
                            logger.info(f"TXT file read successfully with '{sep}' separator and {encoding} encoding")
                            return df
                    except Exception:
                        continue

            # If all combinations fail, try with pandas
            file.seek(0)
            content = file.read().decode('utf-8', errors='replace')
            for sep in separators:
                try:
                    df_pandas = pd.read_csv(StringIO(content), sep=sep)
                    if len(df_pandas.columns) > 1:
                        logger.info(f"TXT file read successfully with pandas using '{sep}' separator")
                        return pl.from_pandas(df_pandas)
                except Exception:
                    continue

            raise ValueError("Could not determine separator for TXT file")

        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    except Exception as e:
        logger.error(f"Error reading {file_format} file: {str(e)}")
        raise ValueError(f"Could not read {file_format.upper()} file: {str(e)}")

def perform_simple_merge(pos_df, supplier_df):
    """
    Perform simple merge: Find all UPCs from POS sheet and match them in Supplier sheet.
    This is essentially an inner join - only matching UPCs are included.

    Args:
        pos_df: POS Polars DataFrame
        supplier_df: Supplier Polars DataFrame

    Returns:
        tuple: (merged_df, unmatched_pos, unmatched_supplier)
    """
    try:
        # Validate input DataFrames
        if pos_df.is_empty():
            raise ValueError("POS DataFrame is empty")
        if supplier_df.is_empty():
            raise ValueError("Supplier DataFrame is empty")

        # Check for UPC column existence
        if "UPC" not in pos_df.columns:
            raise ValueError("UPC column not found in POS data")
        if "UPC" not in supplier_df.columns:
            raise ValueError("UPC column not found in Supplier data")

        # Convert UPC columns to string type for accurate matching
        # Handle potential null values
        pos_df = pos_df.with_columns(
            pl.col("UPC").cast(pl.Utf8).fill_null("MISSING_UPC")
        )
        supplier_df = supplier_df.with_columns(
            pl.col("UPC").cast(pl.Utf8).fill_null("MISSING_UPC")
        )

        logger.info("Performing simple merge: Finding POS UPCs in Supplier data")
        logger.info(f"POS data: {pos_df.shape[0]} rows, Supplier data: {supplier_df.shape[0]} rows")

        # Perform inner join - only keep records where UPC exists in both files
        merged_df = pos_df.join(supplier_df, on="UPC", how="inner")

        # Calculate unmatched records
        if not merged_df.is_empty():
            merged_upcs = set(merged_df["UPC"].to_list())
            unmatched_pos = pos_df.filter(~pl.col("UPC").is_in(merged_upcs))
            unmatched_supplier = supplier_df.filter(~pl.col("UPC").is_in(merged_upcs))
        else:
            # No matches found
            unmatched_pos = pos_df
            unmatched_supplier = supplier_df

        logger.info(f"Merge completed: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
        logger.info(f"Unmatched POS: {unmatched_pos.shape[0]} rows, Unmatched Supplier: {unmatched_supplier.shape[0]} rows")

        return merged_df, unmatched_pos, unmatched_supplier

    except Exception as e:
        logger.error(f"Error during merge: {str(e)}")
        raise ValueError(f"Merge failed: {str(e)}")

def create_excel_with_sheets(merged_df, unmatched_pos, unmatched_supplier):
    """
    Create Excel file with three sheets using openpyxl.
    Enhanced error handling and data validation.

    Returns:
        BytesIO: Excel file in memory
    """
    try:
        output = BytesIO()

        # Convert Polars DataFrames to Pandas for Excel export
        # Handle empty DataFrames gracefully
        try:
            merged_pandas = merged_df.to_pandas() if not merged_df.is_empty() else pd.DataFrame()
        except Exception:
            merged_pandas = pd.DataFrame()

        try:
            unmatched_pos_pandas = unmatched_pos.to_pandas() if not unmatched_pos.is_empty() else pd.DataFrame()
        except Exception:
            unmatched_pos_pandas = pd.DataFrame()

        try:
            unmatched_supplier_pandas = unmatched_supplier.to_pandas() if not unmatched_supplier.is_empty() else pd.DataFrame()
        except Exception:
            unmatched_supplier_pandas = pd.DataFrame()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Write merged data
            if not merged_pandas.empty:
                merged_pandas.to_excel(writer, sheet_name='Merged Data', index=False)
            else:
                empty_df = pd.DataFrame({'Message': ['No merged data available']})
                empty_df.to_excel(writer, sheet_name='Merged Data', index=False)

            # Write unmatched POS data
            if not unmatched_pos_pandas.empty:
                unmatched_pos_pandas.to_excel(writer, sheet_name='Unmatched from POS', index=False)
            else:
                empty_df = pd.DataFrame({'Message': ['No unmatched POS records']})
                empty_df.to_excel(writer, sheet_name='Unmatched from POS', index=False)

            # Write unmatched Supplier data
            if not unmatched_supplier_pandas.empty:
                unmatched_supplier_pandas.to_excel(writer, sheet_name='Unmatched from Supplier', index=False)
            else:
                empty_df = pd.DataFrame({'Message': ['No unmatched Supplier records']})
                empty_df.to_excel(writer, sheet_name='Unmatched from Supplier', index=False)

        output.seek(0)
        logger.info("Excel file with multiple sheets created successfully")
        return output

    except Exception as e:
        logger.error(f"Error creating Excel file: {str(e)}")
        raise ValueError(f"Failed to create Excel file: {str(e)}")

def main():
    """Main application function."""
    # Page configuration MUST be the first Streamlit command
    st.set_page_config(
        page_title="Data Merger V3 - Interactive Workflow",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Log application start
    logger.info("Data Merger V3 session started.")

    # Apply custom styling
    apply_custom_css()

    # Main title and subtitle
    st.markdown('<h1 class="main-title">🔄 Data Merger V3</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">The Interactive Data Workflow Assistant - Transform, Clean, and Export with Ease!</p>', unsafe_allow_html=True)
    
    # Workflow overview
    st.markdown("""
    <div class="instructions">
        <h3>🎯 Interactive Data Workflow:</h3>
        <p><strong>Step 1:</strong> Upload Files → <strong>Step 2:</strong> Transform & Clean → <strong>Step 3:</strong> Export</p>
        <br>
        <p><strong>🔍 How it works:</strong> Upload your POS and Supplier files. The app will find all UPCs from your POS data and match them with corresponding records in your Supplier data.</p>
        <br>
        <p><strong>🚀 V3 Features:</strong></p>
        <ul>
            <li><strong>Polars Engine:</strong> Superior performance for large datasets</li>
            <li><strong>Interactive Transformations:</strong> Real-time data cleaning and filtering</li>
            <li><strong>Smart Excel Export:</strong> Separate sheets for matched and unmatched data</li>
            <li><strong>Multiple Export Formats:</strong> Excel, JSON, Parquet support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Step 1: Upload & Configure Merge
    st.markdown('<div class="step-indicator">📁 Step 1: Upload Files & Configure Merge</div>', unsafe_allow_html=True)

    with st.container():
        # File upload section
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="upload-section">', unsafe_allow_html=True)
            st.subheader("📁 Upload POS File")
            pos_file = st.file_uploader(
                "Choose POS data file",
                type=['csv', 'xlsx', 'xls', 'tsv', 'txt'],
                key="pos_uploader",
                help="Upload your POS data file containing UPC column"
            )
            if pos_file:
                file_format = detect_file_format(pos_file)
                st.success(f"✅ Uploaded: {pos_file.name}")
                st.info(f"📄 Format: {file_format.upper()}")
                logger.info(f"POS file uploaded: {pos_file.name} (format: {file_format})")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="upload-section">', unsafe_allow_html=True)
            st.subheader("📁 Upload Supplier File")
            supplier_file = st.file_uploader(
                "Choose Supplier data file",
                type=['csv', 'xlsx', 'xls', 'tsv', 'txt'],
                key="supplier_uploader",
                help="Upload your Supplier data file containing UPC column"
            )
            if supplier_file:
                file_format = detect_file_format(supplier_file)
                st.success(f"✅ Uploaded: {supplier_file.name}")
                st.info(f"📄 Format: {file_format.upper()}")
                logger.info(f"Supplier file uploaded: {supplier_file.name} (format: {file_format})")
            st.markdown('</div>', unsafe_allow_html=True)

        # Simple merge explanation
        if pos_file and supplier_file:
            st.markdown("---")
            st.subheader("🔧 Ready to Merge")

            st.info("ℹ️ **Merge Process**: The app will find all UPCs from your POS file and match them with corresponding records in the Supplier file. Only matching UPCs will be included in the final merged data.")

            # Merge button
            col_center = st.columns([1, 2, 1])[1]
            with col_center:
                if st.button("🔄 Perform Merge", use_container_width=True, type="primary"):
                    with st.spinner("Processing files and performing merge..."):
                        try:
                            # Read files with enhanced error handling
                            st.info("📖 Reading POS file...")
                            pos_format = detect_file_format(pos_file)
                            pos_df = read_file_with_polars(pos_file, pos_format)

                            st.info("📖 Reading Supplier file...")
                            supplier_format = detect_file_format(supplier_file)
                            supplier_df = read_file_with_polars(supplier_file, supplier_format)

                            # Validate data
                            if pos_df.is_empty():
                                st.error("❌ POS file appears to be empty or could not be read properly")
                                st.stop()
                            if supplier_df.is_empty():
                                st.error("❌ Supplier file appears to be empty or could not be read properly")
                                st.stop()

                            # Display file info
                            st.success(f"✅ POS file loaded: {pos_df.shape[0]} rows, {pos_df.shape[1]} columns")
                            st.success(f"✅ Supplier file loaded: {supplier_df.shape[0]} rows, {supplier_df.shape[1]} columns")

                            # Check for UPC column
                            if 'UPC' not in pos_df.columns:
                                st.error(f"❌ UPC column not found in POS file. Available columns: {', '.join(pos_df.columns)}")
                                st.stop()
                            if 'UPC' not in supplier_df.columns:
                                st.error(f"❌ UPC column not found in Supplier file. Available columns: {', '.join(supplier_df.columns)}")
                                st.stop()

                            st.info("🔄 Performing merge: Finding POS UPCs in Supplier data...")

                            # Perform simple merge
                            merged_df, unmatched_pos, unmatched_supplier = perform_simple_merge(pos_df, supplier_df)

                            # Validate merge results
                            if merged_df.is_empty():
                                st.warning("⚠️ Merge resulted in no matching records. You may want to check your UPC values.")

                            # Store in session state
                            st.session_state['merged_df'] = merged_df
                            st.session_state['unmatched_pos'] = unmatched_pos
                            st.session_state['unmatched_supplier'] = unmatched_supplier
                            st.session_state['original_columns'] = merged_df.columns
                            st.session_state['merge_success'] = True

                            # Display results
                            st.success("✅ Merge completed successfully!")
                            st.info(f"📊 Results: {merged_df.shape[0]} merged rows, {unmatched_pos.shape[0]} unmatched POS, {unmatched_supplier.shape[0]} unmatched Supplier")
                            logger.info(f"Merge successful: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")

                        except Exception as e:
                            error_msg = str(e)
                            st.error(f"❌ Merge failed: {error_msg}")

                            # Provide helpful suggestions based on error type
                            if "UPC" in error_msg:
                                st.info("💡 **Tip**: Make sure both files have a column named exactly 'UPC' (case-sensitive)")
                            elif "Excel" in error_msg or "xlsx" in error_msg:
                                st.info("💡 **Tip**: Try saving your Excel file as CSV format if the issue persists")
                            elif "encoding" in error_msg.lower():
                                st.info("💡 **Tip**: Try saving your file with UTF-8 encoding")

                            logger.error(f"Merge failed: {error_msg}")
        else:
            st.info("📤 Please upload both files and configure merge settings to continue")

    # Step 2: Transformation Studio
    if st.session_state.get('merge_success', False) and 'merged_df' in st.session_state:
        st.markdown('<div class="step-indicator">🔧 Step 2: Interactive Transformation Studio</div>', unsafe_allow_html=True)

        merged_df = st.session_state['merged_df']

        with st.expander("🎛️ Data Transformation Controls", expanded=True):
            # Live data preview
            st.subheader("📊 Live Data Preview")

            # Column selection
            st.subheader("📋 Column Selection")
            available_columns = merged_df.columns
            selected_columns = st.multiselect(
                "Select columns to include in final export:",
                options=available_columns,
                default=available_columns,
                help="Deselect columns you want to exclude from the final export"
            )

            if selected_columns:
                # Apply column selection
                working_df = merged_df.select(selected_columns)

                # Column renaming
                st.subheader("✏️ Column Renaming")
                rename_columns = {}

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original Names**")
                with col2:
                    st.write("**New Names**")

                for col in selected_columns:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text(col)
                    with col2:
                        new_name = st.text_input(f"Rename {col}", value=col, key=f"rename_{col}")
                        if new_name != col:
                            rename_columns[col] = new_name

                # Apply renaming
                if rename_columns:
                    working_df = working_df.rename(rename_columns)
                    logger.info(f"Columns renamed: {rename_columns}")

                # Data filtering
                st.subheader("🔍 Data Filtering")

                # Initialize filters in session state
                if 'filters' not in st.session_state:
                    st.session_state['filters'] = []

                # Add filter button
                if st.button("➕ Add Filter"):
                    st.session_state['filters'].append({
                        'column': selected_columns[0] if selected_columns else '',
                        'operator': 'equals',
                        'value': ''
                    })

                # Display and manage filters
                filters_to_remove = []
                for i, filter_config in enumerate(st.session_state['filters']):
                    col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                    with col1:
                        filter_config['column'] = st.selectbox(
                            "Column",
                            options=selected_columns,
                            index=selected_columns.index(filter_config['column']) if filter_config['column'] in selected_columns else 0,
                            key=f"filter_col_{i}"
                        )

                    with col2:
                        filter_config['operator'] = st.selectbox(
                            "Operator",
                            options=['equals', 'not equals', 'contains', 'greater than', 'less than'],
                            key=f"filter_op_{i}"
                        )

                    with col3:
                        filter_config['value'] = st.text_input(
                            "Value",
                            value=filter_config['value'],
                            key=f"filter_val_{i}"
                        )

                    with col4:
                        if st.button("🗑️", key=f"remove_filter_{i}"):
                            filters_to_remove.append(i)

                # Remove filters
                for i in reversed(filters_to_remove):
                    st.session_state['filters'].pop(i)

                # Apply filters
                for filter_config in st.session_state['filters']:
                    if filter_config['value']:
                        try:
                            col_name = filter_config['column']
                            operator = filter_config['operator']
                            value = filter_config['value']

                            if operator == 'equals':
                                working_df = working_df.filter(pl.col(col_name).cast(pl.Utf8) == value)
                            elif operator == 'not equals':
                                working_df = working_df.filter(pl.col(col_name).cast(pl.Utf8) != value)
                            elif operator == 'contains':
                                working_df = working_df.filter(pl.col(col_name).cast(pl.Utf8).str.contains(value))
                            elif operator == 'greater than':
                                working_df = working_df.filter(pl.col(col_name) > float(value))
                            elif operator == 'less than':
                                working_df = working_df.filter(pl.col(col_name) < float(value))
                        except Exception as e:
                            st.warning(f"Filter error for {col_name}: {str(e)}")

                # Display current data
                st.dataframe(working_df.to_pandas().head(10), use_container_width=True)
                st.info(f"📊 Current data: {working_df.shape[0]} rows, {working_df.shape[1]} columns")

                # Store working dataframe
                st.session_state['working_df'] = working_df
            else:
                st.warning("Please select at least one column to continue.")

        # Step 3: Export
        if 'working_df' in st.session_state:
            st.markdown('<div class="step-indicator">📤 Step 3: Multi-Format Export</div>', unsafe_allow_html=True)

            working_df = st.session_state['working_df']

            # Export format selection
            export_format = st.radio(
                "Choose export format:",
                options=['Excel (.xlsx)', 'JSON (.json)', 'Parquet (.parquet)'],
                help="Select the format for your final export"
            )

            # Generate export file
            if st.button("📥 Generate Export File", type="primary", use_container_width=True):
                with st.spinner("Generating export file..."):
                    try:
                        if export_format == 'Excel (.xlsx)':
                            # Create Excel with multiple sheets
                            excel_file = create_excel_with_sheets(
                                working_df,
                                st.session_state['unmatched_pos'],
                                st.session_state['unmatched_supplier']
                            )

                            st.download_button(
                                label="📥 Download Excel File",
                                data=excel_file.getvalue(),
                                file_name="Data_Merger_V3_Export.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                            logger.info("Excel export generated successfully")

                        elif export_format == 'JSON (.json)':
                            json_data = working_df.to_pandas().to_json(orient='records', indent=2)

                            st.download_button(
                                label="📥 Download JSON File",
                                data=json_data,
                                file_name="Data_Merger_V3_Export.json",
                                mime="application/json",
                                use_container_width=True
                            )
                            logger.info("JSON export generated successfully")

                        elif export_format == 'Parquet (.parquet)':
                            parquet_buffer = BytesIO()
                            working_df.write_parquet(parquet_buffer)

                            st.download_button(
                                label="📥 Download Parquet File",
                                data=parquet_buffer.getvalue(),
                                file_name="Data_Merger_V3_Export.parquet",
                                mime="application/octet-stream",
                                use_container_width=True
                            )
                            logger.info("Parquet export generated successfully")

                        st.success("✅ Export file generated successfully!")

                    except Exception as e:
                        st.error(f"❌ Export failed: {str(e)}")
                        logger.error(f"Export failed: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application failed to start: {str(e)}")
        logger.error(f"Application startup error: {str(e)}")
        st.stop()
