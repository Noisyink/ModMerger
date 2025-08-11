#Written by Noisy - It's probably clunky and bigger than it needs to be
#I ain't no coder, fool

# Import required modules
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from bs4 import BeautifulSoup
import webbrowser
import os 
import sys

def get_resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename

# Define the main application class
class ModMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASOT Mod Merger")
        self.root.geometry("600x600")
        self.root.resizable(True, True)

        try:
            self.root.iconbitmap(get_resource_path("logo.ico"))
        except Exception as e:
            print(f"Icon load failed: {e}")

        self.optional_mods = []
        self.check_vars = []
        self.mission_html = None

        self.init_ui()

    def init_ui(self):
        # Frame for icon and title
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)

        # Title label
        tk.Label(
            title_frame,
            text="ASOT Mod Merger",
            font=("Arial", 16, "bold"),
            justify="left"
        ).pack(side="left")

        # Usage instructions
        tk.Label(
            self.root,
            text="Step 1: Load optional mods HTML\nStep 2: Select mods\nStep 3: Load mission preset\nStep 4: Merge and export",
            justify="left"
        ).pack(pady=10)

        # File load buttons
        tk.Button(self.root, text="Load Optional Mods File", command=self.load_optional_mods_html).pack(pady=5)
        tk.Button(self.root, text="Load Mission File", command=self.load_mission).pack(pady=5)
        tk.Button(self.root, text="Generate Merged File", command=self.merge_and_export).pack(pady=10)

        # Add website link below the last button
        link_label = tk.Label(
            self.root,
            text="https://www.asotmilsim.com/",
            fg="blue",
            cursor="hand2"
        )
        link_label.pack(pady=(0, 10))
        link_label.bind("<Button-1>", lambda e: self.open_website())

    def open_website(self):
        webbrowser.open("https://www.asotmilsim.com/")

    def load_optional_mods_html(self):
        # Prompt user to select optional mods HTML file
        path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if not path:
            return
        try:
            # Clear previous mods before loading new ones
            self.optional_mods.clear()
            self.check_vars.clear()
            # Parse HTML and extract mod rows
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            mod_list_div = soup.find("div", class_="mod-list")
            if not mod_list_div:
                messagebox.showerror("Error", "Could not find 'mod-list' div in the HTML file.")
                return
            mod_table = mod_list_div.find("table")
            if not mod_table:
                messagebox.showerror("Error", "Could not find 'table' inside 'mod-list' div in the HTML file.")
                return
            for row in mod_table.find_all("tr"):
                name_td = row.find("td", {"data-type": "DisplayName"})
                span_tag = row.find("span")
                link_tag = row.find("a")
                if name_td and span_tag and link_tag:
                    name = name_td.text.strip()
                    source = span_tag.text.strip()
                    link = link_tag["href"].strip()
                    self.optional_mods.append({"name": name, "source": source, "link": link})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read optional mods:\n{e}")

        # Create scrollable list of mod checkboxes
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for mod in self.optional_mods:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(scrollable, text=mod["name"], variable=var, anchor="w", justify="left", wraplength=540)
            cb.pack(fill="x", padx=10, pady=2)
            self.check_vars.append((var, mod))

    def load_mission(self):
        # Prompt user to select mission preset HTML file
        path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.mission_html = f.read()
            messagebox.showinfo("Loaded", "Mission preset loaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read mission file:\n{e}")

    def merge_and_export(self):
        if not self.mission_html:
            messagebox.showerror("Error", "Mission file not loaded.")
            return

        try:
            selected_mods = [mod for var, mod in self.check_vars if var.get()]
            if not selected_mods:
                messagebox.showwarning("Warning", "No mods selected.")
            if not selected_mods:
                messagebox.showwarning("Warning", "No mods selected.")
                return
            soup = BeautifulSoup(self.mission_html, "html.parser")
            preset_name = simpledialog.askstring("Preset Name", "Enter a name for the merged preset:")
            if preset_name:
                head = soup.find("head")
                if not head:
                    # Create a head tag if missing
                    head = soup.new_tag("head")
                    soup.html.insert(0, head)
                tag = head.find("meta", attrs={"name": "arma:PresetName"})
                if tag:
                    tag["content"] = preset_name
                else:
                    new_meta = soup.new_tag("meta", name="arma:PresetName", content=preset_name)
                    head.append(new_meta)

            mod_list_div = soup.find("div", class_="mod-list")
            if not mod_list_div:
                messagebox.showerror("Error", "Could not find 'mod-list' div in the mission HTML file.")
                return
            mod_table = mod_list_div.find("table")
            if not mod_table:
                messagebox.showerror("Error", "Could not find 'table' inside 'mod-list' div in the mission HTML file.")
                return

            # Add selected mods to mod list
            for mod in selected_mods:
                tr = soup.new_tag("tr")
                tr["data-type"] = "ModContainer"

                td_name = soup.new_tag("td")
                td_name["data-type"] = "DisplayName"
                td_name.string = mod["name"]

                td_source = soup.new_tag("td")
                span = soup.new_tag("span")
                span["class"] = "from-steam"
                span.string = mod["source"]
                td_source.append(span)

                td_link = soup.new_tag("td")
                a = soup.new_tag("a", href=mod["link"])
                a["data-type"] = "Link"
                a.string = mod["link"]
                td_link.append(a)

                tr.append(td_name)
                tr.append(td_source)
                tr.append(td_link)
                mod_table.append(tr)

            # Use preset name for default filename and filter for HTML files
            default_filename = preset_name if preset_name else "merged_preset"
            out_path = filedialog.asksaveasfilename(
                defaultextension=".html",
                initialfile=f"{default_filename}.html",
                filetypes=[("HTML Files", "*.html")]
            )
            if out_path:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                messagebox.showinfo("Saved", f"Merged file saved:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge:\n{e}")

# Launch application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModMergerApp(root)
    root.mainloop()
