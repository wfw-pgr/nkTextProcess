import os, sys
import googletrans
import nkTextProcess.extract__textFromPDF as etp
import nkTextProcess.convert__text2pdf    as t2p

# ========================================================= #
# ===  translator__usingGoogleTrans.py                  === #
# ========================================================= #

def translator__usingGoogleTrans( input_pdfFile=None, output_pdfFile=None, \
                                  english_txtFile=None, japanese_txtFile=None, \
                                  fontsize=9.0, silent=True ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( input_pdfFile  is None ): sys.exit("[translator__usingGoogleTrans.py] input_pdfFile  == ???")
    if ( output_pdfFile is None ): output_pdfFile = input_pdfFile.replace( ".pdf", "_ja.pdf" )

    # ------------------------------------------------- #
    # --- [2] extract__textFromPDF                  --- #
    # ------------------------------------------------- #
    text_en = etp.extract__textFromPDF( inpFile=input_pdfFile, outFile=english_txtFile, \
                                        remove_return=True )
    
    # ------------------------------------------------- #
    # --- [3] translator into japanese              --- #
    # ------------------------------------------------- #
    tr         = googletrans.Translator()
    text_stack = []
    for ik,apage in enumerate( text_en ):
        text_piece = ( tr.translate( apage, dest="ja", src="en" ) ).text
        text_stack+= [ text_piece ]
    text_ja = "\n\n".join( text_stack )

    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    if ( not( silent ) ):
        print( "\n" + "-"*70 +"\n"  )
        print( text_ja )
        print( "\n" + "-"*70 +"\n"  )
        
    if ( japanese_txtFile is not None ):
        with open( japanese_txtFile, "w" ) as f:
            f.write( text_ja )

    # ------------------------------------------------- #
    # --- [5] convert into japanese pdf             --- #
    # ------------------------------------------------- #
    t2p.convert__text2pdf( outFile=output_pdfFile, texts=text_stack, fontsize=fontsize )
    
    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    return( text_ja )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "--input_pdf"     , default=None, help="input pdf file"     )
    parser.add_argument( "--output_pdf"    , default=None, help="output pdf file"    )
    parser.add_argument( "--english_text"  , default=None, help="english_text_file"  )
    parser.add_argument( "--japanese_text" , default=None, help="japanese_text_file" )
    parser.add_argument( "--fontsize"      , type=float, default=9.0, help="font size"        )
    parser.add_argument( "--show"          , type=bool , default=False, help="display or not" )
    parser.add_argument( "--intermediate"  , type=bool , default=False, help="intermidiate file out" )
    
    args   = parser.parse_args()

    if ( not( args.input_pdf ) ):
        print( "[ How to use ] python translator__usingGoogleTrans.py --input_pdf xxx.pdf " )
        sys.exit()
    else:
        input_pdfFile = str( args.input_pdf )
    if ( args.intermediate ):
        if ( args.english_text  is None ): args.english_text  = "text_en.txt"
        if ( args.japanese_text is None ): args.japanese_text = "text_ja.txt"

    # ------------------------------------------------- #
    # --- [2] call translator                       --- #
    # ------------------------------------------------- #
    print( "[translator__usingGoogleTrans.py] translation of {}".format( args.input_pdf ) )
    translator__usingGoogleTrans( input_pdfFile=args.input_pdf, output_pdfFile=args.output_pdf, \
                                  english_txtFile=args.english_text, \
                                  japanese_txtFile=args.japanese_text,\
                                  fontsize=args.fontsize, silent=not( args.show ) )



