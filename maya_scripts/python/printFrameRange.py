import sys

text = 'playbackOptions'

def readFile( fileName ):

		txtFile = open( fileName, 'r' )	
		fileContents = txtFile.readlines()
		txtFile.close()

		return fileContents

def findContents( fileContents, text ):
	
	for line in fileContents:
		if text in line: return line 
	
	
if __name__ == '__main__':
	fileContents = readFile(sys.argv[1])
	print ( findContents( fileContents, text ) )
	