import tkinter as tk


class GUI:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Input GUI")

        # Add a label to instruct the user
        label = tk.Label(self.root, text="Enter something:")
        label.pack(pady=10)

        # Create an Entry widget to take input
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        # Create a button that gets the input from the Entry widget when clicked
        submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        submit_button.pack(pady=10)


    def on_submit(self):
        user_input = self.entry.get()
        # Do something with the user_input
        print(user_input)










# Start the GUI loop
self.root.mainloop()
