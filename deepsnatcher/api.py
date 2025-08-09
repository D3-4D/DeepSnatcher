import markdown
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import asyncio
from requests_toolbelt.multipart.encoder import MultipartEncoder
from json import dumps
import logging
import requests
from typing import Union, Generator, Literal
from random import randint
import hashlib

class API:
    __Count = 0
    def __init__(self, Logger:logging.Logger=None, History:list=[], ID:str="", Language:str="en-US,en", HistoryRegistry:bool=True, Requester=requests.Session(), Stream:bool=False, Agent:str=FakeUserAgent().random, Model:str=Literal["standard","online","math"]):
        self.ID = ID or str(self.__Count)
        self.PseudoAgent=Agent
        self.Requester=Requester
        self.Model=Model
        self.HistoryRegistry=HistoryRegistry
        self.History=History
        self.Stream=Stream
        self.Lang = Language
        self.Logger=Logger

        self.RequestIdx = 0

        self.__Count+=1

        if Logger:
            Logger.info(f"SYS>Object '{ID}' created.")

    def __del__(self):
        if self.Logger:
            self.Logger.info(f"SYS>Object '{self.ID}' removed.")

    @staticmethod
    def __Hasher(String:str):
        return hashlib.md5(String.encode()).hexdigest()[::-1]
        """
            Adapt to exact hash if needed

                function generateTryitApiKey() {
                    let myrandomstr = Math.round((Math.random() * 100000000000)) + "";
                    const myhashfunction = function() {
                        for (var a = [], b = 0; 64 > b; )
                            a[b] = 0 | 4294967296 * Math.sin(++b % Math.PI);
                        return function(c) {
                            var d, e, f, g = [d = 1732584193, e = 4023233417, ~d, ~e], h = [], l = unescape(encodeURI(c)) + "\u0080", k = l.length;
                            c = --k / 4 + 2 | 15;
                            for (h[--c] = 8 * k; ~k; )
                                h[k >> 2] |= l.charCodeAt(k) << 8 * k--;
                            for (b = l = 0; b < c; b += 16) {
                                for (k = g; 64 > l; k = [f = k[3], d + ((f = k[0] + [d & e | ~d & f, f & d | ~f & e, d ^ e ^ f, e ^ (d | ~f)][k = l >> 4] + a[l] + ~~h[b | [l, 5 * l + 1, 3 * l + 5, 7 * l][k] & 15]) << (k = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][4 * k + l++ % 4]) | f >>> -k), d, e])
                                    d = k[1] | 0,
                                    e = k[2];
                                for (l = 4; l; )
                                    g[--l] += k[l]
                            }
                            for (c = ""; 32 > l; )
                                c += (g[l >> 3] >> 4 * (1 ^ l++) & 15).toString(16);
                            return c.split("").reverse().join("")
                        }
                    }();
                    const tryitApiKey = 'tryit-' + myrandomstr + '-' + myhashfunction(navigator.userAgent + myhashfunction(navigator.userAgent + myhashfunction(navigator.userAgent + myrandomstr + 'hackers_become_a_little_stinkier_every_time_they_hack')));
                    return tryitApiKey;
        """
        
    @staticmethod
    def __InternalFormatter(String:str):
        return "".join(BeautifulSoup(markdown.markdown(String), "html.parser").stripped_strings)
    
    def __KeyGen(self):
        RandomStr = str(randint(0, 10**11))
        Agent = self.PseudoAgent
        Hash = API.__Hasher

        Part = Hash(
            Agent + Hash(
                Agent + Hash(Agent + RandomStr + "hackers_become_a_little_stinkier_every_time_they_hack")
            )
        )
        ApiKey = f"tryit-{RandomStr}-{Part}"

        return ApiKey

    # LINE 2137 RELEVANT
    def Request(self, Input:str) -> list[bool, Union[str, Generator]]:
        Store = self.History if self.HistoryRegistry else []
        Store.append({"role":"user", "content":f"{Input}"})

        Encoded = MultipartEncoder(fields={
            "chat_style": "chat",
            "chatHistory":  f"{dumps(Store)}",
            "model": f"{self.Model}",
            "hacker_is_stinky": "very_stinky",
        })
        
        if self.Logger:
            self.Logger.debug(f"REQ>{self.ID}]DATA]{Encoded}")

        Headers = {
            "User-Agent": f"{self.PseudoAgent}",
            "Accept": "*/*",
            "Accept-Language": f"{self.Lang};q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "api-key": f"{self.__KeyGen()}",
            "Origin": "https://deepai.org",
            "Content-Type": f"{Encoded.content_type}",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=1, i",
        }

        if self.Logger:
            self.Logger.info(f"REQ>{self.ID}]{Encoded}")

        try:
            Response = self.Requester.post(
                "https://api.deepai.org/hacking_is_a_serious_crime",
                cookies={"user_sees_ads": "false",},
                headers=Headers,
                data=Encoded,
                stream=self.Stream,
            )
            
            if Response.status_code != 200:
                Store.pop()
            else:
                self.RequestIdx += 1
                Store.append({"role":"assistant", "content":f"{API.__InternalFormatter(Response.text)}"})
            
            if self.Logger:
                if self.Stream:
                    async def Log():
                        L = ""
                        for Piece in Response.iter_lines(decode_unicode=True):
                            L += Piece
                        self.Logger.debug(f"REQ>{self.ID}]RESPONSE]{L}")
                    asyncio.run(Log())
                else:  
                    self.Logger.debug(f"REQ>{self.ID}]RESPONSE]{Response.text}")
            return [True, [Response.status_code, Response.iter_lines(decode_unicode=True) if self.Stream else Response.text]]
        except Exception as E:
            if self.Logger:
                self.Logger.error(f"REQ>{self.ID}]{E}")
            return [False, E]
