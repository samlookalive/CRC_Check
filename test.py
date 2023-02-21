import os
from tkinter import filedialog
from tkinter import messagebox

import tkinter

polynominal = 0XEDB88320

def u32(n):
      return n & 0xFFFFFFFF

def makecrctable():
      table = list()
      for i in range(256) :
            k = i
            for j in range(8) :
                  if (k & 1) :
                        k = (k >> 1) ^ polynominal
                  else :
                        k >>= 1
            table.append(k)
      return table

def calcCRC(infp):
      mytable = makecrctable()
      CRC = u32(~0)
      while (byte := infp.read(1)):
            CRC = u32(mytable[(CRC ^ int.from_bytes(byte, "big")) & 0XFF ] ^ (CRC >> 8))
      return u32(~CRC)

tk = tkinter.Tk()
tk.title('CRC32 Calculator')
tk.geometry('300x100+50+50')
tk.option_add('*Font', '맑은고딕 25')
files = filedialog.askopenfilename(initialdir="/",\
                 title = "파일을 선택 해 주세요",\
                 filetypes = (("all files","*"), ("hex files","*hex"),("binary files","*bin")))
#files 변수에 선택 파일 경로 넣기

if files == '':
      messagebox.showwarning("경고", "파일을 추가 하세요")    #파일 선택 안했을 때 메세지 출력
else :
      label_file = tkinter.Label(tk, text='File Name').grid(row=0, column=0)
      
      label_crc = tkinter.Label(tk, text='CRC32 ').grid(row=1, column=0)

      entry = tkinter.Entry(tk, width=25).grid(row=0, column=1)
      entry.insert(0,files)
      #entry.pack(padx=5, pady=5)
      mytable = range(0,256)

      fp = open(files, 'rb')
      entry_crc = tkinter.Entry(tk, text=hex(calcCRC(fp)),width=25).grid(row=1, column=1)
      #entry_crc.insert(2, hex(calcCRC(fp)))
      #entry_crc.pack(padx=5, pady=5)

      tk.mainloop()
