#!/usr/bin/python3
#  -*- coding: utf-8 -*-
from modbus_lib import *
import time


class ModbusTcpServer:
    def __init__(self, ip_address, port=502):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip_address, port)
        self.sock.bind(server_address)
        self.sock.listen(10)

    def accept_con(self):
        print("wait connect")
        try:
            connect, addr = self.sock.accept()
            print("connect from :", addr)
            # while True:
            #     data = connect.recv(1000)
            #     if data:
            #         print("get data:", data)
            #         # connect.sendall(str(int(data)+1))
            #         # print("send out")
            #     else:
            #         print('none Data')
            #         time.sleep(1)
        except Exception as e:
            print(e)
            pass
        finally:
            self.sock.close()
            pass

    def recv_data(self):
        # recv result
        try:
            buf = self.sock.recv(1000)
            # show result
            print('--------- PLC packet ---------')
            in_packet = ModbusTcp.unpack(buf)
            hexdump.hexdump(buf)
            print(in_packet)
            hexdump.hexdump(in_packet.pdu.data)
        except Exception as e:
            print(e)
        finally:
            server.sock.close()

    def run(self):
        while True:

            self.accept_con()
            self.recv_data()


if __name__ == '__main__':
    server = ModbusTcpServer('127.0.0.1', 49502)
    server.run()
    #
    # packet = ModbusTcp()
    # msg=packet.pack()
    # hexdump.hexdump(msg)
    # msg = packet.pack()

