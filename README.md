# MalDB

MalDB is a database management system for malware samples.
The database is designed to store and manage malware samples for research purposes.
The database is designed to be used by security researchers, malware analysts, and other security professionals.

---

## Environment Setup

You need python environment to run the MalDB.
Recommended to use conda to create a new environment.
```bash
conda create -n maldb python=3.12
conda activate maldb
```

---

## Installation

1. Clone the repository
2. Install the required dependencies
3. Run the MalDB

```bash
git clone
cd maldb
pip install -r requirements.txt
python main.py
```

---

## Usage

Initialize the database:

```bash
python main.py init
```

Scan malware samples:

```bash
python main.py s [--tag] [--type]
```

Download malware samples:

```bash
python main.py d
```

Export malware samples information:

```bash
python main.py e
```

---

## Sample sources

- MalwareBazaar: https://bazaar.abuse.ch/
- VirusShare: https://virusshare.com/
- VirusTotal: https://www.virustotal.com/
