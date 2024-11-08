import subprocess
import shutil
import os
import glob

def run_command(command):
    """Runs a command and checks if it was successful."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error: Command failed with error code {result.returncode}")
        exit(result.returncode)
    return result

def delete_directory(directory):
    """Deletes a directory if it exists."""
    if os.path.exists(directory):
        print(f"Deleting {directory}...")
        shutil.rmtree(directory)
        print(f"Deleted {directory}")
    else:
        print(f"{directory} does not exist.")

def copy_files(src, dest):
    """Copies files from src to dest."""
    if os.path.isdir(src):
        print(f"Copying files from {src} to {dest}...")
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(f"Copied files from {src} to {dest}.")
    elif os.path.isfile(src):
        print(f"Copying file from {src} to {dest}...")
        shutil.copy(src, dest)
        print(f"Copied file from {src} to {dest}.")
    else:
        print(f"{src} does not exist.")

def main():
    # Step 1: Delete the existing CoffeeManagement directory if it exists
    coffee_management_dir = os.path.join(os.getcwd(), "CoffeeManagement")
    delete_directory(coffee_management_dir)

    # Step 2: Run mvn javafx:jlink
    try:
        run_command("mvn javafx:jlink")
    except Exception as e:
        print(f"Error during Maven build: {e}")
        exit(1)

    # Step 3: Run jpackage to create the application image
    try:
        run_command("jpackage --type app-image -n CoffeeManagement --runtime-image target/coffeemanagement --module com.group13.coffeemanagement/com.group13.coffeemanagement.App")
    except Exception as e:
        print(f"Error during jpackage: {e}")
        exit(1)

    # Step 4: Create the CoffeeManagement/app directory if it doesn't exist
    app_dir = os.path.join(coffee_management_dir, "app")
    os.makedirs(app_dir, exist_ok=True)

    # Step 5: Copy target/classes to CoffeeManagement/app/
    target_classes_dir = os.path.join(os.getcwd(), "target", "classes")
    if os.path.exists(target_classes_dir):
        copy_files(target_classes_dir, app_dir)

    # Step 6: Copy images folder to CoffeeManagement/
    images_dir = os.path.join(os.getcwd(), "images")
    if os.path.exists(images_dir):
        copy_files(images_dir, os.path.join(coffee_management_dir, "images"))

    # Step 7: Copy all JSON files from the root to CoffeeManagement/
    json_files = glob.glob(os.path.join(os.getcwd(), "*.json"))
    for json_file in json_files:
        copy_files(json_file, coffee_management_dir)

    print("Build and copy process completed successfully.")

if __name__ == "__main__":
    main()