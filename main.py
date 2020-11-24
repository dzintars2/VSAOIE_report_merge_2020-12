# VSAOIe atskaišu apvienošana - 2020.gada decembris / 2021.gada janvāris (pārejas īpašais gadījums)
# SIA "AI Finance"
# e-pasts: info@aktivs.lv

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import os, time, hmac


class SocialApp():
    
    window = None
    filepath1 = ""
    filepath2 = ""
    
    def __init__ (self):
        self.window = Tk()
        self.window.title("VSAOIe atskaites apvienošana")
        lbl = Label(self.window, text="VSAOIe atskaites apvienošana")
        lbl.grid(column=1, row=0, padx=5, pady=5)
        self.lbl = Label(self.window, 
	    				text="VSAOI XML 2020.decembris: ", padx=5)
        self.lbl.grid(column=0, row=1, padx=5, pady=5)
        self.lbl_file1 = Label(self.window, 
	    				text="Fails nav izvēlēts", 
	    				borderwidth=1,
	    	 			relief="solid",
	    	 			width=40, 
	    	 			pady=3,
	    	 			padx=3,
	    	 			bg="white",
	    	 			justify="left", 
	    	 			anchor="w",
	    				fg="RED")
        self.lbl_file1.grid(column=1, row=1, padx=5, pady=5)
        self.lbl = Label(self.window, 
	    				text="VSAOI XML 2021.janvāris: ", padx=5)
        self.lbl.grid(column=0, row=2, padx=5, pady=5)
        self.lbl_file2 = Label(self.window, 
	    				text="Fails nav izvēlēts", 
	    				borderwidth=1,
	    	 			relief="solid",
	    	 			width=40, 
	    	 			pady=3,
	    	 			padx=3,
	    	 			bg="white",
	    	 			justify="left", 
	    	 			anchor="w",
	    				fg="RED")
        self.lbl_file2.grid(column=1, row=2, padx=5, pady=5)
        btn_file1= Button(self.window, 
	    				text="Izvēlēties failu", 
	    				command=self.selectFile1, 
	    				width=17)
        btn_file1.grid(column=2, row=1, padx=5, pady=5)
        btn_file2 = Button(self.window, 
	    				text="Izvēlēties failu", 
	    				command=self.selectFile2, 
	    				width=17)
        btn_file2.grid(column=2, row=2, padx=5, pady=5)
        btn_file3 = Button(self.window, 
	    				text="Apstrādāt", 
	    				command=self.mergeData, 
	    				width=17)
        btn_file3.grid(column=2, row=3, padx=5, pady=5)
        zoom = 0.2
        image = Image.open("logo.png")
        pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        panel = Label(self.window, image = img)
        panel.grid(column=0, row=0)
        self.lbl = Label(self.window, 
	    				text="Autors: AI Finance SIA, e-pasts: info@aktivs.lv", padx=5)
        self.lbl.grid(column=1, row=4, padx=5, pady=5)
        self.window.resizable(False, False)
        self.window.mainloop()

    def selectFile1(self):
        filename =  filedialog.askopenfilename(
						title = "Izvēlēties failu",
						filetypes = (("XML datne","*.xml"),("Visi faili","*.*")))
        self.filepath1 = filename
        if filename!="":
            if len(filename)>40:
                self.lbl_file1["text"] = ".."+filename[-38:]
            else:
                self.lbl_file1["text"] = filename
                self.lbl_file1["fg"] = "black"
        else:
            self.lbl_file1["text"] = "Fails nav izvēlēts"
            self.lbl_file1["fg"] = "red"

    def selectFile2(self):
        filename =  filedialog.askopenfilename(
						title = "Izvēlēties failu",
						filetypes = (("XML datne","*.xml"),("Visi faili","*.*")))
        self.filepath2 = filename
        if filename!="":
            if len(filename)>40:
                self.lbl_file2["text"] = ".."+filename[-38:]
            else:
                self.lbl_file2["text"] = filename
                self.lbl_file2["fg"] = "black"
        else:
            self.lbl_file2["text"] = "Fails nav izvēlēts"
            self.lbl_file2["fg"] = "red"

    def mergeData(self):
        if self.filepath1 == "" or self.filepath2 == "":
            messagebox.showerror("Kļūda", "Nav izvēlēts fails!")
            return False
        try:
            file1 = ET.parse(self.filepath1)
        except:
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2020.gada decembri!")
            return False
        try:
            file2 = ET.parse(self.filepath2)
        except:
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2021.gada janvāri!")
            return False    
        root = file1.getroot()
        if (len(root) == 0):
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2020.gada decembri!")
            return False
        gads = 0
        menesis = 0
        hasTab4 = False
        for i in root:
            if str(i.tag) == 'ParskGads':
                gads = int(i.text)
            if str(i.tag) == 'ParskMen':
                menesis = int(i.text)
            if str(i.tag) == 'Tab4':
                hasTab4 = True
        if gads == 0 or menesis == 0:
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2020.gada decembri!")
            return False
        elif gads!= 2020 or menesis != 12:
            messagebox.showerror("Kļūda", "Atskaites failā 2020-12 ir kļūdains periods ("+str(gads)+"-"+str(menesis)+")")
            return False

        #fails 2021-01
        root2 = file2.getroot()
        if (len(root2) == 0):
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2021.gada janvāri!")
            return False
        gads2 = 0
        menesis2 = 0
        for i in root2:
            if str(i.tag) == 'ParskGads':
                gads2 = int(i.text)
            if str(i.tag) == 'ParskMen':
                menesis2 = int(i.text)
        if gads2 == 0 or menesis2 == 0:
            messagebox.showerror("Kļūda", "Neizdevās nolasīt VSOAIe atskaiti par 2021.gada janvāri!")
            return False
        elif gads2!= 2021 or menesis2 != 1:
            messagebox.showerror("Kļūda", "Atskaites failā 2021-1 ir kļūdains periods ("+str(gads2)+"-"+str(menesis2)+")")
            return False
        if hasTab4 == False:
            new = ET.Element('Tab4')
            root.append(new)
        data2 = []
        for i in root2:
            if str(i.tag)[:3] == 'Tab':
                for j in i:
                    hasDarbaVeids = False
                    for z in j:
                        if str(z.tag) in ['Ienakumi','Iemaksas']:
                            #print(z.tag, z.text)
                            #j.remove(z)
                            z.text = "0"
                        if str(z.tag) == 'Stundas':
                            z.text = "0"
                        if str(z.tag) == 'RiskaNodeva':
                            z.text = '0'
                        if str(z.tag) == 'RiskaNodevasPazime':
                            z.text = 'false'
                        if str(z.tag) == 'DarbaVeids':
                            hasDarbaVeids = True
                            z.text = 'G'
                    if hasDarbaVeids == False:
                        new = ET.Element('DarbaVeids')
                        new.text = 'G'
                        j.append(new)
                    data2.append(j)

        if len(data2) == 0:
            messagebox.showerror("Kļūda", "Atskaites par 2021.gada janvāri netika atrasti dati ko apstrādāt!")
            return False
        for i in root:
            if str(i.tag) == 'Tab4':
                for d in data2:
                    i.append(d)
        tree = ElementTree(root)
        file_name = filedialog.asksaveasfilename(confirmoverwrite=False, title = "Saglabāt failu",
						filetypes = (("XML datne","*.xml"),("Visi faili","*.*")))
        if file_name == "":
            messagebox.showerror("Kļūda", "Faila nosaukums netika norādīts!")
            return False
        try:
            tree.write(file_name, encoding="UTF-8")
            messagebox.showinfo("Informācija", "Atskaites apvienotas veiksmīgi!")
        except:
            messagebox.showerror("Kļūda", "Apvienoto failu izveidot neizdevās!")

        

if __name__ == '__main__':
    SocialApp()