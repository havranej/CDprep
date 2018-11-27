try:
	import matplotlib.pyplot as plt
except:
	plot_present = False
else:
	plot_present = True

def default_filename(in_name):
	path = in_name.split("/")
	parts = path[-1].rsplit(".", 1)
	parts[0] += "-o"
	path[-1] = ".".join(parts)
	return "/".join(path)

def file_input():
	in_file = input("Original file path: ")
	out_file = input("Output file (leave blank for default): ")
	if out_file == "":
		out_file = default_filename(in_file)
		print("Output file name set to default:", out_file)
	#if len(out_file) > 12: print("[?] Your file name is longer than 12 characters\n[?] CDPro might have problem with that")
	return in_file, out_file


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

def display_plot(x, y, xlab="Lambda", ylab="Theta"):
	plt.axhline(0, color='red')
	plt.plot(x, y)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.show()

def transform_file():
	in_file, out_file = file_input()
	lmbd, phi = parse_file(in_file)
	c, M, n, d = param_input()
	theta = convert(phi, c, M, d, n)
	if plot_present: display_plot(lmbd, theta)
	write_file(lmbd, theta, out_file)


if __name__ == "__main__":
	try:
		transform_file()
	except (EOFError, KeyboardInterrupt):
		print("\n\n[!] Processing aborted")
	except Exception as e:
		print("\n[!] Something went horribly wrong. \n[!] Please, check your parameters and input file and try again")
		print("[!] {0}".format(e))
	else:
		print("Transformation finished successfully")

	try:
		input("\nPress enter to quit")
	except:
		pass

