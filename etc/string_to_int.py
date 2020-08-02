from datetime import datetime, timedelta

def str2num_counter(text):
	if text.find('만') != -1:
		output = int(float(text.split('만')[0])*10000)
	elif text.find('천') != -1:
		output = int(float(text.split('천')[0])*1000)
	elif text != '':
		output = int(text)
	else:
		output = text
	return output

def str2num_date(text):
	now = datetime.now()
	output = text.split(' ')[0]
	if output.find('년') != -1:
		standard = int(output[:-1])
		output = now + timedelta(days=-(standard*365))
	elif output.find('개월') != -1:
		standard = int(output[:-2])
		output = now + timedelta(days=-(standard*30))
	elif output.find('주') != -1:
		standard = int(output[:-1])
		output = now + timedelta(days=-(standard*7))
	elif output.find('일') != -1:
		standard = int(output[:-1])
		output = now + timedelta(days=-standard)
	elif output.find('시간') != -1:
		standard = int(output[:-2])
		output = now + timedelta(hours=-standard)
	elif output.find('분') != -1:
		standard = int(output[:-1])
		output = now + timedelta(minutes=-standard)
	elif output.find('초') != -1:
		standard = int(output[:-1])
		output = now + timedelta(seconds=-standard)
	else:
		output = now

	return output

def str2num_time(text):
	times = text.split(':')
	times_length = len(times)
	second = 0

	for idx in range(times_length):
		if idx == 0:
			second += int(times[times_length - idx - 1])
		elif idx == 1:
			second += int(times[times_length - idx - 1]) * 60
		elif idx == 2:
			second += int(times[times_length - idx - 1]) * 60 * 60
		elif idx == 3:
			second += int(times[times_length - idx - 1]) * 60 * 60 * 24

	return second
