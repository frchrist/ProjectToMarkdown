import json
import os
import errors

#get all programming languange and extensions
with open("extension.json", "r") as ext:
		extension = dict(json.load(ext))

#Basic ignored folders
ignore_dirs = ["node_modules","migrations", "__pycache__", ".git", ".nuxt", ".venv", "bin", ".output" ]
ignore_files = ['package-lock.json', "yarn-lock.json"]

def processing(dir_name, output: str, ignore_files_plus=[], ignore_dirs_plus = [], sysout = print):
	if not output.endswith(".md") :
		sysout(errors.ERROR_CODE.E1010)
		sysout('ERROR[-] the output must be a markdown file')
		return errors.ERROR_CODE.E1010
	for root, dirs, files in os.walk(dir_name):
		for  dis in ignore_dirs:
			if dis in dirs:
				dirs.remove(dis)
		if files in ignore_dirs:
			continue

		for name in files:
			if name in ignore_files:
				continue

            

			#check if file is code source
			if extension.get(name.split(".")[-1]) == None:
				"""
					if the file extension is not in the extentions.json file
					so this file may be a binary file
					so escape this file
				"""
				continue
        


			path = os.path.join(root,name)

						
			with open(output, 'a+') as file:
				try:
					with open(path, "r") as codeContent:
						cString = ""

						for line in codeContent:
							sysout(line)
							

							cString += line
						ext = name.split(".")[-1]
						programming_lang = extension.get(ext, "config")

						content = f'\n### {path}\n```{programming_lang} \n {cString}```\n\n'
						file.write(content)

				except UnicodeDecodeError as e:
					sysout(e)
					pass

				except Exception as e:
					sysout("ERROR [-] "+e)


	return output

