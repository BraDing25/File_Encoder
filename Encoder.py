import random, zlib, base64
import os, pandas
from PIL import Image
import customtkinter as ct

#============== Create Processing Functions ===============

def compress(int_list):
    #Compresses list of integers into a single string
    bitstream = 0
    for num in int_list:
        bitstream = (bitstream << 12) | num

    byte_len = (len(int_list) * 12 + 7) // 8
    packed_bytes = bitstream.to_bytes(byte_len, byteorder='big')

    compressed = zlib.compress(packed_bytes)
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded

def decompress(encoded):
    #Decompresses string into list of integers
    compressed = base64.b64decode(encoded.encode('utf-8'))
    packed_bytes = zlib.decompress(compressed)

    bitstream = int.from_bytes(packed_bytes, byteorder='big')

    num_ints = 2048
    int_list = []
    for _ in range(num_ints):
        int_list.append((bitstream >> (12 * (num_ints - 1))) & 0xFFF)
        bitstream <<= 12
    return int_list

array = [] #This will be the future encoding key
nums = random.sample(range(2048),2048) #Randomized key
compressedNums = compress(nums)

for i in range(2048):
  array.append([str(i).zfill(4),str(nums[i]).zfill(4)]) #Populates key with unicode number and matching randomized number

#Encodes by matching each character to a randomized character and storing that key
def encode(string):
    new = ""
    new += fileType.zfill(10) + str(len(compressedNums)).zfill(8) + compressedNums #Store the key
    for char in string:
        num = ord(char)
        n = str(num).zfill(4)
        for i in array: #Match unicode character to key list
            if n in i:
                if i[0] == n:
                    new += i[1]
    new = encodeHex(new) #Extra layer of encription to encode the key into hexidecimal
    return new

#Decodes by matching each randomized character to its normal counterpart
def decode(string = ""):
    new = ""
    string = decodeHex(string) #First decode the hexidecimal encoding
    keyLength = int(string[10:18]) #Retrieve length of the compressed randomized list
    oldNums = decompress(string[18:(keyLength+18)]) #Decompress randomized list
    key = []
    for i in range(2048): #Generate key based on decompressed list
        key.append([str(i).zfill(4),str(oldNums[i]).zfill(4)])
 
    data = string[(keyLength+18):] #Retrieve the actual data to convert
    
    #Convert unicode characters back into normal script
    for i in range(0,len(data),4):
        code = data[i:i+4]
        for k in key:
            if code in k:
                if k[1] == code:
                    new += chr(int(k[0]))
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

#============== Create Window/Widgets ===============

ct.set_appearance_mode("system")

root = ct.CTk()
root.title("Encode")
root.geometry("620x500")
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

#--Left Frame--

optionTitle = ct.CTkLabel(optionFrame,text="Options",pady=25,font=bold)
appearanceTitle = ct.CTkLabel(optionFrame,text="Set Appearance",pady=15,font=normalBold)

#--Right Frame--

openFrame = ct.CTkFrame(programFrame,fg_color="transparent")
openName = ct.CTkLabel(openFrame,text=" Open File to Begin",font=normal)
#openImage = ct.CTkLabel(openFrame)

selectFrame = ct.CTkFrame(programFrame,fg_color="transparent")
selection = ct.CTkSegmentedButton(selectFrame,values=["     Encode     ","     Decode     "],border_width=0,font=normal)
selection.set("     Encode     ")

textPreview = ct.CTkTextbox(programFrame,state="disabled",font=boxFont)
errorLabel = ct.CTkLabel(programFrame,text="",text_color="red")
attributionLabel = ct.CTkLabel(programFrame,text="Icons made by Smashicons from www.flaticon.com",font=attFont,text_color="#474747")

#============== Create Button Functions ===============

fileName = ""
fileType = ""
data = ""

