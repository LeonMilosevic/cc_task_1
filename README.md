# Cyber Care Task_1

### Intro

Get sum of replies for a given day.

### How to use it:

```
git clone https://github.com/LeonMilosevic/cc_task_1.git
```

```
pip install -r requirements.txt
```

```
python main.py
```

### Pipeline Walkthrough:

Extract:

- Extract all transactions from Source (source dir)<br />
&darr;
- Ensure Data Quality checks for fetched data.<br />

Transform:

- Apply transformations needed per business requirements.<br />

Load:
- Dump result as csv file in storage dir. <br />

### Expected Results:

- CSV file with sum of replies for 2022-03-05.