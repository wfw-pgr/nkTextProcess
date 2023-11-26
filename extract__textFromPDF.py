import os, sys
import pypdf

# ========================================================= #
# ===  extract__textFromPDF.py                          === #
# ========================================================= #

def extract__textFromPDF( inpFile=None, outFile=None, silent=True, \
                          remove_return=True, returnType="list" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[ex1.py] inpFile == ???" )

    # ------------------------------------------------- #
    # --- [2] read pdf file                         --- #
    # ------------------------------------------------- #
    text_stack = []
    with open( inpFile, "rb" ) as f:
        # -- [2-1] open file                        --  #
        reader = pypdf.PdfReader( f )
        nPages = len( reader.pages )
        # -- [2-2] convert file into text           --  #
        for ik,apage in enumerate( reader.pages ):
            atext       = apage.extract_text()
            if ( remove_return ): atext = atext.replace( "\n", " " )
            text_stack += [ atext ]
        plaintext = "\n".join( text_stack )
    
    # ------------------------------------------------- #
    # --- [4] display / save in a file              --- #
    # ------------------------------------------------- #
    if ( not( silent ) ):
        for ik, atext in enumerate( text_stack ):
            print( "-"*70  )
            print( "---" + " page == {}".format( ik+1 ) )
            print( "-"*70 )
            print( atext )
            print()
    if ( outFile is not None ):
        with open( outFile, "w" ) as f:
            f.write( plaintext )

    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType == "list" ):
        return( text_stack )
    elif ( returnTYype == "str" ):
        return( plaintext  )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "pdf/sample.pdf"
    outFile = "dat/sample.txt"
    ret = extract__textFromPDF( inpFile=inpFile, outFile=outFile )
    print( ret )
