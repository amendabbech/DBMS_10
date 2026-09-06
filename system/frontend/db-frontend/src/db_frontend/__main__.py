import tkinter as tk
from db_frontend import api
from db_frontend.connection_dialog import ConnectionDialog
from db_frontend.ui import App


def main():
    root = tk.Tk()
    root.withdraw()

    dialog = ConnectionDialog(root)
    if not dialog.confirmed:
        root.destroy()
        return

    api.BASE_URL = dialog.url
    api.HEADERS = {"X-API-Key": dialog.key}

    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
