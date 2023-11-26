import os, sys, subprocess


# ========================================================= #
# ===  execute emacs indentation                        === #
# ========================================================= #
def indent__usingEmacs( inpFile=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments Check                       --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[indent__usingEmacs] inpFile == ???" )

    emacs_lisp_command = \
        """
        (defun emacs-format-function ()
        "Format the whole buffer."
        (mark-whole-buffer)
        (indent-region (point-min) (point-max) nil)
        (untabify (point-min) (point-max))
        (delete-trailing-whitespace)
        (save-buffer)
        )
        """
    lspFile = "indent__usingEmacs.lsp"
    with open( lspFile, "w" ) as f:
        f.write( emacs_lisp_command )
    
    # ------------------------------------------------- #
    # --- [2] execute indentation                   --- #
    # ------------------------------------------------- #
    cmd = "emacs -batch {0} -l {1} -f emacs-format-function".format( inpFile, lspFile )
    print( cmd )
    subprocess.call( cmd.split() )
    # ------------------------------------------------- #
    # --- [3] remove lspFile & backupFile           --- #
    # ------------------------------------------------- #
    backupFile = "{0}~".format( inpFile )
    if ( os.path.exists( backupFile ) ):
        cmd = "rm {0}".format( backupFile )
        print( cmd )
        subprocess.call( cmd.split() )
    if ( os.path.exists( lspFile ) ):
        cmd = "rm {0}".format( lspFile )
        print( cmd )
        subprocess.call( cmd.split() )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    inpFile = "sample.vts"
    indent__usingEmacs( inpFile=inpFile )
