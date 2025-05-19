import random, zlib, base64
import os, pandas
from PIL import Image
import customtkinter as ct

#==========================================================
#============== Create Window/Widgets =====================
#==========================================================

ct.set_appearance_mode("system")

root = ct.CTk()
root.title("Encode")
root.geometry("650x530")
root.columnconfigure(0, weight= 1)
root.columnconfigure(1, weight= 3) #Window with 1x2 grid
root.rowconfigure(0, weight = 1)

optionFrame = ct.CTkFrame(root,corner_radius=0)
programFrame = ct.CTkFrame(root)

#--Theme Fonts--

bold = ct.CTkFont("Tw Cen MT",25,weight="bold")
normal = ct.CTkFont("Tw Cen MT",18)
normalBold = ct.CTkFont("Tw Cen MT",18,weight="bold")
boxFont = ct.CTkFont("Cascadia Code")
attFont = ct.CTkFont("Tw Cen MT Condensed",8)

#--Image Icons--

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Images")
txt = ct.CTkImage(light_image=Image.open(os.path.join(path,"txt.png")),dark_image=Image.open(os.path.join(path,"txt.png")),size=(25,25))
csv = ct.CTkImage(light_image=Image.open(os.path.join(path,"csv.png")),dark_image=Image.open(os.path.join(path,"csv.png")),size=(25,25))
json = ct.CTkImage(light_image=Image.open(os.path.join(path,"json.png")),dark_image=Image.open(os.path.join(path,"json.png")),size=(25,25))
html = ct.CTkImage(light_image=Image.open(os.path.join(path,"html.png")),dark_image=Image.open(os.path.join(path,"html.png")),size=(25,25))
xls = ct.CTkImage(light_image=Image.open(os.path.join(path,"xls.png")),dark_image=Image.open(os.path.join(path,"xls.png")),size=(25,25))

blankIm = ct.CTkImage(light_image=Image.new(mode="RGB",size=(0,0)),dark_image=Image.new(mode="RGB",size=(0,0)),size=(0,0))

#--Left Frame--

optionTitle = ct.CTkLabel(optionFrame,text="Options",font=bold)
modeTitle = ct.CTkLabel(optionFrame,text="Detected Cipher Range*",font=normal)
modeSelection = ct.CTkLabel(optionFrame,text="None",font=normal,fg_color=("#3b8ed0","#1f6aa5"),text_color="white",corner_radius=8,width=100)
spaceL = ct.CTkLabel(optionFrame,text="")
appearanceTitle = ct.CTkLabel(optionFrame,text="Set Appearance",font=normalBold)

#--Right Frame--

spaceR = ct.CTkLabel(programFrame,text="")
openName = ct.CTkLabel(programFrame,text="Open File to Begin",font=normal,image=blankIm,compound="center")

selectFrame = ct.CTkFrame(programFrame,fg_color="transparent")
detection = ct.CTkLabel(selectFrame,text="",text_color="green")
selection = ct.CTkSegmentedButton(selectFrame,values=["     Encode     ","     Decode     "],border_width=0,font=normal)
selection.set("     Encode     ")

textPreview = ct.CTkTextbox(programFrame,state="disabled",font=boxFont)
errorLabel = ct.CTkLabel(programFrame,text="",text_color="red")
attributionLabel = ct.CTkLabel(programFrame,text="Icons made by Smashicons from www.flaticon.com",font=attFont,text_color=("#c5c5c5","#474747"))

progressFrame = ct.CTkFrame(programFrame,fg_color="transparent")

#progressBar = ct.CTkProgressBar(programFrame,orientation="horizontal",width=370,progress_color=("#939ba2","#4a4d50"))

#==========================================================
#============== Create Processing Functions ===============
#==========================================================

def compress(int_list,bar = ct.CTkProgressBar):
    #Compresses list of integers into a single string
    array = []
    progress = 0
    for i in int_list:
        array.append(int(i))
        bar.set(progress / len(int_list))
        progress += 1
    int_list=array

    bitstream = 0
    progress = 0
    for num in int_list:
        bitstream = (bitstream << 12) | num
        bar.set(progress / len(int_list))
        progress += 1

    byte_len = (len(int_list) * 12 + 7) // 8
    packed_bytes = bitstream.to_bytes(byte_len, byteorder='big')

    compressed = zlib.compress(packed_bytes)
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded

