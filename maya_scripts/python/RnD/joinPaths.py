#hardcoded test path - this could be read in from a .txt file
prj = "C:/Users/robert/Documents/maya/projects/jibjab/sbtv"
prd = "season_01/101_rain/2_production"
seq = "sq030_reindeer"
sht = "sh_190"
dpt = "03_maya/02_lighting"
fnm = "s030_190_reindeer_lit.mb"
###the slashes may need to be changed for windows
fullFilePath = '/'.join([prj,prd,seq,sht,dpt,fnm])
cmds.file(fullFilePath, force=1, options= "v=0;", type= "mayaBinary", pr=1, ea=1)