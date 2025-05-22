import random, zlib, base64, json
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
jsonI = ct.CTkImage(light_image=Image.open(os.path.join(path,"json.png")),dark_image=Image.open(os.path.join(path,"json.png")),size=(25,25))
html = ct.CTkImage(light_image=Image.open(os.path.join(path,"html.png")),dark_image=Image.open(os.path.join(path,"html.png")),size=(25,25))
xls = ct.CTkImage(light_image=Image.open(os.path.join(path,"xls.png")),dark_image=Image.open(os.path.join(path,"xls.png")),size=(25,25))

blankIm = ct.CTkImage(light_image=Image.new(mode="RGB",size=(0,0)),dark_image=Image.new(mode="RGB",size=(0,0)),size=(0,0))

#--Left Frame--

optionTitle = ct.CTkLabel(optionFrame,text="Options",font=bold)

infoTitle = ct.CTkLabel(optionFrame,text="Key Information*",font=normalBold)

infoFrame = ct.CTkFrame(optionFrame,fg_color="transparent")
infoFrame.columnconfigure((0,1),weight=1)
infoFrame.rowconfigure((0,1),weight=1)

klLabel = ct.CTkLabel(infoFrame,text="Key Length:   ",font=normal)
keyLen = ct.CTkLabel(infoFrame,text="0",font=normal,fg_color=("#3b8ed0","#1f6aa5"),text_color="white",corner_radius=8,width=20)
maxLabel = ct.CTkLabel(infoFrame,text="Max Unicode:   ",font=normal)
maxUL = ct.CTkLabel(infoFrame,text="0",font=normal,fg_color=("#3b8ed0","#1f6aa5"),text_color="white",corner_radius=8,width=20)

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

#Compresses dictionary into a single string
def compress(dic: dict):
    json_str = json.dumps(dic,ensure_ascii=False)         # Convert dict to JSON string
    compressed = zlib.compress(json_str.encode('utf-8')) # Compress bytes
    encoded = base64.b64encode(compressed).decode('utf-8')  # Base64 encode to make it string-safe
    return encoded


#Decompresses string into dictionary
def decompress(encoded: str):
    compressed = base64.b64decode(encoded.encode('utf-8')) # Decode base64
    json_str = zlib.decompress(compressed).decode('utf-8') # Decompress to JSON string
    return json.loads(json_str)



dicKey = dict() #This will be the future encoding key
compressed = ""
pad = 0

#Informational Variables (for window display only)
maxUni = 0
dicLen = 0


def makeKey(string,bar = ct.CTkProgressBar): #Reads file to determine how large the cipher needs to be based on unicode characters
    n = []
    p = 0
    progress = 0
    for i in string:
        x = ord(i)
        if x not in n: #Adds every unique unicode character to key
            n.append(x)
        if x > p: #Finds max unicode character
            p = x
        bar.set(progress / len(string))
        progress += 1
    n.sort()

    global dicKey, compressed, pad, maxUni, dicLen
    pad = len(str(p))
    maxUni = p
    dicLen = len(n)
    keyLen.configure(text=str(dicLen))
    maxUL.configure(text=str(maxUni))

    progress = 0
    rand = random.sample(range(p),len(n))
    rand = list(map(lambda x:str(x).zfill(pad),rand))

    dicKey = dict(zip(n,rand)) #Creates a dictionary to match characters
    compressed = compress(dicKey)


#Encodes by matching each character to a randomized character and storing that key
def encode(string,bar = ct.CTkProgressBar):
    new = ""
    new += fileType.zfill(10) + str(len(compressed)).zfill(8) + str(pad) + compressed #Store the key
    progress = 0
    for char in string:
        num = ord(char)
        new += dicKey[num]
        bar.set(progress / len(string))
        progress += 1
    new = encodeHex(new) #Extra layer of encription to encode the key into hexidecimal
    global downData
    downData = new
    return new


downData = ""

