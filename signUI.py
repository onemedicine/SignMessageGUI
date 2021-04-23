#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3
import hashlib
import time

class Sign_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):
        # Title name
        self.init_window_name.title("Sign_V1.0.0")
        # Set centering
        w = 580
        h = 400
        ws = self.init_window_name.winfo_screenwidth()
        hs = self.init_window_name.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.init_window_name.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Fixed window size
        self.init_window_name.resizable(width=False, height=False)
        # Label
        self.time_label = Label(self.init_window_name, text="Time")
        self.time_label.grid(sticky=W, padx=10, pady=5)
        self.time_label.place(x=10, y=5)

        self.address_label = Label(self.init_window_name, text="ContractAddress")
        self.address_label.grid(sticky=W, padx=10, pady=5)
        self.address_label.place(x=10, y=(5 + 30 + 35) * 1)

        self.key_label = Label(self.init_window_name, text="PrivateKey")
        self.key_label.grid(sticky=W, padx=10, pady=5)
        self.key_label.place(x=10, y=5 + (30 + 35) * 2)

        self.R_label = Label(self.init_window_name, text="R", fg="red")
        self.R_label.grid(sticky=W, padx=10, pady=5)
        self.R_label.place(x=10, y=25 + (30 + 35) * 3)

        self.S_label = Label(self.init_window_name, text="S", fg="red")
        self.S_label.grid(sticky=W, padx=10, pady=5)
        self.S_label.place(x=10, y=20 + (30 + 30) * 4)

        self.V_label = Label(self.init_window_name, text="V", fg="red")
        self.V_label.grid(sticky=W, padx=10, pady=5)
        self.V_label.place(x=10, y=5 + (30 + 30) * 5)

        # Entry
        self.time_Entry = Entry(self.init_window_name, )  # time
        self.time_Entry.grid(padx=10, pady=5)
        self.time_Entry.place(x=10, y=30, width=560, height=35)
        self.time_Entry.insert('0', "1602830629")
        # self.time_Entry.configure(fg='gray')

        self.address_Entry = Entry(self.init_window_name, )  # address
        self.address_Entry.grid(padx=10, pady=5)
        self.address_Entry.place(x=10, y=(5 + 25 + 30 + 35), width=560, height=35)
        self.address_Entry.insert('0', "0x2063d5fEADC9De00628d00507e8892354Bb32cB2")

        self.key_Entry = Entry(self.init_window_name, )  # key
        self.key_Entry.grid(padx=10, pady=5)
        self.key_Entry.place(x=10, y=30 + (30 + 35) * 2, width=560, height=35)
        self.key_Entry.insert('0', "0x26414560176dbd47feec8423e12679a0cda365f79d79a8b56cc2faa11849a7f3")

        self.r_Entry = Entry(self.init_window_name, )  # r
        self.r_Entry.grid(padx=10, pady=5)
        self.r_Entry.place(x=30, y=20 + (30 + 35) * 3, width=540, height=35)
        self.r_Entry['state'] = 'readonly'

        self.s_Entry = Entry(self.init_window_name, )  # s
        self.s_Entry.grid(padx=10, pady=5)
        self.s_Entry.place(x=30, y=0 + (30 + 35) * 4, width=540, height=35)
        self.s_Entry['state'] = 'readonly'

        self.v_Entry = Entry(self.init_window_name, )  # v
        self.v_Entry.grid(padx=10, pady=5)
        self.v_Entry.place(x=30, y=5 + (30 + 30) * 5, width=540, height=35)
        self.v_Entry['state'] = 'readonly'

        # Button
        self.sig_button = Button(self.init_window_name, text="Sign", bg="lightblue", width=15,
                                 command=self.sign_hash_eth)
        # self.sig_button.grid(row=8, column=0)
        self.sig_button.grid(padx=10, pady=5)
        self.sig_button.place(x=230, y=-5 + (30 + 30) * 6)

    def sign_hash_eth(self):
        try:
            unix_time = hex(int(self.time_Entry.get()))
            unix_str64 = "0x" + unix_time[2:].zfill(64)
            unix_bytes = Web3.toBytes(hexstr=unix_str64)
            contract_address = self.address_Entry.get()
            contract_address_bytes = Web3.toBytes(hexstr=contract_address)
            eth_signature_prefix = Web3.toBytes(text="\x19Ethereum Signed Message:\n32")

            x = "0x" + hashlib.new('sha256', contract_address_bytes + unix_bytes).hexdigest()
            x_bytes = Web3.toBytes(hexstr=x)
            base = Web3.sha3(hexstr=Web3.toHex(eth_signature_prefix + x_bytes))
            sig = Account.signHash(base, self.key_Entry.get())

            # print(HexBytes(sig.signature).hex())
            # print("r:", HexBytes(sig.r).hex())
            # print("v:", HexBytes(sig.v).hex())
            # print("s:", HexBytes(sig.s).hex())
            self.r_Entry.configure(state='normal')
            self.s_Entry.configure(state='normal')
            self.v_Entry.configure(state='normal')
            self.r_Entry.delete(0, 'end')
            self.s_Entry.delete(0, 'end')
            self.v_Entry.delete(0, 'end')
            self.r_Entry.insert(0, HexBytes(sig.r).hex())
            self.r_Entry.configure(fg='red')
            self.r_Entry.configure(state='readonly')
            self.s_Entry.insert(0, HexBytes(sig.s).hex())
            self.s_Entry.configure(fg='red')
            self.s_Entry.configure(state='readonly')
            self.v_Entry.insert(0, HexBytes(sig.v).hex())
            self.v_Entry.configure(fg='red')
            self.v_Entry.configure(state='readonly')
        except:
            self.r_Entry.configure(state='normal')
            self.r_Entry.delete(0, 'end')
            self.r_Entry.insert(0, "ERROR: Sign failed!")
            self.r_Entry.configure(fg='red')
            self.r_Entry.configure(state='readonly')

    # Get the current time
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time


def gui_start():
    # Create windows
    init_window = Tk()
    ZMJ_PORTAL = Sign_GUI(init_window)
    # Setting default window properties
    ZMJ_PORTAL.set_init_window()
    # Loop, Keep window display
    init_window.mainloop()


if __name__ == '__main__':
    gui_start()
