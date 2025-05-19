# crossref_to_ris.py

`crossref_to_ris.py` is a Python script that automates the conversion of plain-text references into structured RIS files using the [CrossRef API](https://api.crossref.org/). It is designed to streamline citation cleanup for manuscript preparation, literature reviews, or any academic writing workflow that involves managing large reference lists.

---

## 🔧 Features

- Accepts a plain-text file of free-form references (one per line)
- Queries the CrossRef API to retrieve full citation metadata
- Outputs a valid `.ris` file for use in reference managers like **Zotero**, **EndNote**, or **Mendeley**
- Logs any unmatched references into a separate text file for manual follow-up
- Command-line interface for easy integration into research workflows

---

## 🧪 Usage

```bash
python crossref_to_ris.py references.txt output.ris not_found.txt
```

**Arguments:**
- `references.txt`: Input file containing one reference per line
- `output.ris`: Output file containing all successfully matched references in RIS format
- `not_found.txt`: Output file listing references that could not be matched

---

## 📄 Example Input (`references.txt`)

```
Lennon, Niall J., et al. "Selection, optimization and validation of ten chronic disease polygenic risk scores." Nature medicine 30.2 (2024): 480-487.
Sun L, Pennells L, Kaptoge S, et al. Polygenic risk scores in cardiovascular risk prediction: A cohort study. PLoS Med. 2021;18(1):e1003498.
```

---

## 📤 Example Output (`output.ris`)

```
TY  - JOUR
AU  - Lennon, Niall J.
TI  - Selection, optimization and validation of ten chronic disease polygenic risk scores
JO  - Nature Medicine
Y1  - 2024
VL  - 30
IS  - 2
SP  - 480
EP  - 487
DO  - 10.1038/s41591-024-02900-x
ER  -
```

---

## 📦 Requirements

- Python 3.6 or later
- `requests` library

Install dependencies with:

```bash
pip install requests
```

---

## 📁 File Structure

```
crossref_to_ris/
├── crossref_to_ris.py      # The main script
└── README.md               # This file
```

---

## 📄 License

MIT License — see the main repository [LICENSE](../LICENSE) file.
