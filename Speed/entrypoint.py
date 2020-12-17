#Example File
#Source: https://realpython.com/pyspark-intro/
#https://max6log.wordpress.com/2020/05/25/introduction-to-pyspark-on-docker/

import pyspark

sc = pyspark.SparkContext('local[*]')

txt = sc.textFile('file:////usr//share//X11//Xcms.txt')

python_lines = txt.filter(lambda line: 'the' in line.lower())

print("The number of lines containing 'the' in your file is: ", python_lines.count())