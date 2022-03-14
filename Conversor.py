import os
import easygui

from os import walk
import re
import sys, subprocess, shlex

#txtChangeFFMPEG = "Alterar\nlocal FFMPEG"
txtChangeIn = "Alterar\npasta de entrada" # change input folder
txtChangeOut = "Alterar\npasta de saída" # change output folder
txtCodec = "Selecionar\nCODEC" # select codec
txtQuali = "Selecionar\nQualidade" # select quality
txtSelectConvert = "Selecionar\ne converter" # select and convert
txtExit = "Sair" # exit

#default values
strInputFolder = "E:\\Users\\andre\\Videos"
strOutputFolder = "E:\\Users\\andre\\Videos"
strQuali = "30"
strQualis = ["10","20","27","30","40"] # possible qualities
strCodec = "hevc_nvenc"
strCodecs = ["hevc_nvenc","hevc_amf","h264_amf","libx265"] # possible codecs

# FFMPEG bin must be in PATH

# Change ffmpeg location
def change_ffmpeg_path() :
    global ffmpeg_bin
    global ffprobe_bin
    try:
        easygui.msgbox("Selecionar ffmpeg.exe...")
        strFFMPEG = easygui.fileopenbox("Selecionar ffmpeg.exe")
        if "ffmpeg.exe" not in strFFMPEG:
            easygui.msgbox("Selecionar corretamete o caminho do ffmpeg.exe!", "Warning!")
        else:
            ffmpeg_bin = strFFMPEG
        easygui.msgbox("Selecionar ffprobe.exe...")
        strFFPROBE = easygui.fileopenbox("Selecionar ffprobe.exe")
        if "ffprobe.exe" not in strFFPROBE:
            easygui.msgbox("Selecionar corretamete o caminho do ffprobe.exe!", "Warning!")
        else:
            ffprobe_bin = strFFPROBE
    except:
        easygui.msgbox("Erro ao configurar os arquivos do FFMPEG...", "ERRO!")
        exit()

# Change default input folder
def change_input_folder() :
    selected_folder = easygui.diropenbox("Caminho dos vídeos a serem convertidos:","Selecione",strInputFolder)
    if selected_folder == None:
        return(strInputFolder)
    else:
        return(selected_folder)

# Change default output folder
def change_output_folder() :
    selected_folder = easygui.diropenbox("Pasta de saída dos arquivos convertidos:","Selecione",strOutputFolder)
    if selected_folder == None:
        return(strOutputFolder)
    else:
        return(selected_folder)

# Codec selection
def change_codec() :
    selected_codec = easygui.choicebox("Qual codec deseja utilizar?", "Selecionar",choices=strCodecs)
    if selected_codec == None:
        return(strCodec)
    else:
        return(selected_codec)
        
# Quality selection
def change_quali() :
    selected_quali = easygui.choicebox("Qual qualidade deseja utilizar? (10 = pior e menor)", "Selecionar",choices=strQualis)
    if selected_quali == None:
        return(strQuali)
    else:
        return(selected_quali)

# Discovery codec from existing video files
def get_codec(filename):
    regex = r"codec_name=([a-z0-9]*)"
    cmnd = ['ffprobe', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-loglevel', 'quiet', strInputFolder+"\\"+filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    matches = re.finditer(regex, out.decode("utf-8"), re.MULTILINE)
    try:
        return(next(matches).group(1))
    except:
        return("erro")

# Dialog to allow user video input selection
def select_convert() :
    extensionsToCheck = ['.mkv', '.mp4', '.MP4', '.AVI', '.avi','.MOV']
    while True : 
        # List all files at input folder with video extentions.
        files_list = os.listdir(strInputFolder)
        choices_videos = []
        for file in files_list:
            if any(ext in file for ext in extensionsToCheck):
                choices_videos.append(file)
        videos = easygui.multchoicebox("Quais videos deseja converter? \n Barra de espaço para selecionar.", "Selecionar",choices=choices_videos)
        str = ""
        for video in videos:
            if any(ext in video for ext in extensionsToCheck):
                str = str + video + "::" + get_codec(video) + "\n"
        # Print files and current codecs
        if easygui.ynbox('Confirmar a seleção?\nArquivo::codec_atual\n\n'+str, 'Confirmação', ('Sim', 'Não')):
            for video in videos:
                if any(ext in video for ext in extensionsToCheck):
                    os.system("ffmpeg -i \""+strInputFolder+"\\"+video+"\" -c:v "+strCodec+" -cq "+strQuali+" -c:a copy \"" + strOutputFolder+"\\c_"+video+"\"")
            break;




def init_screen() :
    # message to be displayed 
    text = "Importante: FFMPEG deve estart no Path\n\nPastas com vídeos para converter: "+ strInputFolder +"\nPasta de saída: "+ strOutputFolder +"\nCodec: "+strCodec+"\nQualidade (1=pior): "+strQuali
    
    # window title
    title = "Conversor de videos"
    # button list
    button_list = []
    # appending button to the button list
    #button_list.append(txtChangeFFMPEG)
    button_list.append(txtChangeIn)
    button_list.append(txtChangeOut)
    button_list.append(txtCodec)
    button_list.append(txtQuali)
    button_list.append(txtSelectConvert)
    button_list.append(txtExit)
    
    # creating a button box
    return(easygui.buttonbox(text, title, button_list))

while (1):
    action = init_screen();

    #if (action == txtChangeFFMPEG):
    #    change_ffmpeg_path()
    if (action == txtChangeIn):
        strInputFolder = change_input_folder()
    if (action == txtChangeOut):
        strOutputFolder = change_output_folder()
    if (action == txtCodec):
        strCodec = change_codec()
    if (action == txtQuali):
        strQuali = change_quali()
    if (action == txtSelectConvert):
        select_convert()
    if (action == txtExit):
        exit()
