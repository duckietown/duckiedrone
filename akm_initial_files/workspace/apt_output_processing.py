

f = open("output.txt", "r")
fo = open("run_command.txt", "w+")
first = True 
#fo.write("RUN apt-get update && apt-get install -y \\\n")
for i in f:
	if first == True:
		first = False
		continue
	slash = i.find("/")
	name = i[:slash]
	space1 = i.find(" ")
	i = i[space1+1:]
	space2 = i.find(" ")
	version = i[:space2]
	write_string = "\t"+name+"\\\n"
	fo.write(write_string)
        print("RUN apt-get install -y " +name)
