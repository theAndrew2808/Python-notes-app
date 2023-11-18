import tkinter
from tkinter import messagebox
from datetime import datetime
import os
import subprocess
import webbrowser
from tkinter import *
from tkinter import filedialog
import keyboard
from reportlab.pdfgen import canvas

root = Tk()
root.geometry("460x460")
root.title("Notes ")

note_text = Text(root, wrap="word", height=10)

note_scroll = Scrollbar(root, command=note_text.yview)
note_scroll.pack(side=RIGHT, fill=Y)
note_text.config(yscrollcommand=note_scroll.set)

font = "Arial"
rate = 1
scale2 = float(0.0)

new_font_size = 1
new_button_width = 1


def open_note():
    selected_note = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if selected_note:
        with open(os.path.join(os.path.expanduser('~'), 'notes', selected_note), 'r') as f:
            note_contents = f.read()
            note_text.delete("1.0", END)  # Use "1.0" instead of 0 for Text widget
            note_text.insert("1.0", note_contents)



def save_note():
    if note_text.get("1.0", END) != " ":
        filepath = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")])
        if filepath != "":
            text = note_text.get("1.0", END)
            with open(filepath, "w") as file:
                file.write(text)


def print_note():
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if pdf_file:
        if not pdf_file.endswith('.pdf'):
            pdf_file += '.pdf'
        c = canvas.Canvas(pdf_file)
        c.setFont("Helvetica", 12)
        text = note_text.get("1.0", END)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            c.drawString(10, 800 - 20 * i, line)
        c.save()


def copy_content():
    selected_text = note_text.get(SEL_FIRST, SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(selected_text)
    root.update()


def paste_datetime():
    now = datetime.now()
    timestamp = now.strftime("%H:%M %d.%m.%Y")
    note_text.insert(INSERT, timestamp)


def paste_content():
    clipboard_content = root.clipboard_get()
    note_text.insert(INSERT, clipboard_content)


def set_scale(scale):
    global new_font_size, new_button_width, font, scale2
    new_font_size = int(10 * float(scale))
    print(scale, new_font_size, new_button_width)
    scale2 = scale
    note_text.config(font=(f"{font}", new_font_size))
    new_button_width = int(new_font_size * 0.01 - float(scale))


def ask_before_esc():
    mes = tkinter.messagebox.askokcancel(title="Notes Warning",
                                         message="You want to quit notes, would you like to save changes?")
    if mes:
        save_note()
        root.destroy()
    else:
        root.destroy()


def open_help():
    webbrowser.open(
        "https://support.microsoft.com/windows/%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D0%B2-%D0%B1%D0%BB%D0%BE%D0%BA%D0%BD%D0%BE%D1%82%D0%B5-4d68c388-2ff2-0e7f-b706-35fb2ab88a8c")


def send_feedback():
    global rate
    f_root = Tk()
    f_root.title("Feedback")
    f_root.geometry("220x100")

    def feedback_take():
        btn_feedback.destroy()
        btn_feedback_submit.destroy()
        btn_exit_feedback.pack()
        

    def set_feedback(scale):
        global rate
        rate = scale


    btn_exit_feedback = Button(f_root, text=f"Thanks for submitting feedback ({rate} star)!", command=f_root.destroy)
    btn_feedback = Scale(f_root, from_=1, to=5, resolution=1, orient="horizontal",
                         command=set_feedback)
    btn_feedback_submit = Button(f_root, text=f"Submit feedback", command=feedback_take)

    btn_feedback.pack()
    btn_feedback_submit.pack()


def set_font_arial():
    global font, scale2
    font = "Arial"
    print(font)
    set_scale(scale2)


def set_font_calibri():
    global font, scale2
    font = "Calibri"
    print(font)
    set_scale(scale2)


def set_font_consolas():
    global font, scale2
    font = "Consolas"
    print(font)
    set_scale(scale2)


def set_font_system():
    global font, scale2
    font = "System"
    print(font)
    set_scale(scale2)


btn_scale = Scale(root, from_=0, to=2.5, resolution=0.1, orient="horizontal",
                  command=set_scale)

note_text.pack(expand=YES, fill=BOTH)
btn_scale.pack()


def add_font_types():
    font_menu = Menu(menu)
    menu.add_cascade(label="Fonts", menu=font_menu)
    font_menu.add_command(label="Arial (default)", command=set_font_arial)
    font_menu.add_command(label="Calibri", command=set_font_calibri)
    font_menu.add_command(label="Consolas", command=set_font_consolas)
    font_menu.add_command(label="System", command=set_font_system)
    set_font_arial()


menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu, font=new_button_width)
file_menu.add_command(label="Save", command=save_note, font=new_button_width)
file_menu.add_command(label="Open", command=open_note, font=new_font_size)
file_menu.add_command(label="Print", command=print_note, font=new_font_size)

edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_separator()
edit_menu.add_command(label="Paste Date and time", command=paste_datetime)

view_menu = Menu(menu)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Add Font Types", command=add_font_types)

help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Open Help", command=open_help)
help_menu.add_separator()
help_menu.add_command(label="Help us doing Notes better!", command=send_feedback)

keyboard.add_hotkey('ctrl+s', save_note)
keyboard.add_hotkey('ctrl+o', open_note)

keyboard.add_hotkey('ctrl+q', ask_before_esc)
keyboard.add_hotkey('ctrl+z', note_text.edit_undo)
keyboard.add_hotkey('ctrl+y', note_text.edit_redo)

keyboard.add_hotkey('ctrl+alt+q', root.withdraw)
keyboard.add_hotkey('ctrl+alt+r', root.deiconify)

keyboard.add_hotkey('ctrl+c', copy_content)
note_text.bind('<Control-v>', paste_content)

root.mainloop()
