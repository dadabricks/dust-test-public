# Diagnostics for the UDF sys.path bug: shows which route carries (or drops) the Git-folder
# root for a python file task. Run as a spark_python_task from BOTH /Repos and
# /Workspace/Users, then diff the output. Does NOT import the repo-root module, so it won't
# hard-fail -- it just reports state on the driver and the worker.
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.getOrCreate()

print("=== DRIVER ===")
print("cwd:", os.getcwd())
print("PYTHON_REPO_PATH:", os.environ.get("PYTHON_REPO_PATH"))
print("PYTHON_NOTEBOOK_PATH:", os.environ.get("PYTHON_NOTEBOOK_PATH"))
print("driver sys.path:", sys.path)
try:
    from pyspark.sql.connect.utils import normalize_workspace_includes

    print("normalize_workspace_includes():", normalize_workspace_includes())
except Exception as e:  # noqa: BLE001 - diagnostic only
    print("could not import normalize_workspace_includes:", repr(e))


def worker_probe(_):
    import os
    import sys

    return "|".join(
        [
            "cwd=" + os.getcwd(),
            "PYTHON_REPO_PATH=" + str(os.environ.get("PYTHON_REPO_PATH")),
            "ws_syspath=" + ",".join(p for p in sys.path if p.startswith("/Workspace")),
        ]
    )


probe_udf = udf(worker_probe, StringType())
df = spark.range(1).selectExpr("'x' as c")
print("=== WORKER ===")
print(df.select(probe_udf("c").alias("probe")).collect()[0]["probe"])
