import argparse

try:
	import matplotlib.pyplot as plt
except:
	plot_present = False
else:
	plot_present = True

CONVERSION_FACTOR = 3300
CDPRO_FORMAT_1 = """#
# PRINT    IBasis   
{:>7}{:>10}     
#
# Title Line
{}
#
#    WL_Begin     WL_End       Factor
     {:.5f}    {:.5f}    1
#
# CD DATA (Long to short wavelength)"""

CDPRO_FORMAT_2 = """
#
#  IGuess  Str1   Str2   Str3   Str4    Str5    Str6
        0
"""

class CollidingArgumentsException(Exception):
	pass


def get_default_filename(in_name):
	path = in_name.split("/")
	parts = path[-1].rsplit(".", 1)
	parts[0] += "-o"
	path[-1] = ".".join(parts)
	return "/".join(path)


def get_infile_name():
	in_file = input("Input file path: ")
	return in_file


def get_outfile_name(in_file):
	def_name = get_default_filename(in_file)
	out_file = input(f"Output file, leave blank for default [{def_name}]: ")
	if out_file == "":
		out_file = def_name
		print("Output file name set to default:", out_file)
	return out_file


def ask_parameters():
	c = float(input("Mass concentration [g/l]: "))
	M = float(input("Molar mass [g/mol]: "))
	n = int(input("Number of amino acids: "))
	d = float(input("Cuvette light path [cm]: "))
	return c, M, n, d


def parse_file(path):
	print("Parsing input:", path)
	wlength = []
	phi = []
	with open(path, mode='r', encoding='utf-8') as f:
		for line in f:
			if line[0].isdigit():
				l, p, _ = line.split("\t")
				wlength.append(float(l))
				phi.append(float(p))
	return(wlength, phi)


def check_task_length(task):
	if len(task) != 6 and len(task) != 7:
		raise ValueError("Improper format of the batch file (there must be 6 or 7 columns)")	


def parse_batch_task(line):
	task = line.split()
	check_task_length(task)
	try:
		if len(task) == 6:
			task = (task[0], task[1], float(task[2]), float(task[3]), int(task[4]), float(task[5]))
		elif len(task) == 7:
			task = (task[0], task[1], float(task[2]), float(task[3]), int(task[4]), float(task[5]), task[6])
	except Exception as e:
		raise ValueError("Improper format of the batch file (value format)")
	return task


def parse_batch_file(path):
	tasks = []
	with open(path, mode='r') as f:
		f_lines = f.read().splitlines() 
		for line in f_lines:
			if len(line.strip()) > 0 and line[0] != "#":
				task = parse_batch_task(line)
				tasks.append(task)
	return tasks


def convert(phi, c, M, n, d):
	return list(map(lambda x: x * M / (10 * c * d * n), phi))


def write_file(wlength, theta, path):
	print("Writing file:", path)
	with open(path, mode='w', encoding='utf-8') as f:
		for l, p in zip(wlength, theta):
			f.write("{} {}\n".format(l, round(p, 6)))


def write_cdpro_file(lmbd, theta, path, name, args):
	print("Writing CDPro file:", path)
	mode = 'w' if args["n"] and args["b"] is None else 'a'
	title = name if name is not None else args["i"]
	with open(path, mode=mode, encoding='utf-8') as f:
		f.write(CDPRO_FORMAT_1.format(0, args["c"], title, max(lmbd), min(lmbd)))

		for i, t in enumerate(theta):
			if i % 10 == 0: f.write("\n")
			f.write(" {: .3f}".format(t/CONVERSION_FACTOR))
		
		f.write(CDPRO_FORMAT_2)


def transform_file(task, args):
	if len(task) == 6:
		in_file, out_file, c, M, n, d = task
		name = args["d"]
	elif len(task) == 7:
		in_file, out_file, c, M, n, d, name = task

	lmbd, phi = parse_file(in_file)
	theta = convert(phi, c, M, n, d)
	if not args["q"]: 
		if args["c"] is not None: write_cdpro_file(lmbd, theta, out_file, name, args)
		else: write_file(lmbd, theta, out_file)
	return lmbd, phi, theta
	

