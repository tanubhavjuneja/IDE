import customtkinter as ctk
import subprocess
from PIL import Image
import sys
from tkinter import filedialog
import os
import threading
import pyperclip
execution_thread = None
def run_code():
    global execution_thread
    code = code_text.get(1.0, ctk.END)
    if execution_thread and execution_thread.is_alive():
        execution_thread.join()
    execution_thread = threading.Thread(target=execute_code, args=(code,))
    execution_thread.start()
def execute_code(code):
    process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    output_text.delete(1.0, ctk.END)
    output_text.insert(ctk.END, output)
    if error:
        output_text.insert(ctk.END, error)
def close():
    if execution_thread and execution_thread.is_alive():
        execution_thread.join()
    root.destroy()
    sys.exit()
def create_new_file():
    file_directory = "C:/Users/Tanubhav Juneja/Desktop/__pycache__/"
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    file_path = os.path.join(file_directory, "new_file.py")
    with open(file_path, 'w') as new_file:
        new_file.write("")
    save_file()
def open_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, 'r') as opened_file:
            code_text.delete(1.0, ctk.END)
            code_text.insert(ctk.END, opened_file.read())
        current_file = file_path
def save_file():
    global current_file
    code = code_text.get(1.0, ctk.END).strip()
    if code:
        if current_file:
            with open(current_file, 'w') as file:
                file.write(code)
        else:
            save_file_as()
def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file_path:
        global current_file
        current_file = file_path
        save_file()
mfl="C:/Users/Tanubhav Juneja/Desktop/projects/IDE/"
close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(20, 20))
run_icon=ctk.CTkImage(Image.open(mfl+"icons/play.png"), size=(20, 20))
save_icon=ctk.CTkImage(Image.open(mfl+"icons/save.png"), size=(20, 20))
new_file_icon=ctk.CTkImage(Image.open(mfl+"icons/tab.png"), size=(20, 20))
open_icon=ctk.CTkImage(Image.open(mfl+"icons/open.png"), size=(20, 20))
ide_icon=ctk.CTkImage(Image.open(mfl+"icons/ide.png"), size=(30, 30))
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.attributes('-fullscreen', True)
root.title("Python IDE")
bgcc="gray14"
name_label=ctk.CTkLabel(root,image=ide_icon,text="",font=("Arial",20,"bold"))
name_label.place(relx=0.004,rely=0.004)
main_bar=ctk.CTkFrame(root, bg_color=bgcc,fg_color=bgcc)
run_button = ctk.CTkButton(main_bar,image=run_icon, text="",width=1,fg_color=bgcc,bg_color=bgcc, command=run_code)
run_button.pack(side="left", padx=2, pady=2)
new_file_button = ctk.CTkButton(main_bar, image=new_file_icon, text="",width=1,fg_color=bgcc,bg_color=bgcc, command=create_new_file)
new_file_button.pack(side="left", padx=2, pady=2)
open_file_button = ctk.CTkButton(main_bar, image=open_icon, text="",width=1,fg_color=bgcc,bg_color=bgcc, command=open_file)
open_file_button.pack(side="left", padx=2, pady=2)
save_button = ctk.CTkButton(main_bar,image=save_icon, text="",width=1,fg_color=bgcc,bg_color=bgcc, command=save_file)
save_button.pack(side="left", padx=2, pady=2)
close_button = ctk.CTkButton(main_bar, image=close_icon,fg_color=bgcc,bg_color=bgcc, command=close,text="",width=1)
close_button.pack(side="left", padx=2, pady=2)
main_bar.place(rely=0,relx=0.895)
class CustomText(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyPress-Return>", self.handle_enter)
        self.bind("<KeyPress-BackSpace>", self.handle_backspace)
        self.bind("<KeyPress>", self.handle_bracket)
        self.bind("<Control-c>", self.handle_copy)
        self.bind("<Control-v>", self.handle_paste)
        self.bind("<Control-x>", self.handle_cut)
    def handle_copy(self, event):
        selected_text = self.get("sel.first", "sel.last")
        pyperclip.copy(selected_text)
    def handle_paste(self, event):
        clipboard_text = pyperclip.paste()
        self.insert("insert", clipboard_text)
    def handle_cut(self, event):
        selected_text = self.get("sel.first", "sel.last")
        self.clipboard_clear()
        self.clipboard_append(selected_text)
        self.delete("sel.first", "sel.last")
    def handle_enter(self, event):
        current_line = self.get("insert linestart", "insert")
        next_line = self.get("insert", "insert lineend + 1 line")
        indentation = ""
        for char in current_line:
            if char == " " or char == "\t":
                indentation += char
            else:
                break
        if next_line.strip() != "":
            self.mark_set("insert", "insert lineend")
            self.insert("insert", "\n" + indentation)
            return "break"
        closing_brackets = [")", "]", "}", "\"", "'"]
        closing_bracket_count = sum(char in closing_brackets for char in current_line)
        closing_quote_count = sum(current_line.count(quote) for quote in closing_brackets[3:])
        closing_count = closing_bracket_count + closing_quote_count
        self.mark_set("insert", f"insert+{closing_count}c")
        if current_line.strip().endswith(":"):
            indentation += "    "
        self.insert("insert", "\n" + indentation)
        self.mark_set("insert", "insert lineend")
        self.highlight_syntax()
        return "break"
    def highlight_syntax(self):
        code = self.get("1.0", "end")
        self.tag_remove("comment", "1.0", "end")
        lines = code.split("\n")
        for i, line in enumerate(lines):
            line = line.rstrip()
            if line.startswith("#"):
                start_pos = f"{i + 1}.0"
                end_pos = f"{i + 1}.end"
                self.tag_add("comment", start_pos, end_pos)
                self.tag_config("comment", foreground="green")
            elif "#" in line:
                command, comment = line.split("#", 1)
                command = command.rstrip()
                comment = comment.lstrip()
                if command:
                    command_end = line.index(command) + len(command)
                    start_pos = f"{i + 1}.{command_end}"
                    end_pos = f"{i + 1}.end"
                    self.tag_add("comment", start_pos, end_pos)
                    self.tag_config("comment", foreground="green")
    def handle_backspace(self, event):
        current_line = self.get("insert linestart", "insert")
        if current_line.strip() == "" and current_line.endswith("    "):
            self.delete("insert-4c", "insert")
            return "break"
        return
    def handle_bracket(self, event):
        bracket_pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
            "\"": "\"",
            "'": "'"
        }
        bracket = event.char
        if bracket in bracket_pairs:
            closing_bracket = bracket_pairs[bracket]
            self.insert("insert", bracket + closing_bracket)
            self.mark_set("insert", f"insert-1c")
            return "break"
code_text = CustomText(root, height=650, width=1900, fg_color="gray10", bg_color="gray10", font=("Arial", 15))
code_text.tag_config("comment", foreground="green")
code_text.pack(pady=50)
output_label=ctk.CTkLabel(root,text="Output",font=("Arial",20,"bold"))
output_label.place(rely=0.66,relx=0.02)
output_text = ctk.CTkTextbox(root, height=310, width=1900)
output_text.place(rely=0.7, x=10)
current_file = None
root.mainloop()
