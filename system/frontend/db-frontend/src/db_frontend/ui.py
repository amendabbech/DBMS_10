import tkinter as tk
from tkinter import ttk, messagebox
from db_frontend import api


class App(tk.Toplevel):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.title("Blutspende-Verwaltung")
        self.geometry("750x550")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.spender_tab = SpenderTab(notebook)
        self.zentrum_tab = ZentrumTab(notebook)
        self.spende_tab = SpendeTab(notebook)

        notebook.add(self.spender_tab, text="Spender")
        notebook.add(self.zentrum_tab, text="Spendezentrum")
        notebook.add(self.spende_tab, text="Spende")


class SpenderTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._daten = []
        self._build_ui()
        self._load()

    def _build_ui(self):
        toolbar = tk.Frame(self, pady=6)
        toolbar.pack(fill=tk.X, padx=12)
        tk.Button(toolbar, text="Aktualisieren", command=self._load).pack(side=tk.LEFT)

        listenframe = tk.Frame(self)
        listenframe.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        scrollbar = tk.Scrollbar(listenframe)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste = tk.Listbox(listenframe, font=("Courier", 10),
                                 yscrollcommand=scrollbar.set)
        self.liste.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.liste.yview)

        form = tk.LabelFrame(self, text="Neuen Spender anlegen", padx=10, pady=8)
        form.pack(fill=tk.X, padx=12, pady=8)
        felder = [("Vorname", "vorname"), ("Nachname", "nachname"),
                  ("Geburtsdatum (YYYY-MM-DD)", "geburtsdatum"),
                  ("Blutgruppe", "blutgruppe"), ("Email", "email")]
        self._eingaben = {}
        for i, (label, key) in enumerate(felder):
            tk.Label(form, text=label + ":").grid(
                row=i // 2, column=(i % 2) * 2, sticky=tk.E, padx=6, pady=3)
            entry = tk.Entry(form, width=28)
            entry.grid(row=i // 2, column=(i % 2) * 2 + 1, sticky=tk.W, pady=3)
            self._eingaben[key] = entry
        tk.Button(form, text="Anlegen", command=self._create).grid(
            row=3, column=0, columnspan=4, pady=6)

    def _load(self):
        try:
            self._daten = api.alle_spender()
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        self.liste.delete(0, tk.END)
        for s in self._daten:
            zeile = f"{s['spender_id']:>4} {s['nachname']:<15} {s['vorname']:<15} {s['geburtsdatum']:<12} {s['blutgruppe']:<4} {s['email']}"
            self.liste.insert(tk.END, zeile)

    def _create(self):
        werte = {k: e.get().strip() for k, e in self._eingaben.items()}
        if not all(werte.values()):
            messagebox.showwarning("Eingabe", "Alle Felder ausfuellen.")
            return
        try:
            api.spender_create(**werte)
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        for e in self._eingaben.values():
            e.delete(0, tk.END)
        self._load()


class ZentrumTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._daten = []
        self._build_ui()
        self._load()

    def _build_ui(self):
        toolbar = tk.Frame(self, pady=6)
        toolbar.pack(fill=tk.X, padx=12)
        tk.Button(toolbar, text="Aktualisieren", command=self._load).pack(side=tk.LEFT)

        listenframe = tk.Frame(self)
        listenframe.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        scrollbar = tk.Scrollbar(listenframe)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste = tk.Listbox(listenframe, font=("Courier", 10),
                                 yscrollcommand=scrollbar.set)
        self.liste.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.liste.yview)

        form = tk.LabelFrame(self, text="Neues Spendezentrum anlegen", padx=10, pady=8)
        form.pack(fill=tk.X, padx=12, pady=8)
        felder = [("Name", "name"), ("Adresse", "adresse"), ("Stadt", "stadt")]
        self._eingaben = {}
        for i, (label, key) in enumerate(felder):
            tk.Label(form, text=label + ":").grid(row=i, column=0, sticky=tk.E, padx=6, pady=3)
            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1, sticky=tk.W, pady=3)
            self._eingaben[key] = entry
        tk.Button(form, text="Anlegen", command=self._create).grid(
            row=3, column=0, columnspan=2, pady=6)

    def _load(self):
        try:
            self._daten = api.alle_zentren()
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        self.liste.delete(0, tk.END)
        for z in self._daten:
            zeile = f"{z['zentrum_id']:>4} {z['name']:<20} {z['stadt']:<15} {z['adresse']}"
            self.liste.insert(tk.END, zeile)

    def _create(self):
        werte = {k: e.get().strip() for k, e in self._eingaben.items()}
        if not all(werte.values()):
            messagebox.showwarning("Eingabe", "Alle Felder ausfuellen.")
            return
        try:
            api.zentrum_create(**werte)
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        for e in self._eingaben.values():
            e.delete(0, tk.END)
        self._load()


class SpendeTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._daten = []
        self._build_ui()
        self._load()

    def _build_ui(self):
        toolbar = tk.Frame(self, pady=6)
        toolbar.pack(fill=tk.X, padx=12)
        tk.Button(toolbar, text="Aktualisieren", command=self._load).pack(side=tk.LEFT)

        listenframe = tk.Frame(self)
        listenframe.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        scrollbar = tk.Scrollbar(listenframe)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste = tk.Listbox(listenframe, font=("Courier", 10),
                                 yscrollcommand=scrollbar.set)
        self.liste.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.liste.yview)

        form = tk.LabelFrame(self, text="Neue Spende anlegen", padx=10, pady=8)
        form.pack(fill=tk.X, padx=12, pady=8)
        felder = [("Spender-ID", "spender_id"), ("Zentrum-ID", "zentrum_id"),
                  ("Datum (YYYY-MM-DD)", "spende_datum"), ("Menge (ml)", "menge_ml")]
        self._eingaben = {}
        for i, (label, key) in enumerate(felder):
            tk.Label(form, text=label + ":").grid(
                row=i // 2, column=(i % 2) * 2, sticky=tk.E, padx=6, pady=3)
            entry = tk.Entry(form, width=20)
            entry.grid(row=i // 2, column=(i % 2) * 2 + 1, sticky=tk.W, pady=3)
            self._eingaben[key] = entry
        tk.Button(form, text="Anlegen", command=self._create).grid(
            row=2, column=0, columnspan=4, pady=6)

    def _load(self):
        try:
            self._daten = api.alle_spenden()
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        self.liste.delete(0, tk.END)
        for s in self._daten:
            zeile = f"{s['spende_id']:>4} Spender:{s['spender_id']:<4} Zentrum:{s['zentrum_id']:<4} {s['spende_datum']:<12} {s['menge_ml']}ml"
            self.liste.insert(tk.END, zeile)

    def _create(self):
        werte = {k: e.get().strip() for k, e in self._eingaben.items()}
        if not all(werte.values()):
            messagebox.showwarning("Eingabe", "Alle Felder ausfuellen.")
            return
        try:
            api.spende_create(
                spender_id=int(werte["spender_id"]),
                zentrum_id=int(werte["zentrum_id"]),
                spende_datum=werte["spende_datum"],
                menge_ml=int(werte["menge_ml"]),
            )
        except Exception as exc:
            messagebox.showerror("Fehler", str(exc))
            return
        for e in self._eingaben.values():
            e.delete(0, tk.END)
        self._load()
