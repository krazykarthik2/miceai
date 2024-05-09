import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


guideline="init"
def is_hex(s):
    """ Check if the string s is a valid hexadecimal of max 2 characters """
    try:
        # Try converting to int, allow only up to two hex digits
        return 0 <= int(s, 16) <= 255 and len(s) <= 2
    except ValueError:
        return False

def validate_hex(P):
    """ Validate that the entry's content is a valid hex or empty (used in validatecommand) """
    return P == "" or is_hex(P)

def close_grace(event=None):
    #closes program gracefully
    reply = messagebox.askyesno("exit?","do you really want to exit???")
    if reply:
        exit(0)
    

def on_submit(event=None):
    """ Function to handle the submit button click """
    # Fetch values from all entries
    values = [entry.get().upper() for entry in entries]
    # Check if all entries are valid
    if all(is_hex(value) for value in values):
        messagebox.showinfo("Success", "All values are valid hex: " + ", ".join(values))
        guideline="success bro"    
    else:
        guideline="All are not valid hex\nEnter only valid hex"

# Create the main window
root = tk.Tk()
root.title("mice ai")
root.iconify()
root.iconbitmap(default="assets/icon.ico")





root.geometry("500x500")
root.config(background='#108cff')

gifImage = "assets/init.gif"
openImage = Image.open(gifImage)
frames = openImage.n_frames
imageObject = [tk.PhotoImage(file=gifImage, format=f"gif -index {i}") for i in range(frames)]
count = 0
showAnimation = None

def animation(count):
    global showAnimation
    newImage = imageObject[count]

    gif_Label.configure(image=newImage)
    count += 1
    if count == frames:
        count = 0
    
    showAnimation = root.after(50, lambda: animation(count))

gif_Label = tk.Label(root, image="")
gif_Label.place(x=0, y=0, width=500, height=500)

animation(count)


root.focus()
input()

# Register a validation command
vcmd = (root.register(validate_hex), '%P')

# Create and place the entry widgets
entries = []
for i in range(4):
    entry = tk.Entry(root, validate="key", validatecommand=vcmd, width=5,border="0",justify='center',background="#565656")
    entry.grid(row=0, column=i, padx=5, pady=5)
    entries.append(entry)
    

entries[0].focus()
root.bind("<Return>", on_submit)
root.bind("<Control-d>",close_grace)
guide = tk.Label(root,text="hi",textvariable="hello")
guide.grid(row=1,columnspan=4)
# Submit button
submit_btn = tk.Button(root, text="Submit", command=on_submit,background="black",foreground="blue",border="0")
submit_btn.grid(row=1, columnspan=4)

# Start the GUI event loop
root.mainloop()