def display_plot(x, y, xlab="Lambda", ylab="Theta", title=None):
	plt.axhline(0, color='red')
	plt.plot(x, y)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.subplots_adjust(left=0.15)
	plt.title(title)
	plt.show()


def plot_task(values, args):
	lmbd, phi, theta = values
	if not plot_present:
		print("[!] Matplotlib module required for plotting!")
	else:
		if args["t"]: display_plot(lmbd, theta, title=args["l"])
		if args["f"]: display_plot(lmbd, phi, ylab="Phi", title=args["l"])	


def process_tasks(tasks, args):
	for task in tasks:
		values = transform_file(task, args)
		if args["t"] or args["f"]: 
			plot_task(values, args)


def get_tasks(args):
	if args["b"] is None:
		in_file = get_infile_name() if args["i"] is None else args["i"]
		c, M, n, d = ask_parameters() if args["p"] is None else args["p"]
		if args["q"]: 
			tasks = [(in_file, None, c, M, n, d)]
		else:
			out_file = get_outfile_name(in_file) if args["o"] is None else args["o"]
			tasks = [(in_file, out_file, c, M, n, d)]
	else:
		tasks = parse_batch_file(args["b"])
	return tasks


def check_args(args):
	if args["b"] is not None and args["n"]:
		raise CollidingArgumentsException("In this version, CDProp cannot overwrite existing CDPro INPUT file while in batch mode. \n\
If you want to start from scratch instead of appending to an old file, please, delete the old file manually.")
	
	if args["b"] is not None and (args["i"] or args["o"] or args["p"]):
		print("[?] While in batch mode, -i, -o, and -p arguments are ignored.")

	if args["q"]:
		print("[?] Working in quiet mode, no output files will be written")


def get_args():
	parser = argparse.ArgumentParser(description='Preparation of files for CDPro. Converts units to molar ellipticity and may produce some plots in the process.',
									 epilog="Written by Jan Havránek in 2018")
	plotting_group = parser.add_argument_group('plotting')
	cdpro_group = parser.add_argument_group('CDPro input file')
	
	parser.add_argument("-i", metavar="infile", help="Input file. Will be asked for, if not specified.")
	parser.add_argument("-o", metavar="outfile", help="Output file. Set to default, if not specified.")
	parser.add_argument("-b", metavar="file", help="Batch file. Collides with some of the other console arguments (-i, -o, -p, -q and -n).")
	parser.add_argument("-p", metavar=("c", "M", "n", "d"), nargs=4, type=float, help="Mesurement parameters - mass concentration [g/l], molar mass [g/mol], number of amino acids,\
																  and cuvette light path [cm]. Will be asked for, if not specified.")
	
	plotting_group.add_argument("-t", action="store_true", help="Plot theta in the process of conversion.")
	plotting_group.add_argument("-f", action="store_true", help="Plot phi in the process of conversion.")
	plotting_group.add_argument("-l", metavar="title", help="Plot title.")
	plotting_group.add_argument("-q", action="store_true", help="Do not write output file. Might be useful for plotting.")

	cdpro_group.add_argument("-c", metavar="IBasis", type=int, help="Produce CDPro input file instead of usual molar ellipticity list. IBasis number must be given")
	cdpro_group.add_argument("-d", metavar="title", help="One line title in the CDPro input file. Will be replaced with the infile argument, if not specified")
	cdpro_group.add_argument("-n", action="store_true", help="Overwrite existing outfile, instead of appending to it")

	args = parser.parse_args()
	return vars(args)


def guide_transformation():
	args = get_args()
	check_args(args)
	tasks = get_tasks(args)
	process_tasks(tasks, args)


if __name__ == "__main__":
	try:
		print("")
		guide_transformation()
	except (EOFError, KeyboardInterrupt):
		print("\n\n[!] Processing aborted")
	except CollidingArgumentsException as e:
		print(f"[!] {e}")
	except Exception as e:
		print("\n[!] Something went horribly wrong. \n[!] Please, check your parameters and input file and try again")
		print(f"[!] {e}")
	else:
		print("Process finished successfully")
