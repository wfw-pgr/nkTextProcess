#!/usr/bin/env python3
import os, sys
import pypdf
import googletrans

from reportlab.pdfbase            import pdfmetrics, cidfonts
from reportlab.lib.styles         import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus           import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.pagesizes      import A4, mm, portrait

# ========================================================= #
# ===  extract__textFromPDF.py                          === #
# ========================================================= #

def extract__textFromPDF( inpFile=None, outFile=None, silent=True, \
                          remove_return=True, returnType="list" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[extract__textFromPDF.py] inpFile == ???" )

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
# ===  convert__text2pdf.py                             === #
# ========================================================= #

def convert__text2pdf( outFile=None, texts=None, fontsize=9.0, leading=None, \
                       output_by_page=True ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( outFile is None ): sys.exit( "[convert__text2pdf.py] outFile == ???" )
    if ( texts   is None ): sys.exit( "[convert__text2pdf.py] texts   == ???" )
    if ( leading is None ): leading = 2.0 * fontsize
    
    # ------------------------------------------------- #
    # --- [2] preparation of style                  --- #
    # ------------------------------------------------- #
    margins  = [ 15.0*mm, 15.0*mm, 15.0*mm, 15.0*mm ]
    doc      = SimpleDocTemplate( outFile, pagesize=portrait(A4),\
                                  leftMargin   =margins[0],
                                  bottomMargin =margins[1],
                                  rightMargin  =margins[2],
                                  topMargin    =margins[3] )
    pdfmetrics.registerFont( cidfonts.UnicodeCIDFont( "HeiseiMin-W3" ) )
    style_dict ={
        "name":"Normal",
        "fontName":"HeiseiMin-W3",
        "fontSize":fontsize,
        'borderWidth':0,
        'borderColor':None,
        "leading":leading,              # -- space between lines :: gyokan -- #
        "firstLineIndent":fontsize*1.0, # -- indent  -- #
    }
    style    = ParagraphStyle( **style_dict )
    Story    = []
    Story   += [ Spacer( width=1.0, height=5.0*mm ) ]

    # ------------------------------------------------- #
    # --- [3] pack texts                            --- #
    # ------------------------------------------------- #
    for ik,atext in enumerate( texts ):
        p = Paragraph( atext, style )
        Story += [ p ]
        if ( output_by_page ):
            Story += [ PageBreak() ]
        else:
            Story += [ Spacer( width=2*mm, height=6.0*mm ) ]

    # ------------------------------------------------- #
    # --- [4] build and return                      --- #
    # ------------------------------------------------- #
    doc.build( Story )
    print( "[convert__text2pdf.py] output file :: {} ".format( outFile ) )
    return()


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
    text_en = extract__textFromPDF( inpFile=input_pdfFile, outFile=english_txtFile, \
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
    convert__text2pdf( outFile=output_pdfFile, texts=text_stack, fontsize=fontsize )
    
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



