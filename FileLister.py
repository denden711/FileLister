import os
import glob
from tkinter import Tk, simpledialog
from tkinter.filedialog import askdirectory
from tkinter import messagebox  # メッセージボックスをインポート

def select_folder():
    root = Tk()
    root.withdraw()
    folder_selected = askdirectory()
    root.destroy()
    return folder_selected

def get_user_input(root, prompt):
    input_value = simpledialog.askstring("Input", prompt, parent=root)
    return input_value.strip() if input_value else None

def find_files(folder, extension):
    search_pattern = f'*.{extension}' if extension.startswith('.') else f'*.{extension}'
    return glob.glob(os.path.join(folder, search_pattern))

def write_filenames_to_txt(files, output_file):
    with open(output_file, 'w') as file:
        for filename in files:
            file.write(f"{os.path.splitext(os.path.basename(filename))[0]}\n")

def main():
    try:
        folder = select_folder()
        if not folder:
            messagebox.showerror("Error", "No folder selected. Exiting.")
            return

        root = Tk()
        root.withdraw()
        extension = get_user_input(root, "Enter the file extension (include the dot, e.g., .txt):")
        if not extension:
            messagebox.showerror("Error", "No extension provided. Exiting.")
            return

        output_directory = os.path.join(os.getcwd(), "filelister_output")
        os.makedirs(output_directory, exist_ok=True)

        output_filename = get_user_input(root, "Enter the output file name:")
        if not output_filename:
            messagebox.showerror("Error", "No output file name provided. Exiting.")
            return

        if not output_filename.endswith('.txt'):
            output_filename += '.txt'  # Ensure the output file is a .txt file

        files = find_files(folder, extension)
        if not files:
            messagebox.showinfo("Information", "No files found with the given extension.")
            return

        output_path = os.path.join(output_directory, output_filename)
        write_filenames_to_txt(files, output_path)
        messagebox.showinfo("Success", f"File names are written to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if 'root' in locals():
            root.destroy()

if __name__ == '__main__':
    main()
