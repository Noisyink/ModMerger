# ASOT Mod Merger

A simple Python Tkinter application for merging Arma 3 mod preset HTML files.  
Select mods from an optional mods list, load a mission preset, and export a merged preset.

## Features

- Loads optional mods from an HTML file
- Loads mission preset HTML file
- Lets you select mods via a scrollable checkbox list
- Merges selected mods into the mission preset
- Allows you to name and save the merged preset
- Custom window icon support (`logo.ico`)
- Website link to [asotmilsim.com](https://www.asotmilsim.com/)

## Requirements

- Python 3.8+
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

Install dependencies:
```sh
pip install beautifulsoup4
```

## Usage

1. Place `logo.ico` in the same folder as `ASOTModMergerv5.pyw`.
2. Run the script:
    ```sh
    python ASOTModMergerv5.pyw
    ```
3. Use the buttons to load your optional mods HTML and mission preset HTML.
4. Select mods from the scrollable list.
5. Click "Generate Merged File" to export your merged preset.

## Packaging

If you want to create a standalone executable (e.g., with PyInstaller):

```sh
pyinstaller --onefile --windowed --icon=logo.ico ASOTModMergerv5.pyw
```

## Troubleshooting

- If you see an error about the icon, ensure `logo.ico` exists and is a valid `.ico` file.
- Only `.ico` files are supported for the window icon on Windows.

## License

MIT License

---

Made for