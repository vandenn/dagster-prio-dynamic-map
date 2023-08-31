<div align="center">

# Dynamic Mapping and Op Prioritization with Dagster

![python](https://img.shields.io/badge/python-3.11-blue)
![dagster](https://img.shields.io/badge/dagster-1.4-blue)

A reference repository for implementing parallel ops in Dagster that support sequential chaining.

</div>

# Setup

## Data

Data was downloaded from "The Complete Pokemon Dataset" in Kaggle:
https://www.kaggle.com/datasets/rounakbanik/pokemon
The CSV has also been provided in the `./data` directory.

## Installation

Make sure you have Python 3.11 installed in your system, and that you have the Pokemon CSV in `./data`, then run:
```bash
make init
make setup
make run
```
You should be able to access Dagit via `http://localhost:3000`.
