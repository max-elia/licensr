import argparse
import json
import re
import shutil
import sys
import os

cwd = os.path.dirname(__file__)
root = ""

def license_header(files, src_and_comm, header):
    if os.path.isfile(header):
        reader = open(header,"r")
        lines = reader.readlines()
    elif isinstance(header, str):
        lines = header.splitlines(True)
    else:
        print("\"header\" has to be either string or file")
        return

    for src in src_and_comm:
        r = re.compile(".*" + re.escape(src["src_extension"]))
        f = list(filter(r.match, files))
        header_string = ""

        if isinstance(src["comment"], str):
            for line in lines:
                header_string += src["comment"] + " " + line
            header_string += "\n"

        elif len(src["comment"]) == 1:
            for line in lines:
                header_string += (src["comment"][0] + " " + line)
            header_string += "\n"

        elif len(src["comment"]) == 2:
            header_string += src["comment"][0] + "\n"
            for line in lines:
                header_string += line
            header_string += "\n" + src["comment"][1] + "\n"

        elif len(src["comment"]) == 3:
            header_string += src["comment"][0] + "\n"
            for line in lines:
                header_string += (src["comment"][1] + " " + line)
            header_string += "\n" + src["comment"][2] + "\n"

        for fi in f:
            rest=""
            try:
                shutil.copyfile(fi, fi+"~")
                from_file = open(fi+"~", "r")
                if len(src["comment"]) == 1:
                    while True:
                        f_line = from_file.readline()
                        if not re.match("^[ \t]*"+re.escape(src["comment"][0]),f_line):
                            break
                    rest = f_line + from_file.read()

                elif len(src["comment"]) == 2:
                    f_line = from_file.readline()
                    while re.match("^[ \t\n]+$",f_line):
                        f_line = from_file.readline()
                    if re.match("^[ \t]*"+re.escape(src["comment"][0]),f_line):
                        while not re.match("^[ \t]*"+re.escape(src["comment"][1]),f_line):
                            f_line = from_file.readline()
                        rest = from_file.read()
                    else:
                        from_file.close()
                        from_file = open(fi+"~", "r")
                        rest = from_file.read()
                elif len(src["comment"]) == 3:
                    f_line = from_file.readline()
                    while re.match("^[ \t\n]+$",f_line):
                        f_line = from_file.readline()
                    if re.match("^[ \t]*"+re.escape(src["comment"][0]),f_line):
                        while not re.match("^[ \t]*"+re.escape(src["comment"][2]),f_line):
                            f_line = from_file.readline()
                        rest = from_file.read()
                    else:
                        from_file.close()
                        from_file = open(fi+"~", "r")
                        rest = from_file.read()

                to_file = open(fi, "w")
                to_file.write(header_string)
                to_file.write(rest)
                to_file.close()
                from_file.close()
                os.remove(fi+"~")
            except:
                print("Error writing header to file: " + fi)
                shutil.copyfile(fi + "~", fi)
                os.remove(fi + "~")


def license_debian_dir(path, spdx, copy):
    if os.path.isdir(path):
        path += "/*"
    deb_file = open(root + "debian/copyright", "a")
    deb_file.write("Files: %s\nCopyright: %s\nLicense: %s\n\n" % (str(path).replace(root,""), copy, spdx))
    deb_file.close()

def license_debian_file(files, spdx, copy):
    deb_file = open(root + "debian/copyright", "a")
    for file in files:
        deb_file.write("Files: %s\nCopyright: %s\nLicense: %s\n\n" % (file.replace(root,""), copy, spdx))
    deb_file.close()

def make_debian():
    if not os.path.isdir(root + "debian"):
        os.mkdir(root + "debian")
    deb_file = open(root + "debian/copyright", "w")
    deb_file.write("Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n\n")
    deb_file.close()

def license_dot_license(files, header):
    if os.path.isfile(header):
        head = open(header,"r")
        h = head.read()
    elif isinstance(header, str):
        h = header
    else:
        print("\"header\" has to be either string or a file")
        return

    for file in files:
        f = open(file + ".license", "w")
        f.write(h)
        f.close()


