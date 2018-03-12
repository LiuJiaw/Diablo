# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 12:43:51 2018

@author: Administrator
"""
from Player import Player
from Player import Role
import time
import search
import os
if __name__=="__main__":
    Me=Player()
    BattleTag=raw_input("请输入BattleTag：(格式：XXXXX-XXXX)\n")
    Me.buildPlayerUrl(BattleTag)
    try:
        print "正在获取玩家主页html"
        Me.gethtml()
        print "正在保存玩家主页"
        Me.Savehtml()
        netstates=1
    except:
        print "Error:无法找到玩家数据,可能原因有：\n1.无网络链接\n2.d3服务器繁忙\n3.您尚未创建角色\n4.您很长时间处于非活跃状态，需要登陆游戏！"
        netstates=0
        print "3s后查找本地数据"
        time.sleep(3)
        print "正在为你查找本地数据..."
        if Me.checkIsExisted():
            print ("本地找到%s玩家数据！")%(Me.BattleTag)
            Me.offlinegethtml()
        else:
            print "很抱歉，本地未找到该玩家数据"
            os._exit(0)
    print "正在获取玩家生涯数据"
    Me.PlayerCareerDate.SetDate(search._getPlayerCareer(Me.html))
    print "正在获取玩家各职业游戏时间百分比"
    Me.PlayerTimePercentDate.SetDate(search._getPlayerTimePercent(Me.html))
    print "正在获取玩家各角色ID"
    Me.RoleIDDate.SetDate(Me.BattleTag,search._getRoleID(Me.html))

    Me.ShowPlayerInformation()
    
    for row in Me.getRoleID():
        role=Role()
        role.getRoleUrl(row)
        if netstates==1:
            print ("获取角色ID：%s数据...")%(role.Role_ID["ID"].encode('utf-8'))
            role.searchInformation()
            role.Savehtml()
        else:
            print ("获取角色ID：%s离线数据...")%(role.Role_ID["ID"])
            if role.checkIsExisted():
                role.OfflineInformation()
            else:
                print "很抱歉，本地未发现该角色"
                continue
        role.ShowInformation()
        
    #role=Role()
    #role={"BattleTag":"gvliew-5139",
    #      "ID":"48413231"
    #      }
    #role.OfflineInformation(role)
    #role.ShowInformation()
    
    