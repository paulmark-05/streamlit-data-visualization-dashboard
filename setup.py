#!/usr/bin/env python3
"""
WRICEF Data Visualization Setup Script
This script helps you set up and run the WRICEF data visualization tools
"""

import sys
import subprocess
import importlib
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]} (Compatible)")
    return True

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_packages():
    """Check and install required packages"""
    required_packages = {
        'pandas': 'pandas>=1.5.0',
        'numpy': 'numpy>=1.21.0',
        'matplotlib': 'matplotlib>=3.5.0',
        'seaborn': 'seaborn>=0.11.0',
        'plotly': 'plotly>=5.0.0',
        'streamlit': 'streamlit>=1.25.0',
        'openpyxl': 'openpyxl>=3.0.9'
    }
    
    print("\n🔧 Checking required packages...")
    missing_packages = []
    
    for package, version in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {package} - Already installed")
        except ImportError:
            print(f"❌ {package} - Not found")
            missing_packages.append(version)
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                return False
    
    print("✅ All required packages are installed!")
    return True

def create_sample_files():
    """Create sample configuration files if they don't exist"""
    files_to_create = {
        'config.py': '''# Configuration file for WRICEF Data Visualization

# File paths
DATA_FILE = "WRICEF-Tracker-dump.xlsx"
OUTPUT_DIR = "output"

# Visualization settings
FIGURE_SIZE = (12, 8)
DPI = 300
COLOR_PALETTE = "husl"

# Streamlit settings
PAGE_TITLE = "WRICEF Analytics Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Sample data settings
SAMPLE_RECORDS = 500
RANDOM_SEED = 42
''',
        
        'run_dashboard.bat': '''@echo off
echo Starting WRICEF Data Visualization Dashboard...
streamlit run streamlit_dashboard.py
pause
''',
        
        'run_analysis.bat': '''@echo off
echo Running WRICEF Data Analysis...
python wricef_visualizer.py
pause
''',
        
        'run_quick_start.bat': '''@echo off
echo Running Quick Start Example...
python quick_start_example.py
pause
'''
    }
    
    print("\n📁 Creating configuration files...")
    for filename, content in files_to_create.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        else:
            print(f"ℹ️  {filename} already exists")

def check_files():
    """Check if required Python files exist"""
    required_files = [
        'wricef_visualizer.py',
        'streamlit_dashboard.py',
        'quick_start_example.py',
        'requirements.txt'
    ]
    
    print("\n📄 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        print("Please ensure all required Python files are in the current directory")
        return False
    
    return True

def create_output_directory():
    """Create output directory for generated files"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created {output_dir} directory")
    else:
        print(f"ℹ️  {output_dir} directory already exists")

def display_usage_instructions():
    """Display usage instructions"""
    instructions = """
🎉 Setup Complete! Here's how to use the WRICEF Data Visualization tools:

📊 OPTION 1: Quick Start Example (Recommended for first-time users)
   Command: python quick_start_example.py
   
   What it does:
   • Creates sample data automatically
   • Generates basic visualizations
   • Saves PNG and HTML files
   • Perfect for testing the setup

📈 OPTION 2: Full Analysis Script
   Command: python wricef_visualizer.py
   
   What it does:
   • Processes your actual Excel data
   • Creates comprehensive static visualizations
   • Generates interactive HTML plots
   • Provides detailed insights

🚀 OPTION 3: Interactive Web Dashboard (Most feature-rich)
   Command: streamlit run streamlit_dashboard.py
   
   What it does:
   • Opens a web-based dashboard
   • Real-time filtering and exploration
   • Upload your own Excel files
   • Multiple analysis pages

📁 FILE REQUIREMENTS:
   • Place your Excel file as: WRICEF-Tracker-dump.xlsx
   • Or use the file upload feature in the web dashboard
   • The tools work with sample data if no file is found

🎨 CUSTOMIZATION:
   • Edit the Python files to customize visualizations
   • Modify config.py for settings
   • Use the .bat files on Windows for easy execution

🔧 TROUBLESHOOTING:
   • Run this setup script again if you encounter issues
   • Check the README.md file for detailed instructions
   • Ensure your data follows the expected Excel format

💡 TIPS:
   • Start with the Quick Start Example to verify everything works
   • Use the Web Dashboard for interactive exploration
   • Check the output/ directory for generated files
   """
    
    print(instructions)

def main():
    """Main setup function"""
    print("🚀 WRICEF Data Visualization Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required files
    if not check_files():
        return False
    
    # Install required packages
    if not check_and_install_packages():
        return False
    
    # Create additional files
    create_sample_files()
    create_output_directory()
    
    # Display usage instructions
    display_usage_instructions()
    
    print("\n✅ Setup completed successfully!")
    
    # Ask if user wants to run quick start
    response = input("\n🤔 Would you like to run the Quick Start Example now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("\n🚀 Running Quick Start Example...")
        try:
            import quick_start_example
        except Exception as e:
            print(f"❌ Error running quick start: {e}")
            print("You can run it manually: python quick_start_example.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("Please check the error message and try again")
    
    input("\nPress Enter to exit...")