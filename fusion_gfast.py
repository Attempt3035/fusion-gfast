import tkinter as tk
from tkinter import filedialog


def modify_gcode(file_path):
    gcode_state = {"G": None}
    modified_lines = []
    lines_to_check = []  # Store lines temporarily for checking conditions

    with open(file_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        original_line = line  # Keep the original line for later use
        line = line.split(";", 1)[0].strip()
        if not line:
            modified_lines.append(original_line)
            continue
        words = line.split()

        # Modify G-code state before processing Z5 modifications
        for word in words:
            if word.startswith("G"):
                gcode_state["G"] = word[1:]

        # Check if the current line meets the Z5 condition
        if "Z5" in words and i + 1 < len(lines):
            next_line = lines[i + 1].split(";", 1)[0].strip()
            next_line_words = next_line.split()
            # Check if the next line contains only X and Y words
            if len(next_line_words) == 2 and all(
                w.startswith("X") or w.startswith("Y") for w in next_line_words
            ):
                # Check and replace or insert G0 as needed
                if any(word.startswith("G") for word in words):
                    words = ["G0" if word.startswith("G") else word for word in words]
                else:
                    words.insert(0, "G0")
                lines_to_check.append(i + 2)  # Mark the next line of interest

        # For the line after the X and Y positions line, if necessary
        if i in lines_to_check and not any(w.startswith("G") for w in words):
            words.insert(0, f'G{gcode_state["G"]}')

        modified_line = " ".join(words) + "\n"
        modified_lines.append(modified_line)

    # Write the modified lines to a new file
    output_file_path = (
        file_path.rsplit(".", 1)[0] + "-gfast." + file_path.rsplit(".", 1)[1]
    )
    with open(output_file_path, "w") as file:
        file.writelines(modified_lines)
    print(f"Modified file saved as: {output_file_path}")


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("G-code files", "*.gcode *.nc *.txt"),
            ("All files", "*.*"),
        ]
    )
    if file_path:
        modify_gcode(file_path)
    else:
        print("No file selected.")


# Run the dialog
open_file_dialog()