def decompress(encoded,length,bar = ct.CTkProgressBar):
    #Decompresses string into list of integers
    compressed = base64.b64decode(encoded.encode('utf-8'))
    packed_bytes = zlib.decompress(compressed)

    bitstream = int.from_bytes(packed_bytes, byteorder='big')

    num_ints = int(length)
    int_list = []
    progress = 0
    for _ in num_ints:
        int_list.append((bitstream >> (12 * (num_ints - 1))) & 0xFFF)
        bitstream <<= 12
        bar.set(progress / num_ints)
        progress += 1
    
    progress = 0
    final = []
    for i in int_list:
        final.append(str(i).zfill(len(length.strip("0"))))
        bar.set(progress / len(int_list))
        progress += 1
    return final

dicKey = dict() #This will be the future encoding key
nums = [] #Randomized key
compressedNums = ""
ciLen = 0

def makeKey(string,bar = ct.CTkProgressBar): #Reads file to determine how large the cipher needs to be based on unicode characters
    n = 0
    progress = 0
    for i in string: #Finds max unicode character
        x = ord(i)
        if x > n:
            n = x
        bar.set(progress / len(string))
        progress += 1
    
    pad = len(str(n))
    global nums, dicKey, compressedNums,ciLen
    ciLen = n
    modeSelection.configure(text=str(n))

    progress = 0
    array = random.sample(range(n),n)
    for i in array:
        nums.append(str(i).zfill(pad)) #Creates a randomized, padded list of integers to based on max unicode number
        bar.set(progress / len(array))
        progress += 1
    
    bar2 = ct.CTkProgressBar(progressFrame,width=370,progress_color="green")
    bar2.set(0)
    bar2.pack()
    compressedNums = compress(nums,bar2)
    bar2.destroy()

    dicKey = dict(zip(range(1,n+1),nums)) #Creates a dictionary to match characters

#Encodes by matching each character to a randomized character and storing that key
def encode(string,bar = ct.CTkProgressBar):
    new = ""
    new += fileType.zfill(10) + str(ciLen).zfill(7) + str(len(compressedNums)).zfill(8) + compressedNums #Store the key
    progress = 0
    for char in string:
        num = ord(char)
        new += dicKey[num]
        bar.set(progress / len(string))
        progress += 1
    new = encodeHex(new) #Extra layer of encription to encode the key into hexidecimal
    return new

#Decodes by matching each randomized character to its normal counterpart
def decode(string = "",bar = ct.CTkProgressBar):
    new = ""
    string = decodeHex(string) #First decode the hexidecimal encoding
    ci = string[10:17]
    keyLength = int(string[17:25]) #Retrieve length of the compressed randomized list
    bar2 = ct.CTkProgressBar(progressFrame,width=370,progress_color="green")
    bar2.set(0)
    bar2.pack()
    oldNums = decompress(string[25:(keyLength+25)],ci,bar2) #Decompress randomized list
    bar2.destroy()

    key = dict(zip(oldNums,range(1,int(ci)+1))) #Generate key based on old list
    data = string[(keyLength+25):] #Retrieve the actual data to convert
    
    #Convert unicode characters back into normal script
    pad = len(ci.strip("0"))
    progress = 0
    for i in range(0,len(data),pad):
        code = data[i:i+pad]
        new += chr(key[code])
        bar.set(progress / len(data))
        progress += 1
    return new

#Converts string into hexidecimal by each character
def encodeHex(string):
    new = ""
    for char in string:
        new += format(ord(char),"x").zfill(3)
    return new

#Converts hexidecimal back into a string
def decodeHex(string):
    new = ""
    for i in range(0,len(string),3):
        chunk = string[i:i+3]
        new += chr(int(chunk,16))
    return new

#==========================================================
#============== Create Button Functions ===================
#==========================================================

fileName = ""
fileType = ""
data = ""

