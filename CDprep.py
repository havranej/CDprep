try:
	import matplotlib.pyplot as plt
except:
	plot_present = False
else:
	plot_present = True
import argparse

def default_filename(in_name):
	path = in_name.split("/")
	parts = path[-1].rsplit(".", 1)
	parts[0] += "-o"
	path[-1] = ".".join(parts)
	return "/".join(path)

def get_infile_name():
	in_file = input("Input file path: ")
	return in_file

def get_outfile_name(in_file):
	out_file = input("Output file (leave blank for default): ")
	if out_file == "":
		out_file = default_filename(in_file)
		print("Output file name set to default:", out_file)
	return out_file

def param_input():
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


def convert(phi, c, M, d, n):
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

def get_args():
	parser = argparse.ArgumentParser(description='Preparation of files for CDPro. Converts units to molar ellipticity and may produce some plots in the process.',
									 epilog="Written by Jan Havránek in 2018")
	parser.add_argument("infile", nargs="?", default=None, help="Input file. Will be asked for, if not specified.")
	parser.add_argument("-o", metavar="outfile", help="Output file. Set to default, if not specified.")
	parser.add_argument("-p", metavar=("c", "M", "n", "d"), nargs=4, type=float, help="Mesurement parameters - mass concentration [g/l], molar mass [g/mol], number of amino acids,\
																  and cuvette light path [cm]. Will be asked for, if not specified.")
	parser.add_argument("-t", action="store_true", help="Plot theta in the process of conversion.")
	parser.add_argument("-f", action="store_true", help="Plot phi in the process of conversion.")
	parser.add_argument("-i", metavar="title", help="Plot title.")
	parser.add_argument("-n", action="store_true", help="Do not write output file. Might be useful for plotting.")

	args = parser.parse_args()
	return vars(args)

def transform_file():
	args = get_args()
	in_file = get_infile_name() if args["infile"] is None else args["infile"]
	lmbd, phi = parse_file(in_file)
	c, M, n, d = param_input() if args["p"] is None else args["p"]
	if not args["n"]: out_file = get_outfile_name(in_file) if args["o"] is None else args["o"]
	theta = convert(phi, c, M, d, n)
	if args["t"] or args["f"]:
		if not plot_present:
			print("[!] Matplotlib module required for plotting!")
		else:
			if args["t"]: display_plot(lmbd, theta, title=args["i"])
			if args["f"]: display_plot(lmbd, phi, ylab="Phi", title=args["i"])
	if not args["n"]: write_file(lmbd, theta, out_file)


if __name__ == "__main__":
	try:
		transform_file()
	except (EOFError, KeyboardInterrupt):
		print("\n\n[!] Processing aborted")
	except Exception as e:
		print("\n[!] Something went horribly wrong. \n[!] Please, check your parameters and input file and try again")
		print("[!] {0}".format(e))
	else:
		print("Process finished successfully")

	try:
		input("\nPress enter to quit")
	except:
		pass

