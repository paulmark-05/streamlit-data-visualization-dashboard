# 📊 WRICEF Data Visualization Dashboard

A comprehensive Python-based data visualization solution for analyzing WRICEF (Workflow, Report, Interface, Conversion, Enhancement, Form) tracker data with interactive dashboards and advanced analytics.

## 🌟 Features

### 📈 Static Visualizations
- **WRICEF Type Distribution**: Bar charts showing distribution of different WRICEF types
- **Implementation vs Complexity Heatmaps**: Correlation analysis between implementations and complexity levels
- **Effort Analysis**: Forecast vs Actual effort comparison with scatter plots
- **Timeline Analysis**: Monthly and quarterly delivery trends
- **Priority Distribution**: Pie charts showing priority breakdowns
- **Stage Progress**: Development stage distribution analysis

### 🚀 Interactive Dashboards
- **Real-time Filtering**: Filter by Implementation, WRICEF Type, Complexity, Priority, and Date Range
- **3D Visualizations**: 3D scatter plots for multi-dimensional effort analysis
- **Interactive Timeline**: Plotly-based timeline with hover details
- **Sunburst Charts**: Hierarchical view of Implementation → WRICEF Type → Complexity
- **Treemap Visualizations**: Proportional representation of data distributions
- **Correlation Heatmaps**: Interactive correlation analysis

### 💡 Analytics Features
- **Key Insights Generation**: Automated insights and statistics
- **Effort Efficiency Analysis**: Forecast vs Actual effort tracking
- **Data Quality Metrics**: Missing data analysis and quality indicators
- **Export Capabilities**: Save visualizations as PNG and HTML files

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install Required Packages

```bash
# Option 1: Install from requirements.txt
pip install -r requirements.txt

# Option 2: Install packages individually
pip install pandas numpy matplotlib seaborn plotly streamlit openpyxl
```

### Step 2: Verify Installation

```python
# Test script to verify all packages are installed correctly
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

print("✅ All packages installed successfully!")
```

## 🚀 How to Run the Programs

### Method 1: Command Line Static Analysis

```bash
# Run the main visualization script
python wricef_visualizer.py
```

**What this does:**
- Loads your WRICEF data from `WRICEF-Tracker-dump.xlsx`
- Generates comprehensive static visualizations
- Saves plots as high-quality PNG files
- Creates interactive HTML files
- Displays key insights in the console
- Shows all plots in matplotlib windows

**Output Files:**
- `wricef_distribution.png`
- `complexity_heatmap.png`
- `effort_analysis.png`
- `time_series.png`
- `timeline_interactive.html`
- `effort_3d_interactive.html`
- `sunburst_interactive.html`
- `treemap_interactive.html`

### Method 2: Interactive Web Dashboard

```bash
# Launch the Streamlit web application
streamlit run streamlit_dashboard.py
```

**What this does:**
- Opens a web browser with an interactive dashboard
- Provides real-time filtering and data exploration
- Offers multiple analysis pages
- Allows file upload for your own data
- Includes responsive design for different screen sizes

**Dashboard Features:**
1. **Data Overview**: Basic statistics and data preview
2. **Distribution Analysis**: Interactive charts for data distributions
3. **Effort Analysis**: Comprehensive effort tracking and analysis
4. **Timeline Analysis**: Interactive timeline visualizations
5. **Advanced Analytics**: 3D plots, sunburst charts, and treemaps
6. **Correlation Analysis**: Heatmaps and correlation matrices
7. **Key Insights**: Automated insights and recommendations

## 📁 File Structure

```
project/
├── wricef_visualizer.py          # Main static visualization script
├── streamlit_dashboard.py        # Interactive web dashboard
├── requirements.txt              # Python package dependencies
├── WRICEF-Tracker-dump.xlsx     # Your data file (place here)
└── output/                       # Generated visualizations
    ├── *.png                     # Static plot images
    └── *.html                    # Interactive HTML plots
```

