import PriceAPI
import Reader
import time
import PDFReader

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
from tkinter import *
import customtkinter


# Initialize & setup custom tkinter window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
App = customtkinter.CTk()
App.geometry("600x500")
App.minsize(width=600,height=500)
App.maxsize(width=600,height=500)
App.title("Adams 12 Inventory Calculator")



# Instantiate all important variables
API_Key = ""
Price = 0
Count = 0
file_path = ""
ASIN = []
Quantity = []





Title_Label = customtkinter.CTkLabel(master=App,
                               text="Adams 12 Inventory Calculator",
                               width=500,
                               height=35,
                               font=("Arial", 40),
                               corner_radius=8)
Title_Label.place(relx=0.5, rely=0.05, anchor=CENTER)





lbl1 = customtkinter.CTkLabel(master=App,
                               text="Please input your unique API key from the Rainforest API website.",
                               width=120,
                               height=25,
                               text_color=("white"),
                               corner_radius=8)
lbl1.place(relx=0.5, rely=.175, anchor=CENTER)





API_Key_Entry = customtkinter.CTkEntry(master=App,
                               placeholder_text="API Key",
                               width=300,
                               height=25,
                               border_width=2,
                               corner_radius=10)
API_Key_Entry.place(relx=0.5, rely=.225, anchor=CENTER)




lbl2 = customtkinter.CTkLabel(master=App,
                               text="Please upload the inventory data file. Supported file types(Docx, PDF)",
                               width=120,
                               height=25,
                               text_color=("white"),
                               corner_radius=8)
lbl2.place(relx=0.5, rely=.355, anchor=CENTER)




lbl3_text = tk.StringVar(value="File Path:")

lbl3 = customtkinter.CTkLabel(master=App,
                               textvariable=lbl3_text,
                               width=120,
                               height=25,
                               text_color=("white"),
                               wraplength=450,
                               corner_radius=8)
lbl3.place(relx=0.5, rely=.425, anchor=CENTER)


def upload_file():
    if API_Key_Entry.get() == "":
        showerror("API Input", "Please enter your API Key")
        return
    
    
    global API_Key
    API_Key = API_Key_Entry.get()
    print(API_Key)


    #Open and sets file path to variable
    global file_path
    file_path = filedialog.askopenfilename()
    print(file_path)

    # Updates to display selected file path
    lbl3_text = tk.StringVar(value=f"File Path: {file_path}")
    lbl3.configure(textvariable=lbl3_text)


    file = open("Data.txt", "w")
    file.close()

    file = open("Data.txt", "a")
    file.write("ASIN \t\t Price \t\t Quantity\n")
    file.close()

    file2 = open("Errors.txt", 'w')
    file2.write("Could not find price for the following ASIN's:\n")
    file2.close()

    lists()


def lists():
    # Creats ASIN var and gets the ASINs from doc
    global ASIN 
    # Creats Quantity var and gets the Quantities from doc
    global Quantity
    
    global file_path

    if file_path[-3:] == 'pdf':
        PDFReader.find(file_path)
        ASIN = PDFReader.getASIN()
        Quantity = PDFReader.getQuantity(file_path)
    elif file_path[-4:] == 'docx':
        ASIN = Reader.getAsin(file_path)
        Quantity = Reader.getAmount(file_path)
    else:
        ASIN = []
        Quantity = []
        file_path = ""
        showerror("Invalid File Type", "Please upload the inventory data file. Supported file types(Docx, PDF)")



upload_file_button = customtkinter.CTkButton(master=App,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Upload File",
                                 command=upload_file)
upload_file_button.place(relx=0.5, rely=0.505, anchor=CENTER)






lbl4_text = tk.StringVar(value="")

lbl4 = customtkinter.CTkLabel(master=App,
                               textvariable=lbl4_text,
                               width=120,
                               height=25,
                               text_color=("white"),
                               corner_radius=8)
lbl4.place(relx=0.5, rely=.7, anchor=CENTER)


lbl5_text = tk.StringVar(value="")

lbl5 = customtkinter.CTkLabel(master=App,
                               textvariable=lbl5_text,
                               width=120,
                               height=25,
                               text_color=("white"),
                               corner_radius=8)
lbl5.place(relx=0.5, rely=.775, anchor=CENTER)



lbl6_text = tk.StringVar(value="")



lbl6 = customtkinter.CTkLabel(master=App,
                               textvariable=lbl6_text,
                               width=120,
                               height=25,
                               text_color=("white"),
                               corner_radius=8)
lbl6.place(relx=0.5, rely=.825, anchor=CENTER)




def start_prices():
    # Checks individual cases in which function could not run, throws error and returns
    if ASIN == []:
        showerror("ASIN List Error", "Unable to retrieve ASIN list")
        return
    if Quantity == []:
        showerror("Quantity List Error","Unable to retrieve item Quantity list")
        return
    if file_path == "":
        showerror("File Path Error", "Invalid file path, please try again")
        return
    if API_Key == "":
        showerror("API Input", "Please enter your API Key")
        return
    if len(ASIN) != len(Quantity):
        showerror("Trouble Reading File", "There was a problem, please reupload the inventory file.")
        return
    
    errorCount = 0
    for y in range(5):
        if PriceAPI.find(API_Key, ASIN[y]) == 0:
            errorCount+=1
    if errorCount == 5:    
        showerror("Invalid API Key", "Please check your API Key. If problems continue, check the Rainforest API website. Also, ensure the inventory file is formatted correctly.")
        return


        
    # Count variable for # of ASINs found 
    global count
    count = 0

    # Price variable for total price
    global Price
    Price = 0

    # Updates label to say 0 of ASIN's found
    lbl4_text = tk.StringVar(value=f"{count} of {len(ASIN)} ASIN's found")
    lbl4.configure(textvariable=lbl4_text)



    for x in range(len(ASIN)):
        # Local variable currentPrice to store individual prices to add to Data.txt file
        currentPrice = PriceAPI.find(API_Key, ASIN[x])
        print(type(currentPrice))
        print(currentPrice)
        price_with_quantity = currentPrice * int(Quantity[x]) 
        print(type(price_with_quantity))
        print(price_with_quantity)
        
        # Adds currentPrice -- indiviual price -- to Price variable -- total price
        #global Price
        Price += price_with_quantity
        # Increases count of ASIN's found for "{count} of {len(ASIN)} ASIN's found"
        #global count
        count+=1
        # Updates # of ASIN's found label
        lbl4_text = tk.StringVar(value=f"{count} of {len(ASIN)} ASIN's found")
        lbl4.configure(textvariable=lbl4_text)

        lbl5_text = tk.StringVar(value=f"Total Inventory Price: ${Price}")
        lbl5.configure(textvariable=lbl5_text)

        App.update()
        # Wait 1 second, ensuring to not overwork/overload API
        time.sleep(1)


        file = open("Data.txt", "a")
        file.write(f"{ASIN[x]} \t {currentPrice} \t\t {Quantity[x]}\n")
        file.close()


        if currentPrice == 0:
            file2 = open("Errors.txt", "a")
            file2.write(f"{ASIN[x]}\n")



    file = open("Data.txt", "a")
    file.write(f"Total Price: {Price}")
    file.close()

    PriceAPI.createErrorList()

    lbl6_text = tk.StringVar(value=f"'Data.txt' file created with price data. 'Errors.txt' file created with prices not found.")
    lbl6.configure(textvariable=lbl6_text)


start_prices_button = customtkinter.CTkButton(master=App,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Find Total Inventory Price",
                                 command=start_prices)
start_prices_button.place(relx=0.5, rely=.935, anchor=CENTER)




App.mainloop()
