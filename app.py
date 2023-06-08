from tkinter import *
from turtle import right
import client
import tkinter as tk
import json

def create_gui():
    def clear_text():
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
    def show_entry_fields():
        email=e1.get()
        password=e2.get()
        group_url=e3.get()
        mode_chosen=v.get()
        cookies_str,single_profile=client.run_get_cookies(email,password,group_url)
        print("Mode {} is running".format(mode_chosen))
        if cookies_str==None:
            print("Cannot get the cookies. Recheck input information!")
        else:
            if cookies_str.find("content_owner_id_new")==-1:
                print("The input information may be incorrect, the output cookies is not in standard format!")
            js_filename=group_url.split("/")[-1]
            if len(js_filename)==0:
                js_filename=group_url.split("/")[-2]
            cookies_js=[{"group_url":group_url,"cookies":cookies_str}]
            if mode_chosen==1:
                with open("cookies/{}.json".format(js_filename), 'w', encoding='utf-8') as f:
                    json.dump(cookies_js, f, ensure_ascii=False, indent=4)
                f.close()
            print("Cookies: %s\nGroup URL: %s" % (cookies_str[:min(150,len(cookies_str))], single_profile))
    
    master = tk.Tk()
    v = tk.IntVar()
    tk.Label(master, 
            text="Email").grid(row=0)
    tk.Label(master, 
            text="Password").grid(row=1)
    tk.Label(master, 
            text="Facebook group URL").grid(row=2)
    e1 = tk.Entry(master,width=40)
    e2 = tk.Entry(master,width=40)
    e3 = tk.Entry(master,width=40)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    tk.Label(master, 
            text="""Choose export as json in additional? """,
            justify = tk.CENTER,
            padx = 0).grid(row=3, 
                                        column=1, 
                                        sticky=tk.W, 
                                        pady=3)
    tk.Button(master, 
            text='Quit', 
            command=master.quit).grid(row=5, 
                                        column=0, 
                                        sticky=tk.W, 
                                        pady=5)
    tk.Button(master, 
            text='Show', command=show_entry_fields).grid(row=5, 
                                                        column=1, 
                                                        sticky=tk.W, 
                                                        pady=5)
    tk.Button(master, 
            text='Clear input', 
            command=clear_text).grid(row=5, 
                                        column=2, 
                                        sticky=tk.W, 
                                        pady=5)
    tk.Radiobutton(master, 
                text="Export as json",
                variable=v, 
                value=1).grid(row=4, 
                                        column=1, 
                                        sticky=tk.W, 
                                        pady=4)

    tk.Radiobutton(master, 
                text="Not export",
                variable=v, 
                value=2).grid(row=4,
                column=2,
                sticky=tk.E,pady=4)
    tk.mainloop()
#this comment makes no changes to the basic functionality of project