def modeSelect(input = ""): #Automatically selects encoding or decoding button based on file format
    if (input[:10].find(".") != -1) and (input[10:25].isdigit):
        selection.set("     Decode     ")
        modeSelection.configure(text="Decoding ({})".format(ciLen))
        detection.configure(text="File to Decode Found")
    else:
        selection.set("     Encode     ")
        detection.configure(text="File to Encode Found")

def openFile():
    errorLabel.configure(text="") #Clears errors/preview box
    textPreview.configure(state="normal")
    textPreview.delete("1.0",ct.END)
    textPreview.configure(state="disabled")

    bar = ct.CTkProgressBar(progressFrame,width=370,progress_color="green")
    bar.set(0)
    bar.pack()

    try:
        types = [("Text Files",".txt"),("CSV Files",".csv"),("JSON Files",".json"), #Accepted file formats
                ("HTML Files",".html"),("Excel Files",".xls .xlsx .xlsm .xlsb")]
        filePath = ct.filedialog.askopenfile("r",title="Select File",filetypes=types).name #Open file dialog box and get file path
        basename = os.path.basename(filePath) #Name of file
        openName.configure(text=basename)
        split = os.path.splitext(basename)
        global fileName,fileType, data
        fileName = split[0]
        fileType = split[1]

        readExtentions = [".txt",".csv",".json",".html"]
        excelExtentions = [".xls",".xlsx",".xlsm",".xlsb"]

        #Ensures file is opened properly by python
        if fileType in readExtentions:
            match fileType:
                case ".txt":
                    openName.configure(image=txt,compound="left")
                case ".csv":
                    openName.configure(image=csv,compound="left")
                case ".json":
                    openName.configure(image=json,compound="left")
                case ".html":
                    openName.configure(image=html,compound="left")
            with open(filePath,mode="r") as file:
                data = file.read()
                makeKey(data,bar)
                modeSelect(data)
        elif fileType in excelExtentions:
            openName.configure(image=xls,compound="left")
            data = str(pandas.read_excel(filePath))
            makeKey(data,bar)
            modeSelect(data)
        else:
            openName.configure(image=blankIm,compound="center",text="Open File to Begin") #Reset
            modeSelection.configure(text="None")
            errorLabel.configure(text="File Type Not Supported")
            detection.configure(text="")
    except AttributeError:
        openName.configure(image=blankIm,compound="center",text="Open File to Begin") #Reset
        modeSelection.configure(text="None")
        errorLabel.configure(text="File Not Opened")
        detection.configure(text="")
    bar.destroy()
    
def process(data):
    errorLabel.configure(text="")
    bar = ct.CTkProgressBar(progressFrame,width=370,progress_color="green")
    bar.set(0)
    bar.pack()
    try:
        if data != "":
            textPreview.configure(state="normal") #Clears preview box
            textPreview.delete("1.0",ct.END)
            text = ""
            if selection.get() == "     Encode     ":
                text = encode(data,bar) #Previews encoded data
            else:
                text = decode(data,bar) #Previews decoded data
            textPreview.insert("1.0",text)
            textPreview.configure(state="disabled")
        else:
            errorLabel.configure(text="No Data Read. Please Try Again.")
    except ValueError:
        errorLabel.configure(text="Invalid Decoding Values. Please Try Different File.")
    bar.destroy()

def download(input):
    errorLabel.configure(text="")
    try:
        text = textPreview.get("1.0",'end-1c')
        if  text != "":
            if selection.get() == "     Encode     ": #If file was encoded, download encoded data as .txt
                file = ct.filedialog.asksaveasfile(defaultextension=".txt",title="Select Folder to Download",filetypes=[("Text Files",".txt")])
                file.write(text)
            else:
                filetype = input[:10].lstrip("0") #If file was decoded, download decoded data in original format
                readExtentions = [".txt",".csv",".json",".html"]
                excelExtentions = [".xls",".xlsx",".xlsm",".xlsb"]

                #Ensures file is downloaded properly by python
                if filetype in readExtentions:
                    file = ct.filedialog.asksaveasfile(defaultextension=filetype,title="Select Folder to Download",filetypes=[("Original File Type",filetype)])
                    file.write(text)
                elif filetype in excelExtentions:
                    errorLabel.configure(text = "Excel Downloading Not Yet Implemented")
                else:
                    errorLabel.configure(text = "File Type Not Found or Supported")
        else:
            errorLabel.configure(text="No Data to Download")
    except AttributeError:
        errorLabel.configure(text="Download Incomplete. Please Try Again.")

