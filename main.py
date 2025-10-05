#author Anjana main.py
import os, warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from gui import AppGUI

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
