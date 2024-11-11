# A Tcl/Tk gadget to construct a window of buttons
# SD 20 Nov 2002


#######################################
####                               ####
#### Leave these lines unchanged   ####
####                               ####
#######################################
destroy  .buttons
toplevel .buttons
wm title .buttons "Buttons"
set count 0
proc add_button {title command} {
  global count
  button .buttons.$count -text $title -command $command
  pack   .buttons.$count -side top -pady 1 -padx 1 -fill x
  incr count
}

#######################################
####                               ####
####     Change these lines to     ####
####     add your own buttons      ####
####                               ####
#######################################
add_button "Resize Main" { wm geometry . 464x650+0+0  }
add_button "Hello"       { puts "Hello there"         }
add_button "Goodbye"     { puts "Cheerio"             }
add_button "Exit"        { exit                       }