#Decodes by matching each randomized character to its normal counterpart
def decode(string = "",bar = ct.CTkProgressBar):
    new = ""
    string = decodeHex(string) #First decode the hexidecimal encoding
    keyLength = int(string[10:18]) #Retrieve length of the compressed dictionary
    oPad = int(string[18:19])

    oldNums = decompress(string[19:(keyLength+19)]) #Decompress dictionary
    key = {v: k for k, v in oldNums.items()}

    data = string[(keyLength+19):] #Retrieve the actual data to convert
    
    #Convert unicode characters back into normal script
    progress = 0
    for i in range(0,len(data),oPad):
        code = data[i:i+oPad]
        new += chr(int(key[code]))
        bar.set(progress / len(data))
        progress += 1
    global downData
    downData = new
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
    try:
        input = decodeHex(input)
        if (input[:10].find(".") != -1) and (input[10:25].isdigit):
            selection.set("     Decode     ")
            detection.configure(text="File to Decode Found")
        else:
            selection.set("     Encode     ")
            detection.configure(text="File to Encode Found")
    except ValueError:
        pass

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
                    openName.configure(image=jsonI,compound="left")
                case ".html":
                    openName.configure(image=html,compound="left")
            with open(filePath,mode="r", encoding="utf-8") as file:
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
            keyLen.configure(text="0")
            maxUL.configure(text="0")
            errorLabel.configure(text="File Type Not Supported")
            detection.configure(text="")
    except AttributeError:
        openName.configure(image=blankIm,compound="center",text="Open File to Begin") #Reset
        keyLen.configure(text="0")
        maxUL.configure(text="0")
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
        text = downData
        if  text != "":
            if selection.get() == "     Encode     ": #If file was encoded, download encoded data as .txt
                file = ct.filedialog.asksaveasfile(defaultextension=".txt",title="Select Folder to Download",filetypes=[("Text Files",".txt")])
                file.write(text)
            else:
                input = decodeHex(input)
                filetype = input[:10].lstrip("0") #If file was decoded, download decoded data in original format
                readExtentions = [".txt",".csv",".json",".html"]
                excelExtentions = [".xls",".xlsx",".xlsm",".xlsb"]

                #Ensures file is downloaded properly by python
                if filetype in readExtentions:
                    file = ct.filedialog.asksaveasfilename(defaultextension=filetype,title="Select Folder to Download",filetypes=[("Original File Type",filetype)])
                    with open(file,"w",encoding="utf-8") as file:
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
    aboutWindow.geometry("500x520")
    aboutWindow.title("About Me")

    line1 = "Steps to use encoding program:"
    line2 = "1) Open the file to process using the 'Open File' button \n" \
            "2) Encoding or decoding will automatically be detected \n" \
            "    but can still be manually changed \n" \
            "3) Press 'Run' \n" \
            "4) Download the new data by pressing 'Download'"
    line3 = "*Key Information:"
    line4 = "''Key Length'' is how long the cipher key is, aka how many \n" \
            "unique characters are present within the file. \n" \
            "''Max Unicode'' is the highest unicode character found, which \n" \
            "will affect the total encoded file size due to padding."
    line5 = "Unicode Characters:"
    line6 = "0-127: US ASCII (Standard Alphabet and Symbols) \n" \
            "128-2047: Most Latinic Alphabets (Arabic, Greek, etc.) \n" \
            "2018-65535: Additional Languages (Chinese, Japanese, etc.)** \n" \
            "65536-1114111: Other (More Asian Characters, Emojis, etc.)** \n" \
            "\n" \
            "**!!WARNING!! Large files can cause the program \n" \
            "    to slow down or even crash"

    label1 = ct.CTkLabel(aboutWindow,text=line1,font=normalBold)
    label2 = ct.CTkLabel(aboutWindow,text=line2,font=normal,justify="left")
    label3 = ct.CTkLabel(aboutWindow,text=line3,font=normalBold)
    label4 = ct.CTkLabel(aboutWindow,text=line4,font=normal,justify="left")
    label5 = ct.CTkLabel(aboutWindow,text=line5,font=normalBold,justify="left")
    label6 = ct.CTkLabel(aboutWindow,text=line6,font=normal,justify="left")
    
    space = ct.CTkLabel(aboutWindow,text="")

    label1.pack(anchor="w",padx=15,pady=5)
    label2.pack(anchor="w",padx=15)
    space.pack()
    label3.pack(anchor="w",padx=15,pady=8)
    label4.pack(anchor="w",padx=15)
    label5.pack(anchor="w",padx=15,pady=5)
    label6.pack(anchor="w",padx=15)

    aboutWindow.mainloop()

#==========================================================
#============== Place Left Frame (Options) ================
#==========================================================

optionTitle.pack(pady=20)
openButton = ct.CTkButton(optionFrame,text="Open File",command=openFile,font=normal)
openButton.pack(pady=10)

infoTitle.pack()
klLabel.grid(row=0,column=0,sticky="w")
keyLen.grid(row=0,column=1)
maxLabel.grid(row=1,column=0,sticky="w")
maxUL.grid(row=1,column=1)
infoFrame.pack(pady=10)

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