def openFile():
    errorLabel.configure(text="") #Clears errors/preview box
    textPreview.configure(state="normal")
    textPreview.delete("1.0",ct.END)
    textPreview.configure(state="disabled")

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
        elif fileType in excelExtentions:
            openName.configure(image=xls,compound="left")
            data = str(pandas.read_excel(filePath))
        else:
            openName.configure(image="",text="Open File to Begin")
            errorLabel.configure(text="File Type Not Supported")
    except AttributeError:
        openName.configure(image="",text="Open File to Begin")
        errorLabel.configure(text="File Not Opened")
    

def process(data):
    errorLabel.configure(text="")
    try:
        if data != "":
            textPreview.configure(state="normal") #Clears preview box
            textPreview.delete("1.0",ct.END)
            text = ""
            if selection.get() == "     Encode     ":
                text = encode(data) #Previews encoded data
            else:
                text = decode(data) #Previews decoded data
            textPreview.insert("1.0",text)
            textPreview.configure(state="disabled")
        else:
            errorLabel.configure(text="No Data Read. Please Try Again.")
    except ValueError:
        errorLabel.configure(text="Invalid Decoding Values. Please Try Different File.")

def download(input):
    errorLabel.configure(text="")
    try:
        text = textPreview.get("1.0",'end-1c')
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
    aboutWindow.geometry("430x200")
    aboutWindow.title("About Me")

    line1 = "Steps to use encoding program:"
    line2 = "1) Open the file to process using the 'Open File' button"
    line3 = "2) Select whether to encode or decode"
    line4 = "3) Press 'Run'"
    line5 = "4) Download the new data by pressing 'Download'"

    label1 = ct.CTkLabel(aboutWindow,text=line1,font=normalBold)
    label2 = ct.CTkLabel(aboutWindow,text=line2,font=normal)
    label3 = ct.CTkLabel(aboutWindow,text=line3,font=normal)
    label4 = ct.CTkLabel(aboutWindow,text=line4,font=normal)
    label5 = ct.CTkLabel(aboutWindow,text=line5,font=normal)
    
    label1.pack(anchor="w",padx=15,pady=5)
    label2.pack(anchor="w",padx=15)
    label3.pack(anchor="w",padx=15)
    label4.pack(anchor="w",padx=15)
    label5.pack(anchor="w",padx=15)

    aboutWindow.mainloop()

#============== Place Left Frame (Options) ===============

optionTitle.pack()
openButton = ct.CTkButton(optionFrame,text="Open File",command=openFile,font=normal)
openButton.pack()
appearanceTitle.pack()
appearanceSelect = ct.CTkOptionMenu(optionFrame, values=["Dark Mode","Light Mode"],command=changeAppearance,font=normal)
appearanceSelect.pack()

exitButton = ct.CTkButton(optionFrame,text="Exit",command=close,fg_color="#616161",hover_color="#424242",font=normal)
exitButton.pack(side="bottom",pady=20)
helpButton = ct.CTkButton(optionFrame,text="Help",command=about,font=normal)
helpButton.pack(side="bottom")

optionFrame.grid(row=0,column=0,sticky="nsew")

#============== Place Right Frame (Program) ==============

#openImage.pack(side="left",fill="both")
openName.pack(side="left")
openFrame.pack(pady=10)

selection.pack(side="left")
button = ct.CTkButton(selectFrame, text="Run", command=lambda:process(data),width=80,font=normal)
button.pack(side="right")
selectFrame.pack(anchor="w",pady=10,padx=15,fill="both")

textPreview.pack(anchor="w",padx=15,fill="x")
downloadButton = ct.CTkButton(programFrame, text="Download", command=lambda:download(data),font=normal)
downloadButton.pack(pady=10)

errorLabel.pack(anchor="nw",padx=15)

attributionLabel.pack(anchor="w",side="bottom",pady=1,padx=10)

programFrame.grid(row=0,column=1,sticky="nsew",padx=20,pady=20)

root.mainloop()


