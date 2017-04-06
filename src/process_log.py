# your Python code to implement the features could be placed here
# note that you may use any language, there is no preference towards Python

import sys
import re
from collections import Counter

input_log_file = sys.argv[1]
host_output = open(sys.argv[2], 'w')
hour_output = open(sys.argv[3], 'w')
resource_output = open(sys.argv[4], 'w')
block_output = open(sys.argv[5], 'w')


DATE_FORMAT = '%d/%b/%Y:%H:%M:%S %z'
REGEX_FOR_LOG_LINE = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] \"(\S+) (\S+)\s*(\S+)?\s*\" (\d{3}) (\S+)'

def parse_log_line (line):
	"""
	Parse a single line from the log file.
	It extracts ip, date, url, protocol, respose_code, and response_length
	Argumets:
		line (str): log line to be parsed
	Return:
		dictionary with following keys:
			- host
			- date_time
			- method
			- endpoint
			- protocol
			- response_code
			- content_size
	"""

	match = re.search(REGEX_FOR_LOG_LINE.encode().decode(), line.encode().decode('utf-8','ignore'))

	if match:
		host		  = match.group(1)
		client_identd = match.group(2)
		user_id       = match.group(3)
		date_time     = match.group(4)
		method        = match.group(5)
		endpoint      = match.group(6)
		protocol      = match.group(7)
		response_code = int(match.group(8))
		content_size  = match.group(9)


		result_dict = {}
		result_dict["host"] = host
		result_dict["date_time"] = date_time
		result_dict["method"] = method
		result_dict["url"] = endpoint
		result_dict["protocol"] = protocol
		result_dict["response_code"] = response_code
		result_dict["size"] = content_size

		return result_dict
	else:
		return None
	# print("method : ", method, " --- endpoint : ", endpoint, " --- protocol : ", protocol, " --- response_code : ", response_code, " --- content_size : ", content_size)

enc='iso-8859-15'

def read_from_file (file):
	"""
		function which reads each line from the input log file.
		Arguments:
			file (str): url to log file
	"""

	try:
		with open(file, 'r', encoding=enc) as f_obj:
			for line in f_obj:
				parsed_line = parse_log_line(line)
				if parsed_line:
					yield parsed_line
				
	except FileNotFoundError:
		print("File not found")


def count_host_and_usage_frequency(host_counter, usage_counter,line):
	"""
    Counts number of times host/Ip addresses have accessed the website.
    Arguments:
        counter (Counter class): stores counts for each host/ip
        data (dict): parsed log line
    """
	if line:
		host_counter[line["host"]] += 1
		if line["size"] != "-":
			usage_counter[line["url"]] += int(line["size"])

host_freq = Counter()
data_usage_freq = Counter()

print ("Feature 1")

for line in read_from_file(input_log_file):
	count_host_and_usage_frequency(host_freq, data_usage_freq, line)

hosts_most_freq = host_freq.most_common(10)
usages_most_freq = data_usage_freq.most_common(10)

for host in hosts_most_freq:
	host_info = host[0] + "," + str(host[1])
	host_output.write(host_info + "\n")

for most_freq in usages_most_freq:
	resource_output.write(most_freq[0] + "\n")

print(hosts_most_freq)
print(usages_most_freq)

# for host in hosts_most_freq:
# 	print(host)

# for usage in data_usage_freq:
# 	print(usage)

print ("Feature 1 - end")

