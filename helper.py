        
def name_count(list):
	nameDict = {}
	for name in list:
		if name in nameDict:
			nameDict[name] = nameDict[name] + 1
		if not name in nameDict:
			nameDict[name] = 1

	return nameDict
