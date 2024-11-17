import tkinter as tk
from src.HomeUI import HomeUI

def main():
    root = tk.Tk()
    app = HomeUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()