import argparse

try:
	import matplotlib.pyplot as plt
except:
	plot_present = False
else:
	plot_present = True


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
	wlength = []
	phi = []
	with open(path, mode='r', encoding='utf-8') as f:
		f_lines = f.read().splitlines() 
		for line in f_lines:
			if line[0].isdigit():
				l, p, _ = line.split("\t")
				wlength.append(float(l))
				phi.append(float(p))
	return(wlength, phi)

def parse_batch_task(line):
	task = line.split()
	if len(task) != 6: raise ValueError("Improper format of the batch file")
	task = (task[0], task[1], float(task[2]), float(task[3]), int(task[4]), float(task[5]))
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


def write_file(wlength, phi, path):
	with open(path, mode='w', encoding='utf-8') as f:
		for l, p in zip(wlength, phi):
			f.write("{0} {1}\n".format(l, round(p, 6)))


def display_plot(x, y, xlab="Lambda", ylab="Theta", title=None):
	plt.axhline(0, color='red')
	plt.plot(x, y)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.subplots_adjust(left=0.15)
	plt.title(title)
	plt.show()

def get_tasks(args):
	if args["b"] is None:
		in_file = get_infile_name() if args["infile"] is None else args["infile"]
		c, M, n, d = ask_parameters() if args["p"] is None else args["p"]
		if args["n"]: 
			tasks = [(in_file, None, c, M, n, d)]
		else:
			out_file = get_outfile_name(in_file) if args["o"] is None else args["o"]
			tasks = [(in_file, out_file, c, M, n, d)]
	else:
		tasks = parse_batch_file(args["b"])
	return tasks

def transform_file(task, args):
	in_file, out_file, c, M, n, d = task
	lmbd, phi = parse_file(in_file)
	theta = convert(phi, c, M, n, d)
	if not args["n"]: write_file(lmbd, theta, out_file)
	return lmbd, phi, theta
	

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

def get_args():
	parser = argparse.ArgumentParser(description='Preparation of files for CDPro. Converts units to molar ellipticity and may produce some plots in the process.',
									 epilog="Written by Jan Havránek in 2018")
	plotting_group = parser.add_argument_group('plotting')
	parser.add_argument("infile", nargs="?", default=None, help="Input file. Will be asked for, if not specified.")
	parser.add_argument("-o", metavar="outfile", help="Output file. Set to default, if not specified.")
	parser.add_argument("-b", metavar="file", help="Batch file. Overrides some of the console arguments (-i, -o, -p and -n).")
	parser.add_argument("-p", metavar=("c", "M", "n", "d"), nargs=4, type=float, help="Mesurement parameters - mass concentration [g/l], molar mass [g/mol], number of amino acids,\
																  and cuvette light path [cm]. Will be asked for, if not specified.")
	plotting_group.add_argument("-t", action="store_true", help="Plot theta in the process of conversion.")
	plotting_group.add_argument("-f", action="store_true", help="Plot phi in the process of conversion.")
	plotting_group.add_argument("-l", metavar="title", help="Plot title.")
	plotting_group.add_argument("-n", action="store_true", help="Do not write output file. Might be useful for plotting.")

	args = parser.parse_args()
	return vars(args)


def guide_transformation():
	args = get_args()
	tasks = get_tasks(args)
	process_tasks(tasks, args)


if __name__ == "__main__":
	try:
		guide_transformation()
	except (EOFError, KeyboardInterrupt):
		print("\n\n[!] Processing aborted")
	except Exception as e:
		print("\n[!] Something went horribly wrong. \n[!] Please, check your parameters and input file and try again")
		print(f"[!] {e}")
	else:
		print("Process finished successfully")
