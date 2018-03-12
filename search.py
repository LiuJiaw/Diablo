# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:57:31 2018

@author: Administrator
"""
import re
from bs4 import BeautifulSoup
    
def _getPlayerCareer(html):
    print "获取玩家生涯..."
    Re=r'<span class="num-kills">(.*?)</span>'
    Date=re.findall(Re,html) 
    monsternumkills=int(Date[0])
    elitenumkills=int(Date[1])
    peaklevel=int(Date[2][0:4])
    Tuple=(monsternumkills,elitenumkills,peaklevel)
    return Tuple
    
def _getPlayerTimePercent(html):
    print "获取玩家各职业游戏时间百分比..."
    Re=r'<h2 class="subheader-2" >.*?</h2>\s+(.+?)\s+<br />'
    Date=re.findall(Re,html)
    List=[]
    for row in Date:
        List.append(row)
    return List
    
def _getRoleID(html):
    print "获取玩家各角色URL..."
    Re_Top=r'<a class="hero-portrait-wrapper "\s+.*?\s+/(.*?)"'
    Re_other=r'<li class=".*?">\s+<a href=".*?\s+/(.*?)" data-tooltip=".*?">'
    List=[]        
    Date_top=re.findall(Re_Top,html)
    for row in Date_top:
        List.append(row)
    Date_other=re.findall(Re_other,html)
    for row in Date_other:
        List.append(row)
    return List
    
def _getRoleAttributes(html):
    print "获取玩家主属性..."
    Re_RoleAttributes=r'<span class=".*?"></span>\s+<p><span class="value">\s+(.*?)\s+</span>\s+(.*?)</p>'
    List=[]
    Data_RoleAttributes=re.findall(Re_RoleAttributes,html)
    for row in Data_RoleAttributes:
        List.append(row)
    return List
            
def getSoup(html):
    soup=BeautifulSoup(html)
    return soup

def getEquip(soup,EquipName):
    equip=EquipDetail()
    Class="gear-label slot-"+EquipName
    taglist=soup.find_all('li',class_=Class)
    try:
        name=taglist[0].find_all('span',class_="item-name")
        equip.name=name[0].contents[0].strip()
        affix=taglist[0].find_all('p')
        for row in affix:
            affixname=row.contents[2].strip()
            affixcount=row.contents[1].contents[0].strip()
            equip.detail.append([affixname,affixcount])
    except:
        return equip
    return equip
    
def _getRoleSkills(html):
    print "获取角色技能..."
    Re_MainSkills1=r'<span class="skill-name">\s*(.+?)\s+<span class="rune-name">(.*?)</span>'
    Re_AssistSkills=r'<span class="skill-name">(.*?)</span>\s+</a>'
    List=[]        
    Date_MainSkills1=re.findall(Re_MainSkills1,html)
    for row in Date_MainSkills1:
        if row[1]=='':
            if type(row[1]).__name__=='unicode':
                List.append([row[0],"未设置".decode('utf-8')]) 
            else: 
                List.append([row[0].decode('utf-8'),"未设置".decode('utf-8')])
        else:
            List.append(row)
    while len(List)<6:
        List.append(["未设置".decode('utf-8'),"未设置".decode('utf-8')])
    Date_AssistSkills=re.findall(Re_AssistSkills,html)
    for row in Date_AssistSkills:
        List.append(row)
    while len(List)<10:
        List.append("未设置".decode('utf-8'))
    return List

class EquipDetail:
    def __init__(self):
        self.name=''
        self.detail=[]
