#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Jean-Rémy Bancel <jean-remy.bancel@telecom-paristech.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Chromagon Project nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Jean-Rémy Bancel BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Chrome Cache Entry
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import datetime
import struct
import random

from Model.ChromeModel.Cache.cacheAddress import CacheAddress, CacheAddressError
from Model.ChromeModel.Cache.cacheData import CacheData

from Model.ChromeModel.Cache.base import (
    BaseCacheClass,
    BaseAttribute,
    DT_WEBKIT,
    OTHER
)

from Model.util import log_message

CREATEDAT = "Erstellt am"
URL = "Url"

class CacheEntry(BaseCacheClass):
    """
    See /net/disk_cache/disk_format.h for details.
    """
    STATE = ["Normal",
             "Evicted (data were deleted)",
             "Doomed (shit happened)"]

    def __init__(self, address):
        """
        Parse a Chrome Cache Entry at the given address
        """
        self.addr = address
        self.httpHeader = None
        block = open(address.path + address.fileSelector, 'rb')

        # Going to the right entry
        block.seek(8192 + address.blockNumber*address.entrySize)

        # Parsing basic fields
        self.hash = struct.unpack('I', block.read(4))[0]
        self.next = struct.unpack('I', block.read(4))[0]
        self.rankingNode = struct.unpack('I', block.read(4))[0]
        self.usageCounter = struct.unpack('I', block.read(4))[0]
        self.reuseCounter = struct.unpack('I', block.read(4))[0]
        self.state = struct.unpack('I', block.read(4))[0]
        self.creationTime = struct.unpack('Q', block.read(8))[0]
        self.keyLength = struct.unpack('I', block.read(4))[0]
        self.keyAddress = struct.unpack('I', block.read(4))[0]


        dataSize = []
        for _ in range(4):
            dataSize.append(struct.unpack('I', block.read(4))[0])

        self.data = []
        for index in range(4):
            addr = struct.unpack('I', block.read(4))[0]
            try:
                addr = CacheAddress(addr, address.path)
                self.data.append(CacheData(addr, dataSize[index],
                                                     True))
            except CacheAddressError:
                pass

        # Find the HTTP header if there is one
        for data in self.data:
            if data.type == CacheData.HTTP_HEADER:
                self.httpHeader = data
                break

        self.flags = struct.unpack('I', block.read(4))[0]

        # Skipping pad
        block.seek(5*4, 1)

        # Reading local key
        if self.keyAddress == 0:
            self.key = struct.unpack(str(self.keyLength)+'s', block.read(self.keyLength))[0]
            #self.key = ""
            #for _ in range(self.keyLength):
                #self.key += str(struct.unpack('c', block.read(1))[0])
        # Key stored elsewhere
        else:
            addr = CacheAddress(self.keyAddress, address.path)

            # It is probably an HTTP header
            self.key = CacheData(addr, self.keyLength, True)

        block.close()
        self.init()

    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.key))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.creationTime))
 

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Cache", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.creationTime = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cache für " + attr.name, "error")
                    continue
                self.is_date_changed = True

    
    def keyToStr(self):
        """
        Since the key can be a string or a CacheData object, this function is an
        utility to display the content of the key whatever type is it.
        """
        if self.keyAddress == 0:
            return self.key
        else:
            return self.key.data()
    
    def __str__(self):
        string = "Hash: 0x%08x" % self.hash + '\n'
        if self.next != 0:
            string += "Next: 0x%08x" % self.next + '\n'
        string += "Usage Counter: %d" % self.usageCounter + '\n'\
                  "Reuse Counter: %d" % self.reuseCounter + '\n'\
                  "Creation Time: %s" % self.creationTime + '\n'
        if self.keyAddress != 0:
            string += "Key Address: 0x%08x" % self.keyAddress + '\n'
        string += "Key: %s" % self.key + '\n'
        if self.flags != 0:
            string += "Flags: 0x%08x" % self.flags + '\n'
        string += "State: %s" % CacheEntry.STATE[self.state]
        for data in self.data:
            string += "\nData (%d bytes) at 0x%08x : %s" % (data.size,
                                                            data.address.addr,
                                                            data)
        if self.httpHeader:
            string += str(self.httpHeader.headers)
            if "date" in self.httpHeader.headers:
                string += "\n" + self.httpHeader.headers["date"]
            if "expires" in self.httpHeader.headers:
                string += "\n" + self.httpHeader.headers["expires"]
            if "last-modified" in self.httpHeader.headers:
                string += "\n" + self.httpHeader.headers["last-modified"]
        return string
