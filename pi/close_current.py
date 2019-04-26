import subprocess

def close_current_processes():
	processes = subprocess.check_output(["ps", "-aux"]).split('\n')
	for process in processes:
		process = process.decode("utf-8")
		if "full_circle/pi" in process.lower() and "python" in process.lower() and not "run_at_start" in process.lower():
			split_process = process.split()
			subprocess.call(["sudo", "kill", split_process[1]])
			print "Killed process ", split_process[-1]
			
	return
	
close_current_processes()
