import time 

# Check if it's a new day
# Make a new logfile if it is
def check_filename(filename):
	name = filename[:8]
	new_date = str(time.strftime("%Y%m%d"))
	if new_date != name:
		print("Creating a new log file")
		log_file_name = str(time.strftime("%Y%m%d_%Hh%Mm%Ss")) + "_log.txt"
		log_file = open(log_file_name, "a+")
		log_file.write("\nStart of session\n")
		log_file.close()
		
		return log_file_name
	
	else:
		return None

