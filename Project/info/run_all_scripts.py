#!/usr/bin/env python3
"""
Script Runner for Trading Project
This script runs all Python files in the current directory sequentially.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import importlib.util
import shutil

def get_python_files():
    """Get all Python files in the current directory, excluding this script."""
    current_dir = Path('.')
    python_files = []
    
    # Define the specific order for trading scripts
    script_order = [
        'Skins.py',
        'skins_weekly_history.py', 
        'Skins_mwv.py',
        'skins_history_indicators.py',
        'skins_offers.py',
        'target_creation.py'
    ]
    
    # First, add files in the specified order
    for script_name in script_order:
        script_path = current_dir / script_name
        if script_path.exists():
            python_files.append(script_path)
    
    # Then add any remaining Python files (excluding runner scripts)
    exclude_files = {'run_all_scripts.py', 'run_scripts_auto.py'}
    for file in current_dir.glob('*.py'):
        if (file.name not in exclude_files and 
            file.name not in script_order):
            python_files.append(file)
    
    return python_files

def run_script_with_subprocess(script_path, output_folder):
    """Run a Python script using subprocess."""
    try:
        print(f"\n{'='*60}")
        print(f"Running: {script_path.name}")
        print(f"{'='*60}")
        
        # Set environment variable for output folder
        env = os.environ.copy()
        env['OUTPUT_FOLDER'] = str(output_folder)
        
        # Run the script
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, 
                              text=True, 
                              timeout=300,  # 5 minute timeout
                              env=env)
        
        if result.returncode == 0:
            print(f"✅ {script_path.name} completed successfully!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print(f"❌ {script_path.name} failed with return code {result.returncode}")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
            if result.stdout:
                print("Standard output:")
                print(result.stdout)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_path.name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running {script_path.name}: {str(e)}")
        return False

def run_script_with_import(script_path, output_folder):
    """Run a Python script by importing it as a module."""
    try:
        print(f"\n{'='*60}")
        print(f"Running: {script_path.name}")
        print(f"{'='*60}")
        
        # Set environment variable for output folder
        os.environ['OUTPUT_FOLDER'] = str(output_folder)
        
        # Load and run the script
        spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
        module = importlib.util.module_from_spec(spec)
        
        # Execute the module
        spec.loader.exec_module(module)
        
        print(f"✅ {script_path.name} completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running {script_path.name}: {str(e)}")
        return False

def main():
    """Main function to run all Python scripts."""
    print("🚀 Starting Trading Project Script Runner")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Use a single consistent output folder
    output_folder = Path("trading_results")
    output_folder.mkdir(exist_ok=True)
    
    print(f"📂 Using output folder: {output_folder}")
    
    # Get all Python files
    python_files = get_python_files()
    
    if not python_files:
        print("❌ No Python files found in the current directory")
        return
    
    print(f"\n📋 Found {len(python_files)} Python files to run:")
    for i, file in enumerate(python_files, 1):
        print(f"  {i}. {file.name}")
    
    # Ask user for confirmation
    response = input(f"\n🤔 Do you want to run all {len(python_files)} scripts? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("❌ Operation cancelled by user")
        return
    
    # Ask user for execution method
    print("\n🔧 Choose execution method:")
    print("1. Subprocess (recommended - isolated execution)")
    print("2. Import (faster but may have dependency conflicts)")
    
    method_choice = input("Enter choice (1 or 2): ").strip()
    
    if method_choice == "2":
        run_method = run_script_with_import
        print("📦 Using import method")
    else:
        run_method = run_script_with_subprocess
        print("🔀 Using subprocess method")
    
    # Run all scripts
    successful_runs = 0
    failed_runs = 0
    
    start_time = time.time()
    
    for i, script_file in enumerate(python_files, 1):
        print(f"\n📊 Progress: {i}/{len(python_files)}")
        
        success = run_method(script_file, output_folder)
        
        if success:
            successful_runs += 1
        else:
            failed_runs += 1
        
        # Small delay between scripts
        if i < len(python_files):
            print("⏳ Waiting 2 seconds before next script...")
            time.sleep(2)
    
    # Move any Excel files created in current directory to output folder
    print(f"\n📁 Moving Excel files to output folder...")
    excel_files_moved = 0
    for excel_file in Path('.').glob('*.xlsx'):
        if excel_file.name.startswith('~$'):  # Skip temporary Excel files
            continue
        try:
            shutil.move(str(excel_file), str(output_folder / excel_file.name))
            print(f"  ✅ Moved: {excel_file.name}")
            excel_files_moved += 1
        except Exception as e:
            print(f"  ❌ Failed to move {excel_file.name}: {e}")
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful runs: {successful_runs}")
    print(f"❌ Failed runs: {failed_runs}")
    print(f"📈 Success rate: {(successful_runs/len(python_files)*100):.1f}%")
    print(f"⏱️  Total execution time: {total_time:.2f} seconds")
    print(f"📁 Excel files moved: {excel_files_moved}")
    
    if failed_runs > 0:
        print(f"\n⚠️  {failed_runs} script(s) failed. Check the error messages above.")
    else:
        print(f"\n🎉 All scripts completed successfully!")
    
    print(f"\n📂 All results saved in: {output_folder}")
    print(f"📁 Check the generated Excel files in the output folder.")

if __name__ == "__main__":
    main() 