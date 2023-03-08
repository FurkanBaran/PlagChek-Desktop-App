'''
PlagCheck by Furkan Baran

Instant plagiarism check for documents.
Detects plagiarism between the selected document and the selected sources.
Detects plagiarism, shows plagiarism rate, shows location of plagiarism in documents

https://github.com/FurkanBaran

'''

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter import messagebox
import string

def open_file():
    filepath = askopenfilename(  filetypes=[("Text Files", "*.txt"),
                                                ("All Files", "*.*")]   ) # File browser, it returns file's path.
    if not filepath:                                                      # if no file is selected: just return 
        return
    text.clear()                                                          # clear the main text list
    text_gui.clear()                                                      # clear main text_gui list 
    text_file=open(filepath,'r',encoding="utf-8")                         # open selected file as reading mode
    text_lines=text_file.readlines()                                      # read lines
    word_id=0                                                             # words count variable
    for line in text_lines:                                               # for each line 
        for word in  line.split():                                                              # for each word
                text.append( (word.translate(str.maketrans('','',  r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~‘’“”""")) ).lower())   # append the word's simple and lowercase version (without punctuation) to text list
                text_gui.append([word,False, False])                                                # append the word and its plagiarism values (false initially) to text_gui list
                word_id+=1                                                                          # increase the word id (index) by 1
        text_gui[word_id-1][2]=True                                                             # set newline for this word as True
    printer(-1)                                                                             # print main text
    window.title(f"Plagiarism  Check - {filepath}")                                         # Set window title as "Plagiarism  Check - FilePath"
    text_file.close()                                                                       # close the file
    
def open_files():                       # open multiple files for data to be compared.
    filepaths = askopenfilenames( filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")] )  # filepaths list for selected files paths
    if not filepaths:                   # if no files selected
        return                          # just return
    db_gui.clear()                      # clear the db_gui list
    db_text.clear()                     # clear the db_text list
    file_id=0                           # star file_id from 0
    file_dict.clear()
    for filepath in filepaths:          # for each file's path
        db_text.append([])                                          # add new dimension for this file to db_text 
        db_gui.append([])                                           # and db_gui
        filename=filepath.split('/')[  len(filepath.split('/'))-1 ] # get filename from filepath
        file_dict[filename]=file_id                                 # file_dict: set file_id value for this 'filename' key
        file=open(filepath,'r',encoding='utf-8')                    # open file as reading mode
        text_lines=file.readlines()                                 # get text lines
        word_id=0                                                   # start word_id from 0
        for line in text_lines:                #for each line
            for word in line.split():                   # for each word
                db_gui[file_id].append([word, 0,False]) # append the word to db_gui list
                db_text[file_id].append((word.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”"""))).lower()) # append the word's simple and lowercase word (without punctuation) to db_text list
                word_id+=1                              # increase  word_id by 1
            db_gui[file_id][word_id-1][2]=True          # set newline value for last word to True
        file.close()                             # close this file
        file_id+=1                               # increase file_id by 1
    file_menu['values']=[*file_dict]           # set file_menu list (combobox menu) as file_dict's keys
    btn_go.config(state="normal")              # enable "Go to file" button 
    file_menu.set([*file_dict][0])             # set file_menu combobox to first file
    printer(0)                                 # print the first file to text compare widget

def check():
    window.config(cursor="watch")
    if  (not text  or  not db_text):           # if text or db_text are empty: print error message
        messagebox.showerror("Error","Select required files to compare")
        window.config(cursor="")
        return 1
    N=int(N_menu.get())                        # get N (level) value from N_menu 
    n=N-1;
    check_text=[]                              # list of words to search ( N elements ) 
    for i in range(N-1):                       # append first N-1 word to check_text list (last one will appended in for loop)
        check_text.append(text[i])
    text_len=len(text)                         # length of text list
    #### Searches db_text for every N consecutive words in text ####
    for id in range(text_len - n):     # for each "text" list word's index, expect last N-1 words to prevent list from being out of range
        check_text.append(text[id+ n ])      # update the check_text by adding the next word each loop  
        for file_id in range( len(db_text) ):      # for each file  (index)
            for j in range ( len(db_text[file_id]) - n ):  # for each word's index, expect last N-1 words to prevent list from being out of range
                if check_text==db_text[file_id][j:j+N]:        # if check_text and N consecutive words in db_text are equal (j is first word's index):
                    for k in range(N):                           # set Plagiarism  value for these N words in gui lists (text_gui and db_gui) as True (or 1)
                        text_gui[id+k][1]=True
                        db_gui[file_id][j+k][1]=1
        check_text.pop(0)                                # remove first word in check_text list each loop         
    btn_search.config(state="normal")                        # set "search" button as enabled (clickable)
    printer(0)                                             # print the first db file to comp_text_widget
    printer(-1)                                            # print the main text to main_text_widget
    window.config(cursor="")
    ##### Cleaning GUI values #####
    for id in range(text_len - n):    
        text_gui[id][1]=False
    for file_id in range( len(db_gui) ):
        for j in range( len(db_gui[file_id]) ):
            db_gui[file_id][j][1]=0
    return 0
 
