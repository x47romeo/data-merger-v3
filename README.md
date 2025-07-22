# Data Merger V3 - The Interactive Data Workflow Assistant

🌐 **[Live Demo Available on Streamlit Cloud!](https://your-app-url-here.streamlit.app)**

A revolutionary Streamlit web application that transforms simple file merging into an advanced, interactive data workflow. **Version 3 introduces the power of Polars, interactive transformations, and intelligent multi-format exports!**

## 🚀 Quick Start

### Option 1: Use Online (Recommended)
Visit the live application: **[Data Merger V3 Live App](https://your-app-url-here.streamlit.app)**

### Option 2: Run Locally
```bash
git clone https://github.com/yourusername/data-merger-v3.git
cd data-merger-v3
pip install -r requirements.txt
streamlit run app.py
```

## 🚀 What's New in V3

- **⚡ Polars Engine**: Superior performance and memory efficiency for large datasets
- **🎛️ Interactive Transformation Studio**: Real-time data cleaning, filtering, and column management
- **🔧 Smart Merge Control**: Choose between Inner, Left, and Outer joins with explanations
- **📊 Intelligent Excel Export**: Separate sheets for merged data, unmatched POS, and unmatched Supplier records
- **📤 Multi-Format Export**: Excel (.xlsx), JSON (.json), and Parquet (.parquet) support
- **🔄 Live Data Preview**: See transformations applied in real-time
- **📋 Advanced Filtering**: Multiple filter conditions with various operators

## 🎯 Supported File Formats

| Format | Extensions | Description |
|--------|------------|-------------|
| **CSV** | `.csv` | Comma-separated values |
| **Excel** | `.xlsx`, `.xls` | Microsoft Excel files |
| **TSV** | `.tsv` | Tab-separated values |
| **Text** | `.txt` | Text files with auto-detected separators (`,`, `\t`, `;`, `\|`) |

## Features

- 🎨 **Modern, Professional UI**: Clean design with custom CSS styling
- 📊 **Smart Data Merging**: Handles data type mismatches in UPC columns automatically
- 📝 **Comprehensive Logging**: Tracks all operations and errors in `app_v2.log`
- 🔄 **Real-time Feedback**: Progress indicators and status updates
- 📥 **Easy Download**: One-click download of merged data
- 🛡️ **Error Handling**: Robust error handling with detailed logging
- 🌐 **Multi-Encoding Support**: Handles various text encodings automatically

## 🎯 Interactive Workflow

### Step 1: Upload & Configure Merge
- Upload POS and Supplier files (CSV, Excel, TSV, TXT)
- Select merge type: Inner, Left, or Outer join
- Get clear explanations of each merge type

### Step 2: Interactive Transformation Studio
- **Column Selection**: Choose which columns to include
- **Column Renaming**: Clean up column names (remove suffixes like _right)
- **Data Filtering**: Apply multiple filters with various operators
- **Live Preview**: See changes in real-time

### Step 3: Multi-Format Export
- **Excel Export**: Three sheets (Merged, Unmatched POS, Unmatched Supplier)
- **JSON Export**: Structured data for APIs
- **Parquet Export**: Optimized for analytics

## Requirements

- Python 3.7+
- Streamlit 1.28.0+
- **Polars 0.20.0+** (High-performance data processing)
- Pandas 2.0.0+ (Excel compatibility)
- openpyxl 3.1.0+ (Excel export)
- xlrd 2.0.1+ (Legacy Excel support)

## 🛠️ Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/data-merger-v3.git
   cd data-merger-v3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage Guide

1. **Upload your files**:
   - Upload your POS data file (CSV, Excel, TSV, or TXT with UPC column)
   - Upload your Supplier data file (any supported format with UPC column)
   - The app will automatically detect and display the file format

2. **Configure merge settings**:
   - Select merge type (Inner, Left, or Outer join)
   - Choose your preferred options

3. **Use Interactive Transformation Studio**:
   - Select columns to include
   - Rename columns as needed
   - Apply filters to your data
   - Preview changes in real-time

4. **Export your results**:
   - Choose from Excel, JSON, or Parquet formats
   - Download your processed data

## File Requirements

- Both files must contain a column named **'UPC'**
- Files can be in different formats (e.g., POS.csv + Supplier.xlsx)
- For TXT files, the app will try multiple separators automatically

## Sample Files for Testing

- `sample_pos_data.csv` - CSV format
- `sample_pos_data.tsv` - TSV format  
- `sample_supplier_data.csv` - CSV format
- `sample_supplier_data.txt` - Text format with pipe separators

## Version Comparison

| Feature | V1 (Stable) | V2 (Multi-Format) |
|---------|-------------|-------------------|
| CSV Support | ✅ | ✅ |
| Excel Support | ❌ | ✅ |
| TSV Support | ❌ | ✅ |
| Text File Support | ❌ | ✅ |
| Format Detection | ❌ | ✅ |
| Mixed Format Support | ❌ | ✅ |
| Encoding Handling | ✅ | ✅ |
| Logging | ✅ | ✅ (Enhanced) |

## Technical Details

### Supported Separators for Text Files
- Comma (`,`)
- Tab (`\t`)
- Semicolon (`;`)
- Pipe (`|`)

### Encoding Support
- UTF-8
- Latin-1
- ISO-8859-1
- CP1252 (Windows)

## Troubleshooting

### Common Issues

1. **"Unsupported file format"**
   - Ensure your file has a supported extension (.csv, .xlsx, .xls, .tsv, .txt)

2. **"Could not read Excel file"**
   - Verify the Excel file is not corrupted
   - Try saving as CSV if issues persist

3. **"UPC column not found"**
   - Ensure both files have a column named exactly 'UPC'
   - Check for extra spaces or different capitalization

### Log Files
- V1 logs: `app.log`
- V2 logs: `app_v2.log`

## File Structure

```
Matcher/
├── app.py                    # V1 - Stable CSV-only version
├── app_v1_stable.py         # V1 - Backup copy
├── app_v2.py                # V2 - Multi-format version
├── requirements.txt         # V1 dependencies
├── requirements_v2.txt      # V2 dependencies
├── README.md               # V1 documentation
├── README_V2.md            # V2 documentation (this file)
├── sample_pos_data.csv     # Sample CSV
├── sample_pos_data.tsv     # Sample TSV
├── sample_supplier_data.csv # Sample CSV
├── sample_supplier_data.txt # Sample TXT
├── app.log                 # V1 log file
└── app_v2.log              # V2 log file (created when V2 runs)
```

## 🚀 Deployment

This application is deployed on **Streamlit Community Cloud** for free public access.

### Deploy Your Own Copy

1. **Fork this repository** on GitHub
2. **Sign up** for [Streamlit Community Cloud](https://share.streamlit.io/)
3. **Connect your GitHub account** and select this repository
4. **Deploy** with one click!

### Deployment Requirements
- Public GitHub repository
- `requirements.txt` file (✅ included)
- `app.py` as the main application file (✅ included)
- Streamlit Community Cloud account (free)

## 📊 Live Demo

Try the application online: **[Data Merger V3 Live App](https://your-app-url-here.streamlit.app)**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check this README for usage instructions
- **Live Demo**: Test the application online before local installation
