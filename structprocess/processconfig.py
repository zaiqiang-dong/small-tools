def pconfig():
    configFd = open("./.config", "r")
    outFd = open("./source/config.h", "w")
    lines = configFd.readlines()
    outlines = []
    for line in lines:
        line = line.strip()
        if line != "" and line[0:1] != '#' and line[0:1] != " ":
            splines = line.split('=')
            if len(splines) >= 2:
                outlines.append("#define " + splines[0] + " " + splines[1] + "\n")
            else:
                outlines.append("#define " + splines[0] + "\n")

        else:
            pass

    outFd.writelines(outlines)
    outFd.close()
    configFd.close()


if __name__ == "__main__":
    pconfig()
