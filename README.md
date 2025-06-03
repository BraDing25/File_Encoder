# File Encoder
This project was made to develop my skills in file handling and manipulation. It takes an input from a file and encodes the characters based on a randomized unicode cipher and allows for the downloading of both the encoded and decoded formats.

## Major Changes Between Old and New Versions

This encoding script follows after its predacessor but was made completely from stratched and every mechanism completely revamped.
1. Allows for more file types (.txt, .csv, .json, .html, .xlsx, .xls, .xlsm, .xlsb)
2. Encodes not just letters and numbers, but thousands of different characters
3. Cipher isn't pre-made but randomly generated every time the program is ran
4. Complete UI overhaul to look much nicer

## How It's Made

Packages Used: Python, zlib, base64, os, pandas, PIL Image, customtkinter

Firstly, the program begins by having the user open a file, allowing for only specific extensions. Once the file is read, the user has the option to encode or decode depending on what type of data is being read, and once that has run then they have the option to download the file.

The program works by first generating a randomized key based on the unique unicode characters found and compressing it, allowing for much more variety of text, which will later be used to encode and decode the data. The encoding process begins by first storing the file extension and the compressed key for future access. Next it goes through every character in the string of data to convert it to its unicode number, and matching it with the generated key. The last step of the encoding process is to encode it once again but into a hexidecimal format so the final encoded data is one single format and completely unrecognizable. The decoding process is the exact same just reversed; convert hexidecimal into normal text, retrieve the key that was used, then match the encoded numbers to the cipher.

Every other function in the stript is for the UI such as the button to open files that will show the right name with the correct extension icon, etc.

## Lessons Learned

I learned how to manipulate more than just .txt files but also various other text-related file formats as well as Excel. Additionally, I learned about conversions of characters and things such as bytes or unicode characters, and how to convert from one form to another. Lastly I learned more UI building techniques using customtkinter.

## Changelog:
v1.2:
- Changed dictionaries to only use the unique unicode characters present rather than every unicode character within a range to save on space
- Added information displays to show the length of the key and max unicode character found
- Updated help menu accordingly

v1.1: 
- Reordered sections 
- Removed unneccesary code 
- Changed key from looped arrays to dictionaries 
- Changed UI code to be more consistant 
- Added automatic encode/decode detection 
- Added automatic max unicode detection (used to generate key length and save space)* 
- Added progress bar 
- Updated help menu accordingly

*This new unicode detection changes the key from default being a length of 2048 (unicode characters that include majority of written text) to a system that automatically finds the largest unicode character in the text, and makes a key of that length, since the program will never have to worry about a character being larger than that, drasitcally reducing the size of the key

## Future Updates

Add more file formats, store key outside of file so there is an actual layer of security since right now there is none

## How to Use

Simply run the script
