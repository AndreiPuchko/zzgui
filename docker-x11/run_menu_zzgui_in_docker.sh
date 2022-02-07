##
# Color  Variables
##
green=''
blue=''
yellow=''
clear=''

ColorGreen(){
	echo  $green$1$clear
}
ColorTitle(){
	echo  ''$1$clear
}

ColorYellow(){
    echo  $yellow$1$clear
}

RunZzGui()
{
docker run --rm -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -u zzgui \
    zzgui \
    python3 demo/${1-demo_07.py} /ini:none
}

menu(){
clear
echo  "
$(ColorTitle 'Input demo number an press Enter:')
$(ColorGreen '1)') basic: main menu, form & widgets
$(ColorGreen '2)') forms and forms in form
$(ColorGreen '3)') grid form (CSV data), automatic creation of forms based on data
$(ColorGreen '4)') progressbar, data loading, sorting and filtering
$(ColorGreen '5)') nonmodal form
$(ColorGreen '6)') code editor
$(ColorGreen '7)') database app (4 tables, mock data loading) - requires a zzdb package
$(ColorGreen '8)') database app, requires a zzdb package, autoschema
$(ColorGreen '0)') Exit
$(ColorYellow 'Choose an option:') "
        read a
        case $a in
            0) exit 0 ;;
	        *) RunZzGui demo_0$a.py; menu ;;
		#*) echo -e $red"Wrong option."$clear; WrongCommand;;
        esac
}
# Call the menu function
menu
