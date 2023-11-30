import os, sys

# ========================================================= #
# ===  make__scanParameterFile.py                       === #
# ========================================================= #

def make__scanParameterFile( inpFile=None, outFile=None, mark=None, values=[], replaceMode=False ):

    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[make__scanParameterFile.py]  == ???" )
    if ( outFile is None ): sys.exit( "[make__scanParameterFile.py]  == ???" )
    
    # ------------------------------------------------- #
    # --- [1] read file                             --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        text = f.read()

    # ------------------------------------------------- #
    # --- [2] replace                               --- #
    # ------------------------------------------------- #
    if ( replaceMode ):
        for ik,val in enumerate(values):
            mark_ = mark + "{}".format(ik+1)
            text  = text.replace( mark_, val )
    else:
        text = text.format( *values )
    
    # ------------------------------------------------- #
    # --- [3] save file                             --- #
    # ------------------------------------------------- #
    with open( outFile, "w" ) as f:
        f.write( text )
        

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    nFile         = 4
    inpFile       = "dat/ref.json"
    outFile_base  = "dat/param_{0:02}.json"
    for ik in range( nFile ):
        outFile = outFile_base.format( ik+1 )
        values  = [ "{}".format(ik), "{}".format(-12.0*ik) ]
        mark    = "$"
        make__scanParameterFile( inpFile=inpFile, outFile=outFile, values=values, mark=mark, replaceMode=True )