def search():                                                         # this function gets a string from selected text in main text widget, and searchs it from db_text
                                                                      # marks this string in db_text as 2 (means it is found)  
    if main_text_widget.tag_ranges("sel"):                            # if there is "selected text"
        selected_text=main_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST) # assign it to selected_text
    else:
        messagebox.showerror("Error", "Please select text first.")  # else show error message
        return 1

    selected_text_list=[ (x.translate(str.maketrans('', '', string.punctuation))  ).lower()             # create a selected_text_list with words in selected_text 
                            for x in selected_text.split() ]                                            # but words are simple (without punctuation) and lowercase to make it easy to compare
    n=len(selected_text_list) # counts of selected words, kind of local N
    # search loop: same as check() but it returns when selected text is found
    for file_id in range( len(db_text)):                            # for each file (by index) in db_text
        for j in range ( len( db_text[file_id]) - ( n-1 ) ):        # for each this file's word except last (n-1) ones
            if selected_text_list==db_text[file_id][j:j+n]:         # if selected_text_list and n consecutive words in this file are equal (j is first word's id):
                for k in range(n):                                  # set "Plagiarism" value for these n words in db_gui as 2 (means "Found")
                    db_gui[file_id][j+k][1]=2
                printer(file_id)                                    # print this file in comp_text_widget
                return  0                                           # return function
    messagebox.showerror("Error: Not Found!", "Please select different text that contains plagiarism.") # if not found, show error message
    return 1
            
def printer(fileid):                        # this function gets fileid integer and prints corresponding file (in db_gui) with words according their Plagiarism value
    if fileid == -1:                         # if fileid is -1, prints main text to main text widget
        main_text_widget.delete("1.0",tk.END)
        text_len=len(text)
        plag_count=0                                               # counts of words with Plagiarism ratio is True 
        ## *** Printing the text to main text widget *** ##
        for word in range(text_len):                                                  # for each word in "text" list
            if text_gui[word][1]==False:                                              # if Plagiarism ratio is False insert to main text areea as normal text
                main_text_widget.insert(tk.END, text_gui[word][0]+" ", 'normal')
            else:                                                                     # else insert it as red color and increase count by 1
                main_text_widget.insert(tk.END, text_gui[word][0] +" ", 'plagiarism')
                plag_count+=1 
            if text_gui[word][2]==True:                                               # if this word's index marked as newline, insert a newline to text widget
                main_text_widget.insert(tk.END, "\n", 'normal')
            p_ratio=(plag_count/text_len)*100
            ratio['value']=p_ratio                                                    # set ratio bar value to 100*Plagiarism ratio
            ratio_label.config (text=f"Plagiarism Ratio: {p_ratio:.2f}%")             # update Plagiarism ratio label
    else:
        comp_text_widget.delete("1.0",tk.END)    # delete comp_text_widget
        lenn=len(db_gui[fileid])                # length of file's word list
        for word in range(lenn):                # for each word (index)
            if db_gui[fileid][word][1]==0:      # if word's Plagiarism value is 0, insert it as normal text
                comp_text_widget.insert(tk.END,db_gui[fileid][word][0]+" ", 'normal')
            elif db_gui[fileid][word][1]==1:    # if word's Plagiarism value is 1, insert it as plagiarism text (bold)
                comp_text_widget.insert(tk.END, db_gui[fileid][word][0] +" ", 'plagiarism')
            else:                               # if word's Plagiarism value is 2, insert it as found text (marked as black)
                comp_text_widget.insert(tk.END, db_gui[fileid][word][0] +" ", 'found')
            if  db_gui[fileid][word][2]==1:     # # if word's newLine value is 1, insert a new line
                comp_text_widget.insert(tk.END,  "\n", 'normal')
    return 0

