# Bug repro for python file task: a UDF that re-imports a repo-root module on the
# Spark worker. Unlike a notebook task, a python_file task does NOT get the Workspace/repo
# sys.path propagation on the executor, so under /Workspace/Users this fails with
# ModuleNotFoundError during UDF deserialization; under /Repos it works. Run this as a
# spark_python_task (NOT a notebook task) to reproduce.
from libraries.gen_hello import gen_hello
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.getOrCreate()

hello_udf = udf(lambda name: gen_hello(name), StringType())

df = spark.range(1).selectExpr("'Ala' as name")
res = df.select(hello_udf("name").alias("greeting")).collect()[0]["greeting"]
print(res)
assert res == "Hello Ala", f"unexpected result from gen_hello UDF: {res}"
