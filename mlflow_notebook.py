# Databricks notebook source

import mlflow

run = mlflow.start_run()
run_id = mlflow.active_run().info.run_id
mlflow.end_run()
dbutils.notebook.exit(run_id)
