# DAG Modeler
## 1. evaluate the latency distribution, calculated as the cdf of measured latency, of individual stages within the DAGs, more details refer to /DAG_Modeler/DAG_Modeler/CDF.cs
### Note that the algorithm makes the step size as 10 (interval) to divide the original data; moreover, the right boundary of each interval are recorded.
## 2. 

# Data Loader
## ORION post-process the dataset as follows:
### For video analysis application
Each record corresponds to a video_index, which are splitted into 30 video chunks and each chunk shares the same execution info, 
including split, extract, and classify, which are processed by six workers.
For evaluating the conditional latency distribution of intra-stages (parallel worker), it requires to check all the latency of workers in processing chunks

