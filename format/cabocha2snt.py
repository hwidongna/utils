from __init__ import *
INFO = re.compile("\* (\d+) (-1|\d+)[O|D] (\d+)/(\d+)")#* 0 11D 0/0 2.08150609

def main():
	args = sys.argv[1:]
	space = re.compile( "[ 	]" )
	slash = re.compile( "/" )
	
	header = re.compile( "^\* \d" )
	eos = re.compile( "^EOS$" )
	
	for arg in args :
		os.system( "cut -f1,4 < " + arg + " > build.temp" )
		infile = open( 'build.temp' , 'r' )
		base_out = open( arg + ".base" , 'w' )
		stem_out = open( arg + ".stem" , 'w' )
		line = infile.readline() 

		bunsetsu = "" 
		stem = ""	
		pos = ""
		baseline = ""
		stemline = ""
		idx = 0
		start = 0
		end = 0

		while line != "" :	
			parts = space.split( line )

			#sys.stdout.write( line )
			#sys.stdout.write( parts[0] + "\n" )
			if header.search( line ) != None :
				#sys.stdout.write( "111\n" )
				#sys.stdout.write( bunsetsu + 'a\n'  )
				#sys.stdout.write( pos + 'b\n'  )
				if len(bunsetsu) != 0 :	
					btemp = bunsetsu + "@/#" + pos
					btemp = btemp.replace( "\n" , "" )
					stemp = stem + "@/#" + pos
					stemp = stemp.replace( "\n" , "" )
					if len(baseline) != 0 :	
						baseline += " " 
						stemline += " " 
					stemline += stemp 
					baseline += btemp 

				bunsetsu = ""
				stem = ""
				pos = ""
				nums = slash.split( parts[3] )
				start = int(nums[0])
				end = int(nums[1])
				idx = 0 


			elif eos.search( line ) != None :
				if len(bunsetsu) != 0 :	
					btemp = bunsetsu + "@/#" + pos
					btemp = btemp.replace( "\n" , "" )
					stemp = stem + "@/#" + pos
					stemp = stemp.replace( "\n" , "" )
					if len(baseline) != 0 :	
						baseline += " " 
						stemline += " " 
					stemline += stemp 
					baseline += btemp 
					bunsetsu = ""
					stem = ""
					pos = ""
	
			#sys.stdout.write( "222\n" )
				base_out.write( baseline + "\n" )
				stem_out.write( stemline + "\n" )
				baseline = ""
				stemline = ""
				
			else :
				#print idx, start, end
				#sys.stdout.write( "333\n" )
				#sys.stdout.write( parts[0] + "\n" )
				if idx < start :
					stem += parts[0]
				#	sys.stdout.write( stem + "a\n" )
				elif idx == start :
					stem += parts[0]
					pos += parts[1]
				#	sys.stdout.write( stem + "/" + pos + "b\n" )
				if idx > start and idx <= end :
					pos += parts[0]

				#	sys.stdout.write( pos +  "c\n" )
				if idx > end  :
					stem += parts[0]
				#	sys.stdout.write( stem + "d\n" )
				bunsetsu += parts[0]
				#print bunsetsu	
				idx = idx + 1 
			line= infile.readline()

		infile.close()
		base_out.close()
		stem_out.close()
		os.system( "rm build.temp" )
if __name__=="__main__":
    if sys.argv[1:]:
        main()
        sys.exit()
    for line in imap(str.strip, sys.stdin):
        if not line:
            sys.stdout.write(linesep)
            continue
        bInfo = INFO.match(line)
        if bInfo:
            chunkno, governor, head_start, head_end = map(int, bInfo.groups())
            i = 0
            continue
        sys.stdout.write('\t'.join(line.split('\t')+map(str,[chunkno]))+linesep)
        i += 1

