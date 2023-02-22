import os
from tkinter import filedialog
from tkinter import messagebox
import tkinter

polynominal = 0XEDB88320
tk = tkinter.Tk()

# GUI 설정
#Set_GUIConfigure(mainWindow)
#tk.iconbitmap("CRC_Check.ico")
tk.title('Checksum(CRC32) Calculator')
tk.geometry('395x150+50+50')
tk.resizable(False, False)
tk.option_add('*Font', '맑은고딕 11')

def u32(n):
      return n & 0xFFFFFFFF

def makecrctable():
      tb = list()
      for i in range(256) :
            k = i
            for j in range(8) :
                  if (k & 1) :
                        k = (k >> 1) ^ polynominal
                  else :
                        k >>= 1
            tb.append(k)
      return tb

def calcCRC(infp):
      crctable = makecrctable()
      CRC = u32(~0)
      while (byte := infp.read(1)):
            CRC = u32(crctable[(CRC ^ int.from_bytes(byte, "big")) & 0XFF ] ^ (CRC >> 8))
      return u32(~CRC)

def OpenFile():
      try:
            # Openfile 버튼 입력 시 선택된 파일 정보 return
            filename = filedialog.askopenfilename(initialdir="/",\
                  title = "파일을 선택 해 주세요",\
                  filetypes = (("all files","*"), ("hex files","*hex"),("binary files","*bin")))
            if filename :
                  entry_file.delete(0, len(entry_file.get()))
                  entry_file.insert(0, filename)
                  entry_crc.delete(0, len(entry_crc.get()))
                  fp = open(filename, 'rb')
                  entry_crc.insert(0,"0x"+f'{calcCRC(fp):X}')
      except:
            messagebox.showerror("ERROR", "알수 없는 오류 발생.")

def enterinput(event):
      try:
            filename = entry_file.get()
            if filename :
                  entry_crc.delete(0, len(entry_crc.get()))
                  fp = open(filename, 'rb')
                  entry_crc.insert(0,"0x"+f'{calcCRC(fp):X}')
            else :
                  messagebox.showerror("ERROR", "파일명을 정확히 입력하세요")
      except:
            messagebox.showerror("ERROR", "입력된 파일명 혹은 위치가 정확하지 않습니다.")

label_crc = tkinter.Label(tk, text='CRC32', width =7, font=("맑은고딕",18))
label_file = tkinter.Label(tk, text='파일 경로', width=10)
entry_file = tkinter.Entry(tk, width=35)
entry_file.insert(0,"파일을 입력하거나 선택하세요.")
entry_crc = tkinter.Entry(tk, width=11, font=("맑은고딕", 30))
entry_crc.insert(0,"")
btn_load = tkinter.Button(tk, text='선택',width=8, command=lambda:OpenFile())
# add 'enter' event callback function
tk.bind("<Return>", enterinput)

label_crc.grid(padx=5, pady=20, row = 0, column= 0, sticky='s')
entry_crc.grid(padx=5, pady=22, row = 0, column= 1, columnspan=3)
label_file.grid(padx=8, pady=1, row = 1, column= 0, sticky='w')
entry_file.grid(padx=8, pady=1, row = 2, column= 0, columnspan=3)
btn_load.grid(padx=1, pady=1, row = 2, column= 3)

tk.mainloop()