N=3 
text=[]         # main text list, [word]
text_gui=[]     # main text list for gui, [word, isPlagiarism, newLine ]
db_text=[]      # database text list    [File] [Word] 
db_gui=[]       # db text list for gui, [File] [word, isPlagiarism, newLine ]
file_dict={}    # file list dictionary, keys=file name, values=file id

# Main window
window = tk.Tk() # Open new window
window.title("Plagiarism Check") # Set window's title
# # Main window conf.
window.rowconfigure(0, minsize=800, weight=1) 

# # Left side ( Button Frame)
btn_frame = tk.Frame(window, relief=tk.RAISED, bd=4)
# #  Right side Button widgets
btn_file = tk.Button(btn_frame,  text="Import Text File" , command=open_file)     # Open file button: runs open_file() func
btn_files = tk.Button(btn_frame, text="Import Data Files", command=open_files)    # Open files button: runs open_files() func
# # # N Selecting Label
N_label=tk.Label(btn_frame, text="Select Level")
# # # N Selecting default int variable
default_N = tk.IntVar(window)
default_N.set(3)
# # # N Selecting Combobox
N_menu = ttk.Combobox(btn_frame, state="readonly",  textvariable= default_N)
N_menu['values']=[3,4,5,6,7]
btn_check = tk.Button(btn_frame, text="Check",  command=check)                    # Check button: runs check() func
btn_search = tk.Button(btn_frame,  state="disabled", text="Search" ,  command= search)                    # Search button: runs search() func

# # Left text frame (Main text)
first_frame=tk.Frame(window, relief=tk.RAISED, bd=1)                                                    
# # # Frame's row-column config
first_frame.rowconfigure(2,weight=1)     # maximize the text widget 
first_frame.columnconfigure(0, weight=1) # maximize column  
# # # Plagiarism Ratio Label
ratio_label=tk.Label(first_frame, text="Plagiarism Ratio")
# # # Plagiarism Ratio Bar
ratio =ttk.Progressbar(first_frame, length=100, mode='determinate')
# # # Main text widget
main_text_widget = tk.Text(first_frame,wrap='word', borderwidth=5)
# # # # Main text widget styles
main_text_widget.tag_configure('normal', foreground='black', font=('Arial', 16))
main_text_widget.tag_configure('plagiarism',  foreground='red',  font=('Arial', 16))

# # Right text frame (Data text)
second_frame=tk.Frame(window, relief=tk.RAISED, bd=1)
# # # Frame's row-column config
second_frame.rowconfigure(2,weight=1)
second_frame.columnconfigure(0, weight=1)
# # # File Selecting Label
# # # File Selecting default string variable
default_opt = tk.StringVar(window,value="Select a data sources...")
# # # File Selecting Combobox
file_menu = ttk.Combobox(second_frame, state="readonly",  textvariable= default_opt) 
# # # File Selecting "Go to file"  Button
btn_go = tk.Button(second_frame, state="disabled", text="Go to file", command=lambda: printer( file_dict[ file_menu.get() ] ) , borderwidth=3) # send index of file in file_menu to printer() by using file_dict.
# # # Data text widget
comp_text_widget = tk.Text(second_frame,wrap='word', borderwidth=5)
# # # # Data text widget styles
comp_text_widget.tag_configure('normal', foreground='black', font=('Arial', 16))
comp_text_widget.tag_configure('plagiarism',  foreground='black',  font=('Arial', 16, 'bold'))
comp_text_widget.tag_configure('found',  foreground='white', background="black",  font=('Arial', 16, 'bold'))

# # # # Placement # # # #
# Main Frames
btn_frame.grid(row=0, column=0, sticky="ns")
first_frame.grid(row=0, column=1, sticky="ns")
second_frame.grid(row=0, column=2, sticky="ns")
# btn_frame widgets
btn_file.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_files.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_check.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_search.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
N_label.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
N_menu.grid(row = 5, column = 0,sticky="ew", padx=5, pady=10)
# first_frame widgets
ratio_label.grid(column = 0, row = 0, sticky="w", padx=5, pady=5)
ratio.grid(column = 0, row = 1, sticky="ew", padx=5, pady=5)
main_text_widget.grid(row=2, column=0, sticky="nsew", padx=5, pady=5, ipadx=5,ipady=5)
# second_frame widgets
file_menu.grid(column = 0, row = 0,sticky="ew", padx=5, pady=5)
btn_go.grid(column = 0, row = 1, sticky="ew", padx=5, pady=2)
comp_text_widget.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
window.mainloop() # main window loop
