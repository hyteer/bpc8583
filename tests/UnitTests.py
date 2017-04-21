#!/usr/bin/env python

import os
import time
import sys
import binascii
import unittest

from bpc8583.ISO8583 import ISO8583, ParseError
from bpc8583.py8583spec import IsoSpec1987ASCII, IsoSpec1987BCD

class AsciiParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = ISO8583(IsoSpec = IsoSpec1987ASCII())
        self.IsoPacket.Strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
                    for b4 in range(0, 5):
                        MTI = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.SetIsoContent((MTI + "0000000000000000").encode('latin'))
                        self.assertEqual(self.IsoPacket.MTI(), MTI)
    
        # negative test
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent("000A".encode('latin'))
            
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent("0000".encode('latin'))
            
        for b4 in range(6, 9):
            with self.assertRaisesRegex(ParseError, "Invalid MTI"):
                MTI = "010" + str(b4)
                self.IsoPacket.SetIsoContent(MTI.encode('latin'))
                
    def test_Bitmap(self):
        
        # Primary bitmap
        for shift in range(0, 63):
            bitmap = '{:0>16X}'.format(1 << shift)
            content = '0200' +  bitmap + ''.zfill(256)

            self.IsoPacket.SetIsoContent(content.encode('latin'))
            self.assertEqual(self.IsoPacket.Bitmap()[64 - shift], 1)
            self.assertEqual(self.IsoPacket.Field(64 - shift), 1)
            
        # Secondary bitmap
        for shift in range(0, 64):
            bitmap = '8{:0>31X}'.format(1 << shift)
            content = '0200' +  bitmap + ''.zfill(256)
            
            self.IsoPacket.SetIsoContent(content.encode('latin'))
            self.assertEqual(self.IsoPacket.Bitmap()[128 - shift], 1)
            self.assertEqual(self.IsoPacket.Field(128 - shift), 1)
                
class BCDParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = ISO8583(IsoSpec = IsoSpec1987BCD())
        self.IsoPacket.Strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
                    for b4 in range(0, 5):                        
                        MTI = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.SetIsoContent(binascii.unhexlify(MTI + "0000000000000000"))
                        self.assertEqual(self.IsoPacket.MTI(), MTI)
                        
        # negative test
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent(binascii.unhexlify("000A"))

        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent(binascii.unhexlify("0000"))
            
        for b4 in range(6, 9):
            with self.assertRaisesRegex(ParseError, "Invalid MTI"):
                MTI = binascii.unhexlify("010" + str(b4))
                self.IsoPacket.SetIsoContent(MTI)
    
    def test_Bitmap(self):
        pass
                
if __name__ == '__main__':
    unittest.main()
