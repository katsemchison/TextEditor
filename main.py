import tkinter as tk
from tkinter import END, messagebox
from tkinter.filedialog import askopenfile, asksaveasfile
import hashlib


class TextEditor:
    def __init__(self, master):

        # set up title as well as default starting directory
        self.title = "Simple Text Editor"
        self.master = master
        self.master.title(self.title)
        self.file_name = "c:\\users"

        # create widgets, a menu and the text box to edit the text in
        # changed the command to close the window with X button here as well to keep it with the close option in menu
        self.menu = tk.Menu(master)
        self.menu.add_command(label="Open", command=self.open_file)
        self.menu.add_command(label="Save", command=self.save)
        self.menu.add_command(label="Close", command=self.close)
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.config(menu=self.menu)

        self.text = tk.Text(master)
        self.text.pack()

        # set first signature here to compare text against in the future to prevent unwanted loss of data
        self.signature = self.get_signature(self.text.get(1.0, END))

    def get_signature(self, contents):
        # get the hash of the current text to see if any changes have been made
        return hashlib.md5(contents.encode('utf-8')).digest()

    def open_file_dialog(self):
        # create a dialog box to open a file, use the last used directory stored in filename
        file = askopenfile(initialdir=self.file_name,
                           filetypes=[("Text File", "*.txt")],
                           title="Choose a text document")
        if file:
            # if the user has selected a file, change the stored directory, delete what's in the current text field
            # add the new data without any filler white space, change the signature to the new data and move
            # the cursor to the end of the document. I also decided to change the title here to reflect the new document
            self.file_name = file.name
            self.text.delete(1.0, END)
            self.text.insert(END, file.read().strip())
            self.signature = self.get_signature(self.text.get(1.0, END))
            self.text.mark_set("insert", END)
            self.master.title(f'{self.title} - {self.file_name.split("/")[-1]}')

    def open_file(self):
        # to open a new file, first check if there are any changes to the current document to prevent loss of data
        # then if they do decide to open a new document anyway, open the file dialog
        if self.get_signature(self.text.get(1.0, END)) != self.signature:
            response = messagebox.askokcancel("Overwrite data?",
                                              "Your data will be overwritten, would you like to continue?")
            if response:
                self.open_file_dialog()
        else:
            self.open_file_dialog()

    def save(self):
        # open the file location using the stored directory, if it already has .txt on the end, then just save it to
        # the location, otherwise add it on so that it's readable in the future
        file_location = asksaveasfile(initialdir=self.file_name,
                                      filetypes=[("Text File", "*.txt")],
                                      title="Choose where to save")
        if file_location:
            if file_location.name[-4:] != ".txt":
                self.file_name = file_location.name + ".txt"
            else:
                self.file_name = file_location.name

            # take all of the contents from the document and save them to the chosen file
            contents = self.text.get(1.0, END)
            with open(self.file_name, "w") as file:
                file.write(str(contents))

            # reset the signature after saving
            self.signature = self.get_signature(contents)

    def close(self):
        # if the close button or the x button are clicked, check if any unsaved changes have been made and prompt
        # if needed
        if self.get_signature(self.text.get(1.0, END)) == self.signature:
            self.master.destroy()
        else:
            if messagebox.askokcancel("Attention", "Close without saving changes?"):
                self.master.destroy()


# set the window size as well as get the app running
window_size = "400x400+400+400"
root = tk.Tk()
editor = TextEditor(root)
root.geometry(window_size)
root.resizable(False, False)
root.mainloop()