## 📊 Data Format Requirements

Your Excel file should contain these key columns:
- `Implementation`: Project implementation name
- `WRICEF Type`: W, R, I, C, E, or F
- `Complexity`: Low, Medium, High, Very High
- `Priority of Delivery`: Priority levels
- `Stage`: Development stage
- `ABAP Effort Forecast (hrs)`: Estimated ABAP effort
- `ABAP Actual Effort (hrs)`: Actual ABAP effort
- `PI Effort Forecast (hrs)`: Estimated PI effort
- `PI Actual Effort (hrs)`: Actual PI effort
- `FSD Planned Del Date`: Planned delivery date
- `Dev Actual Delivery Date`: Actual delivery date

**Note:** If your data doesn't match exactly, the program will work with available columns and create sample data for missing fields.

## 🎨 Customization Options

### Modifying Visualizations

1. **Change Color Schemes**: Edit the color palettes in the scripts
```python
# In wricef_visualizer.py, modify color schemes
colors = plt.cm.Set3(np.linspace(0, 1, len(data)))  # Change Set3 to other colormaps
```

2. **Add New Chart Types**: Extend the `create_dashboard_plots()` method
```python
# Add your custom visualization
def create_custom_plot(self):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Your custom plotting code here
    return fig
```

3. **Modify Dashboard Layout**: Edit the Streamlit dashboard layout
```python
# In streamlit_dashboard.py
col1, col2, col3 = st.columns([2, 1, 1])  # Adjust column ratios
```

### Adding New Analysis Pages

1. Create a new method in `StreamlitWRICEFDashboard` class
2. Add the page to the navigation selectbox
3. Include the method call in the main display logic

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing packages
```bash
pip install [missing_package_name]
```

2. **File Not Found Error**: Ensure your Excel file is named correctly and in the same directory
```bash
# Check if file exists
ls -la WRICEF-Tracker-dump.xlsx
```

3. **Streamlit Not Opening**: Check if the port is available
```bash
streamlit run streamlit_dashboard.py --server.port 8502
```

4. **Memory Issues with Large Files**: Reduce data size or increase system memory
```python
# Sample large datasets
df_sample = df.sample(n=1000)  # Use smaller sample
```

### Performance Optimization

1. **For Large Datasets** (>10,000 rows):
   - Use data sampling: `df.sample(n=5000)`
   - Enable Streamlit caching: `@st.cache_data`
   - Process data in chunks

2. **For Slow Visualizations**:
   - Reduce plot complexity
   - Use smaller figure sizes
   - Disable animations in Plotly

## 📈 Advanced Usage

### Batch Processing Multiple Files

```python
import glob

# Process multiple Excel files
files = glob.glob("*.xlsx")
for file in files:
    visualizer = WRICEFDataVisualizer(file)
    plots = visualizer.create_dashboard_plots()
    # Save with file-specific names
```

### Custom Analysis Scripts

```python
# Create custom analysis
from wricef_visualizer import WRICEFDataVisualizer

visualizer = WRICEFDataVisualizer('your_data.xlsx')
df = visualizer.df

# Your custom analysis code
custom_analysis = df.groupby('Implementation')['ABAP Effort Forecast (hrs)'].sum()
print(custom_analysis)
```

### Export Options

```python
# Export filtered data
filtered_data = df[df['Implementation'] == 'EWM']
filtered_data.to_excel('ewm_analysis.xlsx', index=False)

# Export visualizations with custom settings
fig.savefig('custom_plot.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
```

## 🤝 Contributing

To extend this visualization suite:

1. Fork the repository
2. Add new visualization methods
3. Update the dashboard with new features
4. Test with sample data
5. Submit improvements

## 📝 License

This project is open source and available for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your data format matches requirements
4. Test with sample data first

---

**🎉 Happy Data Visualization!** 

This comprehensive toolkit provides everything needed to analyze and visualize your WRICEF tracker data with professional-quality charts and interactive dashboards.