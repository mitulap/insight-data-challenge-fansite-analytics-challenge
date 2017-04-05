# your Python code to implement the features could be placed here
# note that you may use any language, there is no preference towards Python

import sys
import re

input_log_file = sys.argv[1]

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

	match = re.search(REGEX_FOR_LOG_LINE, line)

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
	result_dict["content_size"] = content_size

	return result_dict
	# print("method : ", method, " --- endpoint : ", endpoint, " --- protocol : ", protocol, " --- response_code : ", response_code, " --- content_size : ", content_size)

def read_from_file (file):
	"""
		function which reads each line from the input log file.
		Arguments:
			file (str): url to log file
	"""

	try:
		with open(file) as f_obj:
			for line in f_obj:
				print(parse_log_line(line))
				
	except FileNotFoundError:
		print("File not found")

read_from_file(input_log_file)