def changeAppearance(choice):
    if choice == "Dark Mode":
        ct.set_appearance_mode("dark")
    else:
        ct.set_appearance_mode("light")

def close():
    root.destroy()

def about(): #Creates a new window that gives basic information
    aboutWindow = ct.CTk()
    aboutWindow.geometry("500x450")
    aboutWindow.title("About Me")

    line1 = "Steps to use encoding program:"
    line2 = "1) Open the file to process using the 'Open File' button \n" \
            "2) Encoding or decoding will automatically be detected \n" \
            "    but can still be manually changed \n" \
            "3) Press 'Run' \n" \
            "4) Download the new data by pressing 'Download'"
    line3 = "*Cipher Range Information:"
    line4 = "The number tells the program how long the key list \n" \
            "should be, with the length representing the max \n" \
            "unicode character found within the file"
    line5 = "0-127: US ASCII (Standard Alphabet and Symbols) \n" \
            "128-2047: Most Latinic Alphabets (Arabic, Greek, etc.) \n" \
            "2018-65535: Additional Languages (Chinese, Japanese, etc.)** \n" \
            "65536-1114111: Other (More Asian Characters, Emojis, etc.)** \n" \
            "\n" \
            "**!!WARNING!! Numbers in higher ranges cause the program \n" \
            "    to slow down or even crash"

    label1 = ct.CTkLabel(aboutWindow,text=line1,font=normalBold)
    label2 = ct.CTkLabel(aboutWindow,text=line2,font=normal,justify="left")
    label3 = ct.CTkLabel(aboutWindow,text=line3,font=normalBold)
    label4 = ct.CTkLabel(aboutWindow,text=line4,font=normal,justify="left")
    label5 = ct.CTkLabel(aboutWindow,text=line5,font=normal,justify="left")
    
    space = ct.CTkLabel(aboutWindow,text="")

    label1.pack(anchor="w",padx=15,pady=5)
    label2.pack(anchor="w",padx=15)
    space.pack()
    label3.pack(anchor="w",padx=15,pady=8)
    label4.pack(anchor="w",padx=15)
    label5.pack(anchor="w",padx=15,pady=5)

    aboutWindow.mainloop()

#==========================================================
#============== Place Left Frame (Options) ================
#==========================================================

optionTitle.pack(pady=25)
openButton = ct.CTkButton(optionFrame,text="Open File",command=openFile,font=normal)
openButton.pack()

modeTitle.pack(pady=10)
modeSelection.pack()

spaceL.pack(pady=15)

appearanceTitle.pack(pady=15)
appearanceSelect = ct.CTkOptionMenu(optionFrame, values=["Dark Mode","Light Mode"],command=changeAppearance,font=normal)
appearanceSelect.pack()

exitButton = ct.CTkButton(optionFrame,text="Exit",command=close,fg_color=("#909090","#616161"),hover_color=("#616161","#424242"),font=normal)
exitButton.pack(side="bottom",pady=20)

helpButton = ct.CTkButton(optionFrame,text="Help",command=about,font=normal)
helpButton.pack(side="bottom")

optionFrame.grid(row=0,column=0,sticky="nsew")

#==========================================================
#============== Place Right Frame (Program) ===============
#==========================================================

spaceR.pack()
openName.pack()

detection.pack(anchor="w")
selection.pack(side="left")
button = ct.CTkButton(selectFrame, text="Run", command=lambda:process(data),width=80,font=normal)
button.pack(side="right")
selectFrame.pack(anchor="w",pady=10,padx=15,fill="both")

textPreview.pack(anchor="w",padx=15,fill="x")
downloadButton = ct.CTkButton(programFrame, text="Download", command=lambda:download(data),font=normal)
downloadButton.pack(pady=10)

progressFrame.pack()

errorLabel.pack(anchor="nw",padx=15,pady=10)

attributionLabel.pack(anchor="w",side="bottom",pady=1,padx=10)

programFrame.grid(row=0,column=1,sticky="nsew",padx=20,pady=20)

root.mainloop()
