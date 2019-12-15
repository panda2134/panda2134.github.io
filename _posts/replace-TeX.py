#!/usr/bin/env python3
from os import listdir, SEEK_SET
from io import StringIO
# $$
for filename in listdir():
	if len(filename.split('.')) <= 1 or filename.split('.')[1] != 'md':
		continue
	print("Opening", filename)
	tmp = StringIO()
	with open(filename, "r") as f:
		f.seek(0, SEEK_SET)
		for line in f.readlines():
			if len(line.split()) == 1 and line.split()[0] == '$$':
				print(line, file=tmp, end='')
				# print("got", line, end='')
				continue
			line = line.replace('$$', '$')
			print(line, file=tmp, end='')
			# print("got", line, end='')
	tmp.seek(0, SEEK_SET)
	with open(filename, "w") as f:
		f.write(tmp.read())
	print("Processed", filename)

# \{
for filename in listdir():
	if len(filename.split('.')) <= 1 or filename.split('.')[1] != 'md':
		continue
	print("Opening", filename)
	tmp = StringIO()
	with open(filename, "r") as f:
		f.seek(0, SEEK_SET)
		for line in f.readlines():
			line = line.replace('\\{', '\\\\{').replace('\\}', '\\\\}')
			print(line, file=tmp, end='')
			# print("got", line, end='')
	tmp.seek(0, SEEK_SET)
	with open(filename, "w") as f:
		f.write(tmp.read())
	print("Processed", filename)