def license(args):
    global root
    json_file = open(args.config, "r", encoding="UTF-8")
    config = json.load(json_file)
    json_file.close()

    root = args.project_path
    if len(root) > 0 and root[-1] != '/':
        root += "/"
    if not os.path.isdir(root):
        print("No valid path to root folder was given.")
        return


    all_files = []
    for (dirpath, dirnames, filenames) in os.walk(root):
        for x in filenames:
            all_files.append(os.path.join(dirpath, x))

    if os.path.isdir(root + "debian"):
        shutil.rmtree(root + "debian")

    licenses = []
    if all (keys in config for keys in ("SPDX", "license_text")) and os.path.isfile(config["license_text"]):
        lic_text = config["license_text"]
        if lic_text[:1] == '/':
            lic_text = lic_text[1:]
        if os.path.isfile(config["license_text"]):
            licenses.append((config["SPDX"], lic_text))
            if config["license_text"] in all_files:
                all_files.remove(lic_text)

        r = re.compile(
            "((.*\.licen[cs]e)|(.*[Ll][Ii][Cc][Ee][Nn][SsCc][Ee])|(.*LICEN[CS]ES/.*)|(.*\.git/+)|(.*\.svn/+)|(.*COPYING/.*)|(.*copyright)|(.*\.spdx)|(.*\.gitignore))")
        all_files = list(set(all_files) - set(filter(r.match, all_files)))

        # Exceptions
        if "exceptions" in config:
            for exception in config["exceptions"]:
                if "path" in exception:
                    path = exception["path"]
                    if (path[:1] == '/'):
                        path = path[1:]
                    if (path[-1] == '/'):
                        path = path[:-1]
                    path = root + path

                    exc_files = []
                    if os.path.isfile(path):
                        exc_files.append(path)
                    elif os.path.isdir(path):
                        for (dirpath, dirnames, filename) in os.walk(path):
                            for x in filename:
                                exc_files.append(os.path.join(dirpath, x))
                    else:
                        print("Path error in exception" + exception["path"])

                    exc_files = list(set(exc_files) - set(filter(r.match, exc_files)))

                    all_files = list(set(all_files) - set(exc_files))

                    if "SPDX" in exception:
                        isHere = False
                        for li in licenses:
                            if li[0] == exception["SPDX"]:
                                isHere = True

                        if not isHere:
                            if "license_text" in exception:
                                lic_text = exception["license_text"]
                                if lic_text[:1] =='/':
                                    lic_text = lic_text[1:]

                                if os.path.isfile(lic_text):
                                    licenses.append((exception["SPDX"], lic_text))
                                    if lic_text in all_files:
                                        all_files.remove(lic_text)
                                else:
                                    print("Wrong license_text file set for: " + exception["path"])
                                    continue

                    src_files = []
                    if "src_extensions_and_comment" in exception:
                        regex = ""
                        for src_extension in exception["src_extensions_and_comment"]:
                            if regex == "":
                                regex += "(.*" + re.escape(src_extension["src_extension"]) + ")"
                            else:
                                regex += "|" + "(.*" + re.escape(src_extension["src_extension"]) + ")"

                        for file in exc_files:
                            if re.match(regex, file):
                                src_files.append(file)

                    if src_files and "header" in exception:
                        license_header(src_files, exception["src_extensions_and_comment"], exception["header"])
                        exc_files = list(set(exc_files) - set(src_files))

                    if all(keys in exception for keys in ("SPDX", "copyright")):
                        if src_files:
                            if not os.path.isfile(root + "debian/copyright"):
                                make_debian()
                            license_debian_file(exc_files)
                        else:
                            if not os.path.isfile(root + "debian/copyright"):
                                make_debian()
                            license_debian_dir(path,exception["SPDX"], exception["copyright"])
                    elif "header" in exception:
                        license_dot_license(exc_files,exception["header"])
                    else:
                        print("Not enough Information in config file for exception: ", path,
                             "\nNo changes have been made to this directory")

                else:
                    print("\"path\"-attribute has to be set for all exceptions\nLicensing failed")

        # All files
        src_files = []
        if "src_extensions_and_comment" in config:
            regex = ""
            for src_extension in config["src_extensions_and_comment"]:
                if regex == "":
                    regex += "(.*" + re.escape(src_extension["src_extension"]) + ")"
                else:
                    regex += "|" + "(.*" + re.escape(src_extension["src_extension"]) + ")"

            for file in all_files:
                if re.match(regex, file):
                    src_files.append(file)

        if src_files and "header" in config:
            license_header(src_files, config["src_extensions_and_comment"], config["header"])
            all_files = list(set(all_files) - set(src_files))

        if all(keys in config for keys in ("SPDX", "copyright")):
            if not os.path.isfile(root + "debian/copyright"):
                make_debian()
            license_debian_file(all_files, config["SPDX"], config["copyright"])
        elif "header" in config:
            license_dot_license(all_files,config["header"])
        else:
            print("Not enough Information in config file to apply licensing.",
                  "\nNo changes have been made.")

        if len(licenses) == 1:
            shutil.copyfile(licenses[0][1], root + "LICENSE")
            if os.path.isdir(root + "LICENSES"):
                shutil.rmtree(root + "LICENSES")
        else:
            if not os.path.isdir(root + "LICENSES"):
                os.mkdir(root + "LICENSES")
            for lic in licenses:
                shutil.copyfile(lic[1], root + "LICENSES/" + lic[0] + ".txt")
            if os.path.isfile(root + "LICENSE"):
                os.remove(root + "LICENSE")

    else:
        print("License Text and SPDX have to be set correctly")


def main():
    parser = argparse.ArgumentParser(description = "A CLI for licensing your project")
    parser.add_argument("-c", type=str,
                        dest="config",
                        default="config.json",
                        help="Path to config.json file")
    parser.add_argument("-p", type=str,
                        dest="project_path",
                        help="Path to project root (defaults to cwd)",
                        default=cwd)

    args = parser.parse_args()
    sys.stdout.write(str(license(args)))


if __name__ == "__main__":
    main()