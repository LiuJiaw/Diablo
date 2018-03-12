# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 11:54:02 2018

@author: Administrator
"""

import requests
import search
import os
import sys

headers={
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'d3.blizzard.cn',  
    'Referer':'http://d3.blizzard.cn/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
}

class Player:            
    #初始化
    def __init__(self):
        self.BattleTag=''
        self.PlayerUrl=''
        self.html=''
        #PlayerCareerDate为记录杀怪数量和巅峰等级的对象
        self.PlayerCareerDate=PlayerCareer()
        #PlayerTimePercentDate为记录各职业游戏时间百分比的对象
        self.PlayerTimePercentDate=PlayerTimePercent()
        #RoleUrlDate为记录各角色id的对象
        self.RoleIDDate=Role_ID()
    #生成玩家Url   
    def buildPlayerUrl(self,BattleTag):
        self.BattleTag=BattleTag
        self.PlayerUrl='http://d3.blizzard.cn/action/profile/career/'+self.BattleTag
    #获取当前玩家主页的html
    def gethtml(self):
        response=requests.get(self.PlayerUrl,headers=headers,timeout=3)
        self.html=response.text 
    #检测本地是否存有该玩家数据
    def checkIsExisted(self):
        filename=Dirname=('save/'+self.BattleTag).decode('utf-8').encode('gb2312')+'/career.txt'
        if not os.path.exists(filename):
            return 0
        return 1    
    #读取本地的玩家数据
    def offlinegethtml(self):
        filename=Dirname=('save/'+self.BattleTag).decode('utf-8').encode('gb2312')+'/career.txt'
        f=open(filename,"r")
        self.html=f.read()
        f.close
    #展示玩家信息
    def ShowPlayerInformation(self):
        print '***********************************************'
        print '*                 玩家信息                    *'
        print '***********************************************'
        print self.BattleTag
        print self.PlayerUrl
        self.PlayerCareerDate.Show()
        self.PlayerTimePercentDate.Show()
        self.RoleIDDate.Show()
    #存储玩家信息    
    #def Save(self):
     #   if not os.path.exists(self.BattleTag):
     #       os.mkdir(self.BattleTag)
     #   print '正在保存玩家生涯数据...'
     #   filename=self.BattleTag+'/'+'career.txt'
     #   f=open(filename,'w')
     #   f.write(self.BattleTag.encode('utf-8')+'\n')
     #   f.write(self.PlayerUrl.encode('utf-8')+'\n')
     #   f.write(str(self.PlayerCareerDate.MonsterNumKills)+'\n')
     #   f.write(str(self.PlayerCareerDate.EliteNumKills)+'\n')
     #   f.write(str(self.PlayerCareerDate.PeakLevel)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.barbarian)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.crusader)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.demon_hunter)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.monk)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.witch_doctor)+'\n')
     #   f.write(str(self.PlayerTimePercentDate.wizard)+'\n')
     #   for row in self.RoleIDDate.role_id:
     #       f.write(row['ID']+'\n')
     #   f.close()
    #将该玩家的html存储至本地    
    def Savehtml(self):
        Dirname=('save/'+self.BattleTag).decode('utf-8').encode('gb2312')
        if not os.path.exists(Dirname):
            os.mkdir(Dirname)
        filename=Dirname+'/career.txt'.decode('utf-8').encode('gb2312')
        f=open(filename,'w')
        f.write(self.html.encode('utf-8'))
        f.close()
        
    def getRoleID(self):
        return self.RoleIDDate.role_id
        
class Role:
    def __init__(self):
        self.Role_ID={
            "BattleTag":'',
            "ID":''
        }
        self.Role_Url=''
        self.html=''
        #SkillList存储技能
        self.SkillList=[]
        #Attributes存储主要属性
        self.Attributes=[]
        #Equip存储角色13件装备信息        
        self.Equip=Equipment()
        
    def getRoleUrl(self,role_id):
        self.Role_ID=role_id
        self.Role_Url='http://d3.blizzard.cn/action/profile/career/'+self.Role_ID["BattleTag"].decode('utf-8')+'/hero/'+self.Role_ID["ID"]
        
    def gethtml(self,Url):
        response=requests.get(Url,headers=headers)
        html=response.text
        return html    
    #查询角色网上数据    
    def searchInformation(self):
        self.html=self.gethtml(self.Role_Url)
        self.SkillList=search._getRoleSkills(self.html)
        self.Attributes=search._getRoleAttributes(self.html)
        self.Equip.SetDate(self.html)
    #检测角色数据在本地是否存在    
    def checkIsExisted(self):
        filename=('save/'+self.Role_ID["BattleTag"]).decode('utf-8').encode('gb2312')+'/'+self.Role_ID["ID"].encode('gb2312')+'.txt'
        if not os.path.exists(filename):
            return 0
        return 1
    #查询角色本地数据    
    def OfflineInformation(self):
        filename=('save/'+self.Role_ID["BattleTag"]).decode('utf-8').encode('gb2312')+'/'+self.Role_ID["ID"].encode('gb2312')+'.txt'
        f=open(filename,'r')
        self.html=f.read()
        f.close()
        self.SkillList=search._getRoleSkills(self.html)
        self.Attributes=search._getRoleAttributes(self.html)
        self.Equip.SetDate(self.html)
    #展示角色信息    
    def ShowInformation(self):
        print '-----------------------------------------------------------'
        print '                          start                            '
        print '-----------------------------------------------------------'
        print "****************主要技能****************"
        for row in self.SkillList[0:3]:
            text=row[0]+':'+row[1]+'\t'
            sys.stdout.write(text)
        print ''
        for row in self.SkillList[3:6]:
            text=row[0]+':'+row[1]+'\t'
            sys.stdout.write(text)
        print ''
        print "****************辅助技能****************"
        for row in self.SkillList[6:10]:
            sys.stdout.write(row)
            sys.stdout.write('\t')
        print ''
        print "****************主要属性****************"
        for row in self.Attributes[0:3]:
            text=row[1]+':'+row[0]+'\t'
            sys.stdout.write(text)
        print ''
        for row in self.Attributes[3:5]:
            text=row[1]+':'+row[0]+'\t'
            sys.stdout.write(text)
        print ''
        print "****************装备信息****************"
        self.Equip.Show()
        print '-----------------------------------------------------------'
        print '                           end                             '
        print '-----------------------------------------------------------'
        
    #保存数据    
    #def Save(self):
    #    if not os.path.exists(self.Role_ID["BattleTag"]):
    #        os.mkdir(self.Role_ID["BattleTag"])
    #    print "正在保存角色ID为%s的数据"%(self.Role_ID["ID"].encode('utf-8'))
    #    filename=self.Role_ID["BattleTag"]+'/'+self.Role_ID["ID"]+'.txt'
    #    f=open(filename,'w')
    #    for row in self.SkillList[0:6]:
    #        f.write(row[0].encode('utf-8')+row[1].encode('utf-8')+'\n')
    #    for row in self.SkillList[6:10]:
    #        f.write(row.encode('utf-8')+'\n')
    #    f.close()
        
    #将角色的html写入文件    
    def Savehtml(self):
        Dirname=('save/'+self.Role_ID["BattleTag"]).decode('utf-8').encode('gb2312')
        if not os.path.exists(Dirname):
            os.mkdir(Dirname)
        filename=Dirname+'/'+self.Role_ID["ID"].encode('gb2312')+'.txt'
        f=open(filename,'w')
        f.write(self.html.encode('utf-8'))
        f.close()
        
        
class PlayerCareer: 
    def __init__(self):
        #怪物杀害数量
        self.MonsterNumKills=0
        #精英怪杀死数量
        self.EliteNumKills=0
        #巅峰等级
        self.PeakLevel=0
    #设置数据
    def SetDate(self,Tuple):
        self.MonsterNumKills=Tuple[0]
        self.EliteNumKills=Tuple[1]
        self.PeakLevel=Tuple[2]
    def Show(self):
        print "怪物杀死数量：",self.MonsterNumKills
        print "精英杀死数量：",self.EliteNumKills
        print "巅峰等级：",self.PeakLevel
        

class PlayerTimePercent:
    def __init__(self):
        #野蛮人游戏时间占比
        self.barbarian=0
        #圣教军游戏时间占比
        self.crusader=0
        #猎魔人游戏时间占比
        self.demon_hunter=0
        #武僧游戏时间占比
        self.monk=0
        #死灵法师游戏时间占比            
        self.necromancer=0
        #巫医游戏时间占比            
        self.witch_doctor=0
        #魔法师游戏时间占比            
        self.wizard=0
        
    def SetDate(self,List):
        self.barbarian=List[0]
        self.crusader=List[1]
        self.demon_hunter=List[2]
        self.monk=List[3]
        self.necromancer=List[4]
        self.witch_doctor=List[5]
        self.wizard=List[6]
        
    def Show(self):
        print ("死灵法师:%s".decode('utf-8'))%(self.necromancer)
        print ("巫医:%s".decode('utf-8'))%(self.witch_doctor)
        print ("魔法师:%s".decode('utf-8'))%(self.wizard)
        print ("野蛮人:%s".decode('utf-8'))%(self.barbarian)
        print ("圣教军:%s".decode('utf-8'))%(self.crusader)
        print ("猎魔人:%s".decode('utf-8'))%(self.demon_hunter)
        print ("武僧:%s".decode('utf-8'))%(self.monk)

        
class Role_ID:
    def __init__(self):
        #role_id为字典类型列表，存储每个玩家的角色的BattleTag和数字ID
        self.role_id=[]
        self.count=0
        
    def SetDate(self,BattleTag,List):
        self.count=len(List)
        for row in List:
            ID_Dic={"BattleTag":BattleTag,
                    "ID":row
            }
            self.role_id.append(ID_Dic)            
            
    def Show(self):
        for i in range(0,self.count):
            print self.role_id[i]["ID"],self.role_id[i]["BattleTag"]
            
class Equipment:
    def __init__(self):
        #头部名称及属性
        self.Head=EquipDetail()
        #躯干名称及属性
        self.Torso=EquipDetail()
        #足部名称及属性
        self.Feet=EquipDetail()
        #手部名称及属性
        self.Hands=EquipDetail()
        #肩部名称及属性
        self.Shoulders=EquipDetail()
        #腿部名称及属性
        self.Legs=EquipDetail()
        #护腕名称及属性
        self.Bracers=EquipDetail()
        #主手名称及属性
        self.MainHand=EquipDetail()
        #副手名称及属性
        self.OffHand=EquipDetail()
        #腰部名称及属性
        self.Waist=EquipDetail()
        #右指环名称及属性
        self.RightFinger=EquipDetail()
        #左指环名称及属性
        self.LeftFinger=EquipDetail()
        #颈部名称及属性
        self.Neck=EquipDetail()
        
    def SetDate(self,html):
        print "获取角色装备信息..."
        soup=search.getSoup(html)
        #分别爬取各装备名称及词缀
        self.Head=search.getEquip(soup,'head')
        self.Torso=search.getEquip(soup,'torso')
        self.Feet=search.getEquip(soup,'feet')
        self.Hands=search.getEquip(soup,'hands')
        self.Shoulders=search.getEquip(soup,'shoulders')
        self.Legs=search.getEquip(soup,'legs')
        self.Bracers=search.getEquip(soup,'bracers')
        self.MainHand=search.getEquip(soup,'mainHand')
        self.OffHand=search.getEquip(soup,'offHand')
        self.Waist=search.getEquip(soup,'waist')
        self.RightFinger=search.getEquip(soup,'rightFinger')
        self.LeftFinger=search.getEquip(soup,'leftFinger')
        self.Neck=search.getEquip(soup,'neck')
        
    def Show(self):
        print "**头部装备信息**"
        if self.Head.name:
            print self.Head.name
            for row in self.Head.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到头部信息...".decode('utf-8')
            
        print "**躯干装备信息**"
        if self.Torso.name:
            print self.Torso.name
            for row in self.Torso.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到躯干信息...".decode('utf-8')
        
        print "**足部装备信息**"        
        if self.Feet.name:
            print self.Feet.name
            for row in self.Feet.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到足部信息...".decode('utf-8')
        
        print "**手部装备信息**"
        if self.Hands.name:
            print self.Hands.name
            for row in self.Hands.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到手部信息...".decode('utf-8')
        
        print "**肩部装备信息**"
        if self.Shoulders.name:
            print self.Shoulders.name
            for row in self.Shoulders.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到肩部信息...".decode('utf-8')
        
        print "**腿部装备信息**"
        if self.Legs.name:
            print self.Legs.name
            for row in self.Legs.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到腿部信息...".decode('utf-8')
        
        print "**护腕装备信息**"
        if self.Bracers.name:
            print self.Bracers.name
            for row in self.Bracers.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到护腕信息...".decode('utf-8')
         
        print "**主手武器装备信息**"
        if self.MainHand.name:
            print self.MainHand.name
            for row in self.MainHand.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到主手武器信息...".decode('utf-8')
            
        print "**副手装备信息**"
        if self.OffHand.name:
            print self.OffHand.name
            for row in self.OffHand.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到副手信息...".decode('utf-8')
        
        print "**腰部装备信息**"
        if self.Waist.name:
            print self.Waist.name
            for row in self.Waist.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到腰部信息...".decode('utf-8')
        
        print "**左手指环装备信息**"
        if self.LeftFinger.name:
            print self.LeftFinger.name
            for row in self.LeftFinger.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到左手指环信息...".decode('utf-8')
        
        print "**右手指环装备信息**"
        if self.RightFinger.name:
            print self.RightFinger.name
            for row in self.RightFinger.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到右手指环信息...".decode('utf-8')
        
        print "**项链装备信息**"
        if self.Neck.name:
            print self.Neck.name
            for row in self.Neck.detail:
                sys.stdout.write(row[0]+':'+row[1]+'    ')
            print ''
        else:
            print "没有找到项链信息...".decode('utf-8')
            
            
        
class EquipDetail:
    def __init__(self):
        self.name=''
        self.detail=[]
        