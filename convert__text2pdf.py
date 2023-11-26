import os, sys
from reportlab.pdfbase            import pdfmetrics, cidfonts
from reportlab.lib.styles         import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus           import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.pagesizes      import A4, mm, portrait

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
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    outFile = "pdf/sample.pdf"
    texts   = [ 60*"これはサンプルです.({})".format( ik ) for ik in range(6) ]
    
    convert__text2pdf( outFile=outFile, texts=texts )
    
