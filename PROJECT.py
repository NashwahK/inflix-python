# MAIN SOURCE CODE - INFLIX MOVIE REGISTRATION SYSTEM
# MADE BY NASHWAH MOHAMMAD (SE-22023) AND IMAN JAWAD (SE-22025)

# Importing all required libraries
import tkinter
from tkinter import *
from tkinter import ttk
import customtkinter
from PIL import ImageTk, Image
import pyodbc
import tkinter as tk
from tkinter import messagebox
import pyautogui
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ALL FUNCTIONS
# Defining Function for Delete Button
def delete_booking():
    # For clearing the frame before griding new widgets
    def clear_frame():
        for widgets in f2.winfo_children():
            widgets.destroy()

    clear_frame()

    # Creating a Function to delete data entry from database
    def clear_booking():
        if len(var8.get()) != 13 or var8.get().isalpha():
            messagebox.showerror("Invalid CNIC", "CNIC must be 13 numbers.")
            return
        else:
            # Establishing a connection between Python and Database (MS Access)
            con1 = pyodbc.connect((r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                                   r"DBQ=C:\Users\Nashwah\Documents\inflix.accdb;"))
            cursor1 = con1.cursor()
            cursor1.execute(f"SELECT cid FROM customer WHERE ccnic='{var8.get()}'")
            cid = cursor1.fetchall()
            # Applying indexing on the ID fetched for removing redundant brackets
            ind_cid = cid[0][0]
            cursor2 = con1.cursor()
            cursor2.execute(f"SELECT bsid FROM booking WHERE cid = '{ind_cid}'")
            seat = cursor2.fetchall()
            print(seat)
            # Apply indexing on the ID fetched for removing redundant brackets
            ind_seat = seat[0][0]
            cursor3 = con1.cursor()
            cursor3.execute(f"DELETE FROM booking WHERE cid ='{ind_cid}'")
            cursor4 = con1.cursor()
            cursor4.execute(f"DELETE FROM customer WHERE ccnic='{var8.get()}'")
            cursor5 = con1.cursor()
            cursor5.execute(f"UPDATE seats SET status='Available' WHERE bsid= {ind_seat}")
            con1.commit()
            cursor1.close()
            cursor2.close()
            cursor3.close()
            cursor4.close()
            cursor5.close()
            con1.close()
            messagebox.showinfo("Deletion Done Successfully!", "Your booking has successfully been deleted. "
                                "See you soon!")
    # Creating Labels and Entry boxes
    dl1 = customtkinter.CTkLabel(f2, text="Enter your CNIC number",
                                 font=("Segoe UI Light", 18),
                                 bg_color="transparent", fg_color="transparent",
                                 text_color=("gray20", "gray90"))
    dl1.grid(row=0, column=0, pady=10, padx=10)
    l2 = customtkinter.CTkLabel(f2, text="Are you sure you want to delete your booking?",
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"), font=("Segoe UI Light", 18))
    l2.grid(row=1, column=0, pady=25, padx=50)

    e1 = customtkinter.CTkEntry(f2, width=200, textvariable=var8)
    e1.grid(row=0, column=1, padx=50, pady=10)
    b2 = customtkinter.CTkButton(f2, text="Yes", command=clear_booking, fg_color=('#8f2530', '#691921'),
                                 hover_color='#66272d')
    b2.grid(row=1, column=1, pady=25, padx=10)


# Defining Function for Book Button
def book_ticket():
    # Making image global
    global seat_img

    # For clearing the frame before griding new widgets
    def clear_frame():
        for widgets in f2.winfo_children():
            widgets.destroy()

    clear_frame()

    def display_shows():
        # This function updates the seats available to the user
        # Establishing a connection between Python and Database (MS Access)
        con1 = pyodbc.connect((r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                               r"DBQ=C:\Users\Nashwah\Documents\inflix.accdb;"))
        cursor1 = con1.cursor()
        cursor1.execute(f"SELECT show_ID FROM shows WHERE show_name = '{var6.get()}'")
        showid = cursor1.fetchall()
        # Applying indexing on ID fetched for remove redundant brackets
        show = showid[0][0]
        cursor2 = con1.cursor()
        cursor2.execute(f"SELECT seats FROM seats WHERE status='Available' AND show_ID='{show}'")
        seat_list = cursor2.fetchall()
        # Creating a list for appending seat names to
        list1 = []
        # Running a for loop for making each element into a list
        for seat1 in seat_list:
            seat1 = list(seat1)
            list1.extend(seat1)
        # This is a method of inserting elements in a Combobox
        seats_cb['values'] = list1
        con1.commit()
        con1.close()

    def generate_ticket():
        gen = customtkinter.CTk()
        gen.title("Movie Ticket")
        gen.resizable(False, False)

        # This function is used to keep the ticket window in center
        def mid_window(width=150, height=100):
            # Finding coordinates
            x = (1400 / 2) - (100 / 2)
            y = (500 / 2) - (200 / 2)
            gen.geometry('%dx%d+%d+%d' % (width, height, x, y))

        mid_window(width=390, height=500)

        # This function takes a screenshot and saves it as PDF

        def pdf_saver():
            # This function locates ticket on screen and saves it as pdf
            area = (650, 130, 600, 750)
            screenshot = pyautogui.screenshot(region=area)
            screenshot.save('ticket.png')
            # Creating a canvas to insert image to
            # Canvases can be saved as other file formats
            c = canvas.Canvas("screenshot.pdf", pagesize=letter)
            c.drawImage("ticket.png", 0, 0)
            c.showPage()
            c.save()
            messagebox.showinfo("PDF successfully saved", "Your ticket has successfully "
                                                          "been saved as a PDF file in "
                                                          "the current directory")

        cl1 = customtkinter.CTkLabel(gen, text="Movie Ticket", font=("System", 40))
        cl1.place(x=65, y=50)
        cl2 = customtkinter.CTkLabel(gen, text="Name :", font=("System", 20))
        cl2.place(x=10, y=130)
        l21 = customtkinter.CTkLabel(gen, font=("System", 20))
        l21.place(x=90, y=130)
        cl3 = customtkinter.CTkLabel(gen, text="Contact :", font=("System", 20))
        cl3.place(x=10, y=170)
        l31 = customtkinter.CTkLabel(gen, font=("System", 20))
        l31.place(x=90, y=170)
        cl4 = customtkinter.CTkLabel(gen, text="Movie :", font=("System", 20))
        cl4.place(x=10, y=210)
        l41 = customtkinter.CTkLabel(gen, font=("System", 20))
        l41.place(x=90, y=210)
        cl5 = customtkinter.CTkLabel(gen, text="Show :", font=("System", 20))
        cl5.place(x=10, y=250)
        l51 = customtkinter.CTkLabel(gen, font=("System", 20))
        l51.place(x=90, y=250)
        cl6 = customtkinter.CTkLabel(gen, text="Price :", font=("System", 20))
        cl6.place(x=10, y=290)
        l61 = customtkinter.CTkLabel(gen, font=("System", 20))
        l61.place(x=90, y=290)
        intersection = customtkinter.CTkLabel(gen,
                                              text="## -------------------------------------------------------------"
                                                   "--------##", text_color=("black", "white"), fg_color="transparent")
        intersection.place(x=30, y=330)
        ins = customtkinter.CTkLabel(gen, text="Please head over to the counter for payment", font=("System", 16))
        ins.place(x=3, y=360)
        ins = customtkinter.CTkLabel(gen, text="ENJOY YOUR MOVIE", font=("System", 16))
        ins.place(x=90, y=400)
        pdf = customtkinter.CTkButton(gen, text="Download as PDF", fg_color=('#8f2530', '#691921'),
                                      hover_color='#66272d', command=pdf_saver)
        pdf.place(x=120, y=470)
        # Storing required information in variables for the ticket
        name = var1.get()
        contact = var2.get()
        movie = var5.get()
        show = var6.get()
        # Establishing a connection between Python and Database (MS Access)
        con1 = pyodbc.connect((r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                               r"DBQ=C:\Users\Nashwah\Documents\inflix.accdb;"))
        cursor1 = con1.cursor()
        cursor1.execute(f"SELECT mprice FROM movies WHERE mname = '{var5.get()}'")
        price = cursor1.fetchall()
        ind_price = price[0][0]
        con1.close()
        l21.configure(text=name)
        l31.configure(text=contact)
        l41.configure(text=movie)
        l51.configure(text=show)
        l61.configure(text=ind_price)
        gen.mainloop()

    # This function is used to check for any inaccurate data entry
    # and transfer data to the database
    def confirm_booking():
        if var1.get().isdigit():
            messagebox.showerror("Invalid Name", "Name should only contain letters")
            return
        elif len(var2.get()) != 11 or var2.get().isalpha():
            messagebox.showerror("Invalid Phone Number", "Phone Number must contain 11 numbers")
            return
        elif len(var4.get()) != 13 or var4.get().isalpha():
            messagebox.showerror("Invalid CNIC", "CNIC must be 13 numbers.")
            return
        else:
            # Establishing a connection between Python and Database (MS Access)
            con1 = pyodbc.connect((r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                                   r"DBQ=C:\Users\Nashwah\Documents\inflix.accdb;"))
            cursor1 = con1.cursor()
            cursor1.execute(f"INSERT INTO customer(cname, cphone, cemail, ccnic) "
                            f"values('{var1.get()}','{var2.get()}','{var3.get()}', '{var4.get()}')")
            con1.commit()
            cursor1.close()
            cursor2 = con1.cursor()
            cursor2.execute(f"SELECT cid FROM customer WHERE ccnic = '{var4.get()}'")
            cid = cursor2.fetchall()
            cursor3 = con1.execute(f"SELECT mid FROM movies WHERE mname='{var5.get()}' ")
            mov = cursor3.fetchall()
            cursor4 = con1.execute(f"SELECT show_ID FROM shows WHERE show_name='{var6.get()}'")
            show = cursor4.fetchall()
            cursor5 = con1.cursor()
            cursor5.execute(f"SELECT bsid FROM seats WHERE seats='{var7.get()}'")
            seat_itm = cursor5.fetchall()
            # Applying indexing on the ID fetched for removing redundant brackets
            ind_mov = mov[0][0]
            ind_show = show[0][0]
            ind_seats = seat_itm[0][0]
            ind_cid = cid[0][0]
            cursor6 = con1.cursor()
            cursor6.execute(f"INSERT INTO booking(mid, show_ID, bsid, cid) "
                            f"values('{ind_mov}', '{ind_show}', '{ind_seats}', '{ind_cid}')")
            cursor7 = con1.cursor()
            con1.commit()
            cursor7.execute(f"UPDATE seats SET status='Unavailable' WHERE bsid = {ind_seats}")
            con1.commit()
            con1.close()
            booknow.destroy()
            gentick = customtkinter.CTkButton(f2, text="Generate Ticket", fg_color=('#8f2530', '#691921'),
                                              hover_color='#66272d', command=generate_ticket)
            gentick.grid(row=9, column=2, padx=5)

    # Creating Labels and Entry Boxes
    l2 = customtkinter.CTkLabel(f2, text="Name: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l2.grid(row=2, column=0, padx=10, pady=20)
    l3 = customtkinter.CTkLabel(f2, text="Contact Number: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l3.grid(row=3, column=0, padx=20, pady=10)
    l4 = customtkinter.CTkLabel(f2, text="Email ID: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l4.grid(row=4, column=0, padx=20, pady=10)
    l5 = customtkinter.CTkLabel(f2, text="CNIC", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l5.grid(row=5, column=0, padx=20, pady=10)
    l6 = customtkinter.CTkLabel(f2, text="Movie: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l6.grid(row=6, column=0, padx=20, pady=10)
    l7 = customtkinter.CTkLabel(f2, text="Show: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l7.grid(row=7, column=0, padx=20, pady=10)
    l8 = customtkinter.CTkLabel(f2, text="Seat: ", font=("Segoe UI Light", 18),
                                bg_color="transparent", fg_color="transparent",
                                text_color=("gray20", "gray90"))
    l8.grid(row=8, column=0, padx=20, pady=10)
    # Inserting image for seating chart
    seat = PhotoImage(file=r'D:\INFlix\seats.png')
    seat_img = seat.subsample(2, 2)
    seat = Label(f2, image=seat_img)
    seat.grid(row=9, column=1)

    e2 = customtkinter.CTkEntry(f2, width=200, textvariable=var1)
    e2.grid(row=2, column=1, padx=50, pady=10)
    e3 = customtkinter.CTkEntry(f2, width=200, textvariable=var2)
    e3.grid(row=3, column=1, padx=20, pady=10)
    e4 = customtkinter.CTkEntry(f2, width=200, textvariable=var3)
    e4.grid(row=4, column=1, padx=50, pady=10)
    e5 = customtkinter.CTkEntry(f2, width=200, textvariable=var4)
    e5.grid(row=5, column=1, padx=20, pady=10)

    movie_cb = ttk.Combobox(f2, values=["Black Panther: Wakanda Forever",
                                        "Captain Marvel",
                                        "Ms. Marvel"],
                            justify=tk.LEFT, font=(None, 13), textvariable=var5)
    movie_cb.grid(row=6, column=1, padx=20, pady=10)

    show_cb = ttk.Combobox(f2, values=["Afternoon Show",
                                       "Evening Show",
                                       "Late Night Show"],
                           justify=tk.LEFT, font=(None, 13), textvariable=var6)
    show_cb.grid(row=7, column=1, padx=20, pady=10)
    seats_cb = ttk.Combobox(f2, justify=tk.LEFT,
                            font=(None, 13),
                            textvariable=var7)
    seats_cb.grid(row=8, column=1, padx=20, pady=10)

    seats_conf = customtkinter.CTkButton(f2, text="Show Available Seats", fg_color=('#8f2530', '#691921'),
                                         hover_color='#66272d', command=display_shows)
    seats_conf.grid(row=8, column=2, padx=5)
    booknow = customtkinter.CTkButton(f2, text="Confirm", fg_color=('#8f2530', '#691921'),
                                      hover_color='#66272d', command=confirm_booking)
    booknow.grid(row=9, column=2, padx=5)


# Defining Function for View Button
def view_movies():
    # For clearing f2 before adding new widgets
    def clear_frame():
        for widget in f2.winfo_children():
            widget.destroy()

    clear_frame()

    # Making images global
    global img1
    global img2
    global img3
    # Creating labels for images
    img1 = ImageTk.PhotoImage(Image.open(r'D:\INFlix\wakandaforever.png'))
    movie1 = Label(f2, bd=3, relief="solid", image=img1)
    movie1.grid(row=0, column=0, padx=50, pady=10)

    img2 = ImageTk.PhotoImage(Image.open(r'D:\INFlix\cmarvel.png'))
    movie2 = Label(f2, bd=3, relief="solid", image=img2)
    movie2.grid(row=0, column=1, padx=10, pady=10)

    img3 = ImageTk.PhotoImage(Image.open(r'D:\INFlix\mmarvel.png'))
    movie3 = Label(f2, bd=3, relief="solid", image=img3)
    movie3.grid(row=0, column=2, padx=50, pady=10)

    # Adding textbox for descriptions
    # Movie 1 : Black Panther: Wakanda Forever
    movielabel = customtkinter.CTkLabel(f2, text="Black Panther: Wakanda Forever",
                                        font=("Segoe UI", 18))
    movielabel.grid(row=1, column=0, pady=5)
    moviename1 = customtkinter.CTkTextbox(f2, fg_color=("gray40", "gray30"),
                                          height=100,
                                          width=210, text_color="white",
                                          font=("Segoe UI Light", 13),
                                          scrollbar_button_color=('#8f2530', '#691921'),
                                          scrollbar_button_hover_color="#66272d")
    moviename1.grid(row=2, column=0, pady=0)

    moviename1.insert("0.0", "Synopsis:\nThe people of Wakanda fight to  protect their home by intervening"
                             "world powers as they mourn the death of King T'Challa.\n"
                             "Ratings: 4.5/5")
    moviename1.configure(state="disabled")

    # Movie 2: Captain Marvel
    movielabel2 = customtkinter.CTkLabel(f2, text="Captain Marvel",
                                         font=("Segoe UI", 18))
    movielabel2.grid(row=1, column=1, pady=5)
    moviename2 = customtkinter.CTkTextbox(f2, fg_color=("gray40", "gray30"), height=100,
                                          width=210, text_color="white", font=("Segoe UI Light", 13),
                                          scrollbar_button_color=('#8f2530', '#691921'),
                                          scrollbar_button_hover_color="#66272d")
    moviename2.grid(row=2, column=1, pady=0)

    moviename2.insert("0.0", "Synopsis:\nCarol Danvers is now one of the universe's most powerful hero when Earth is"
                             " caught in the middle of a galactic war between two     alien races.\nRatings: 3.5/5")
    moviename2.configure(state="disabled")

    # Movie 3: Ms. Marvel
    movielabel3 = customtkinter.CTkLabel(f2, text="Ms. Marvel",
                                         font=("Segoe UI", 18))
    movielabel3.grid(row=1, column=2, pady=5)
    moviename3 = customtkinter.CTkTextbox(f2, fg_color=("gray40", "gray30"), height=100,
                                          width=210, text_color="white", font=("Segoe UI Light", 13),
                                          scrollbar_button_color=('#8f2530', '#691921'),
                                          scrollbar_button_hover_color="#66272d")
    moviename3.grid(row=2, column=2, pady=10)

    moviename3.insert("0.0", "Synopsis:\nKamala feels like she doesn't fit in at school and sometimes even at home, "
                             "that is until she gets superpowers like the heroes she looks up to.\nRatings: 4.5/5")
    moviename3.configure(state="disabled")

    # Adding Book Now Buttons under each Movie
    movie1book = customtkinter.CTkButton(f2, text="Book Now!",
                                         font=("Segoe UI Light", 24),
                                         width=30, command=book_ticket,
                                         fg_color=('#8f2530', '#691921'),
                                         hover_color='#66272d')
    movie1book.grid(row=3, column=0, pady=10)

    movie2book = customtkinter.CTkButton(f2, text="Book Now!", font=("Segoe UI Light", 24), width=30,
                                         command=book_ticket, fg_color=('#8f2530', '#691921'), hover_color='#66272d')
    movie2book.grid(row=3, column=1, pady=10)

    movie3book = customtkinter.CTkButton(f2, text="Book Now!", font=("Segoe UI Light", 24), width=30,
                                         command=book_ticket, fg_color=('#8f2530', '#691921'), hover_color='#66272d')
    movie3book.grid(row=3, column=2, pady=10)


# The Front End Development - CTk
# Creating the Master Window
m = customtkinter.CTk()
# Making the image variables global to module level
global img1
global img2
global img3
global seat_img

# Defining String Variable
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
var5 = StringVar()
var6 = StringVar()
var7 = StringVar()
var8 = StringVar()

# Storing variables for efficiency
screen_width = m.winfo_screenwidth()
screen_height = m.winfo_screenheight()

# Setting the window size and position
m.geometry(f"{screen_width}x{screen_height}+0+0")
m.title("Movie Reservation System")

# Setting the background color w.r.t Dark Mode and Light Mode
m.configure(fg_color=("gray90", "gray5"))

# Set the appearance to the default mode of the user
customtkinter.set_appearance_mode("System")
title = customtkinter.CTkLabel(m, text="INFlix Movie Reservation System",
                               text_color=("black", "white"),
                               font=("Segoe UI", 50, "bold"),
                               bg_color="transparent")
title.pack(fill=X)

# Creating Frame 1
f1 = customtkinter.CTkFrame(m, width=375, height=500,
                            fg_color=("gray80", "gray10"))
f1.place(relx=0.16, rely=0.1, anchor=tkinter.N)

# Fixing frame size
f1.grid_propagate(False)

welcometext = customtkinter.CTkLabel(f1, text="Welcome to the INFlix Movie Reservation System!",
                                     text_color=("black", "white"), font=("Segoe UI Light", 18))
welcometext.grid(row=1, column=0, pady=(15, 5), padx=3)
l1 = customtkinter.CTkLabel(f1, text="Please facilitate yourself with these options",
                            text_color=("black", "white"), font=("Segoe UI Light", 18))
l1.grid(row=2, column=0, pady=5)

# Creating Buttons for navigating through the application
showbutton = customtkinter.CTkButton(f1, text="View Movies",
                                     font=("Segoe UI Light", 26),
                                     width=40, command=view_movies,
                                     corner_radius=10,
                                     fg_color=('#8f2530', '#691921'),
                                     hover_color='#66272d')
showbutton.grid(row=5, column=0, pady=(50, 10))

bookbutton = customtkinter.CTkButton(f1, text="Book Your Ticket",
                                     font=("Segoe UI Light", 26),
                                     width=40, command=book_ticket,
                                     corner_radius=10,
                                     fg_color=('#8f2530', '#691921'),
                                     hover_color='#66272d')
bookbutton.grid(row=6, column=0, pady=10)

deletebutton = customtkinter.CTkButton(f1, text="Delete a Booking", font=("Segoe UI Light", 26),
                                       width=40, command=delete_booking, corner_radius=10,
                                       fg_color=('#8f2530', '#691921'), hover_color='#66272d')
deletebutton.grid(row=7, column=0, pady=(10, 50))

# Creating Frame 2
f2 = customtkinter.CTkFrame(m, fg_color=("gray80", "gray10"), width=855,
                            height=screen_height)
f2.place(relx=0.655, rely=0.1, anchor=tkinter.N)

# Run the application
m.mainloop()
