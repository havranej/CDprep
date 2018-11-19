
def user_input():
	print("CDPro preparation script")
	in_file = input("Original file path: ")
	out_file = input("Output file: ")
	c = float(input("Mass concentration [g/l]: "))
	M = float(input("Molar mass [g/l]: "))
	n = int(input("Number of amino acids: "))
	d = float(input("Cuvette light path [cm]: "))
	return in_file, out_file, c, M, n, d


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


def transform_file():
	in_file, out_file, c, M, n, d = user_input()
	lmbd, phi = parse_file(in_file)
	theta = convert(phi, c, M, d, n)
	write_file(lmbd, theta, out_file)


if __name__ == "__main__":
	try:
		transform_file()
	except EOFError:
		print("\n\nProcessing aborted")
	except Exception as e:
		print("\n[!] Something went horribly wrong. \n[!] Please, check your parameters and input file and try again")
		print("[!] {0}".format(e))
	else:
		print("Transformation finished successfully")

	try:
		input("\nPress enter to quit")
	except:
		pass

