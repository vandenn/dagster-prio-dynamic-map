<div align="center">

# Dynamic Mapping and Op Prioritization with Dagster

![python](https://img.shields.io/badge/python-3.11-blue)
![dagster](https://img.shields.io/badge/dagster-1.4-blue)

A reference repository for implementing parallel ops in Dagster that support sequential chaining.

</div>

# 📄 Overview

🔍 You will find all these job definitions in the [`src/jobs.py`](src/jobs.py) file.

## Standard Static Job

The standard static job is what you may typically build in Dagster. If you were developing an ETL pipeline for a large raw dataset for example, the job would perform the full extraction of data first, then the various transforms, and finally load to whichever destination data store you need the data to be. You'd have a Gantt chart that looks like this:

![Non-Dynamic Gantt Chart](https://github.com/vandenn/dagster-prio-dynamic-map/assets/6585214/ed0bd529-d263-41a3-ae39-624f299e9186)

However, this **can be really slow** especially if you're running a lot of expensive transforms on a huge amount of data, since each job is iterating through the data sequentially. As mentioned in the [Dagster documentation](https://docs.dagster.io/concepts/ops-jobs-graphs/dynamic-graphs#a-static-job), even if a job can be parallelized internally, if something goes wrong, the whole thing needs to start over.

## Standard Dynamic Job

With [Dynamic Graphs](https://docs.dagster.io/concepts/ops-jobs-graphs/dynamic-graphs#dynamic-graphs), we can achieve parallelization of jobs on **batches** of the data, instead of having to iterate through the entire chunk one at a time, using [`DynamicOut`](https://docs.dagster.io/_apidocs/dynamic#dagster.DynamicOut) and [`map`](https://docs.dagster.io/_apidocs/dynamic#dagster.DynamicOut).

![chrome_Ulwcc3D3ko](https://github.com/vandenn/dagster-prio-dynamic-map/assets/6585214/34116c7e-373f-43ba-8044-783b0be47729)

This is better than the static job in terms of performance, but only if your ETL pipeline doesn't require that your data be transformed sequentially.

However, as you'll notice in the Gantt chart above, there's another problem: all the cloned/mapped ops of one op all get executed first before moving on to the next set of ops. This can be an **issue if memory is also a concern** wherever Dagster is deployed, because this set-up will still retrieve all of the data first before executing the subsequent transform and load steps.

## Dynamic Job with Prioritization

Using Dagster's [`dagster/priority`](https://docs.dagster.io/guides/customizing-run-queue-priority#defining-queue-prioritization-rules) tag, we can tell Dagster to immediately run the next op in the sequence by increasing the priority of the ops that come later. Looking at the Gantt chart below, a group of batches (up to how many concurrent processes your machine can handle, or how much is specified using the [`max_concurrent`](https://docs.dagster.io/guides/limiting-concurrency-in-data-pipelines#op-based-jobs)) are executed from end-to-end first before moving to the next group of batches.

![chrome_uLCydDoFFP](https://github.com/vandenn/dagster-prio-dynamic-map/assets/6585214/f05ae1b7-85d6-4651-8844-bc0b09830046)

With this, you have control over how many concurrent ops can run at the same time, and the pipeline will have the opportunity to clean up data from batches that have been fully processed already.

# 🛠 Setup

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
