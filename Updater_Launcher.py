#-*- coding: utf-8 -*-

#Imports
#Imports
import wx
import hashlib
import base64
import urllib
import time
import wx.html2
import os
from os.path import *
from os import getcwd
import requests
from bs4 import BeautifulSoup
import glob
import winreg
import webbrowser
import threading
import subprocess
import platform

#IDs
ID_SETTINGS= wx.NewIdRef()
ID_EXIT= wx.NewIdRef()

#Init var url
file_config_changed=0
file_is_ok=0

#LISTES // LISTS
l_bonjour=[]
l_err_parse=[u"ERREUR !\n\nIMPOSSIBLE DE PARSER\nLE SERVEUR D'UPLOAD !",u"ERROR !\n\nIMPOSSIBLE TO PARSE\nUPLOAD SERVER !"]
l_update=[u"MISE A JOUR",u"UPDATE"]
l_config=[u"CONFIG SERVEUR",u"CONFIG SERVER"]
l_start=[u"DEMARRER LE JEU !",u"START THE GAME !"]
l_site=[u"SITE WEB",u"WEBSITE"]
l_updater=[u"MISE A JOUR :", u"UPDATER :"]
l_info=[u"INFORMATIONS :"]
l_launch=[u"LANCEUR :",u"LAUNCHER :"]
l_settings=[u"CONFIG :",u"SETTINGS :"]
l_paypal=[u"DON POUR LE DEV :",u"DONATE FOR THE DEV :"]
l_aide_set=[u"REGLAGES",u"SETTINGS"]
l_aide_exit=[u"QUITTER",u"EXIT"]
l_set_dlg=[u"CONFIGURATION DU CLIENT",u"CLIENT SETTINGS"]
l_file_config=[u"Adresse du fichier de MaJ :",u"Update file adress :"]
l_file_config_txt=[u"Adresse fichier actuelle :",u"Current file adress :"]
l_maj_up=[u"Fichier(s) Mis a Jour : ",u"File(s) Updated : "]
l_all_up=[u"TOUS LES FICHIERS SONT A JOUR ! :)",u"ALL FILES ARE UP TO DATE ! :)"]
l_admin=["\n\nRELANCEZ EN MODE\nADMINISTRATEUR !!!","\n\nRUN AS ADMINISTRATOR !!!"]
l_bad_serv=[u"MAUVAIS FICHIER DE CONFIG !\n\nENTREZ UN CHEMIN VALIDE !\n\nCONTACTEZ UN ADMIN !",u"WRONG CONFIG FILE PATH !\n\nENTER A VALID PATH !\n\nCONTACT AN ADMIN !"]
l_404=[u"ERREUR 404\nFICHIER DE CONFIGURATION\nNON TROUVE",u"ERROR 404\nCONFIG FILE NOT FOUND"]
l_bad_file=[u"MAUVAIS DOSSIER DE DL !\n\nENTREZ UN NOM\nDE DOSSIER VALIDE !\n\nCONTACTEZ UN ADMIN !",u"WRONG DL FOLDER PATH !\n\nENTER A VALID\nFOLDER NAME !\n\nCONTACT AN ADMIN !"]
l_404_file=[u"ERREUR 404 DOSSIER NON TROUVE",u"ERROR 404 FOLDER NOT FOUND"]
l_exe=[u"Erreur Nom d'EXE",u"EXE Name Error"]
l_bad_exe=[u"Nom de l'EXE incorrect !",u"Wrong EXE name !"]
l_err_bat=[u"Erreur d'EXE non-valide !\n\nImpossible de lancer\nle jeu !\n\nContactez un ADMIN !!! ",u"Error of non-valid\nEXE name !\n\nImpossible to launch !\n\nContact an ADMIN !!!"]
l_err_net=[u"PROBLEME DE CONNEXION !\n\nVERIFIEZ L'ETAT DU SERVEUR !\n\nOU\n\nVERIFIEZ LA CONNEXION INTERNET !",u"IMPOSSIBLE TO CONNECT !\n\nVERIFY SERVER IS ONLINE !\n\n\n\nOR\n\n\n\nVERIFY INTERNET CONNECTION !"]
l_net_title=[u"PROBLEME DE CONNEXION !",u"CONNEXION WARNING !"]
l_secu_txt=[u"/!\ ATTENTION /!\ MODIFIER CETTE ADRESSE PEUT NUIRE AU BON FONCTIONNEMENT DU CLIENT !\nNE LE FAIRE QUE SUR DEMANDE D'UN ADMIN !\nCOCHEZ LA BOX POUR CONTINUER QUAND MEME...",
                u"/!\ WARNING /!\ MODIFY THIS ADRESS CAN CAUSE CLIENT MALFUNCTION !\nDO IT ON ADMIN'S REQUEST ONLY !\nCHECK THE BOX TO CONTINUE HOWEVER..."]
l_check=[u"J'ACCEPTE",u"I ACCEPT"]
l_folder=[u"Répertoire de téléchargement :",u"Downloads folder :"]
l_donate=[u"FAIRE UN DON",u"MAKE A DONATION"]
l_err_ext=[u"DESOLE PAS DE FICHIER(S)\n\n",u"SORRY NO FILE(S)\n\n"]
l_ici=[u"\n\nICI !",u"\n\nHERE !"]
l_checksum=[u"\nCalcul du checksum de : ",u"\nCalculating remote checksum of : "]
l_no_up=[u"\n\n- LE JEU EST A JOUR...",u"\n\n- GAME ALREADY UP TO DATE..."]
l_progress=[u"PROGRESSION MAJ :",u"UPDATE PROGRESSION :"]
l_txtProg=[u"Téléchargement du fichier : ",u"Downloading file : "]
l_onoff=[u"SERVEUR D'UPLOAD :",u"UPLOAD SERVER :"]
l_btn_serv=[u"RAFRAICHIR",u"REFRESH"]
l_news=[u"DERNIERES NOUVELLES :",u"LATEST NEWS :"]
l_err_patch=[u"ERREUR DE PATCH !",u"PATCHING ERROR !"]
l_btn_patch=[u"PATCHER"]
l_patch=[u"Jeu déjà patché !\n\nEditez le fichier 'fix.conf'\net mettez sa valeur a 0\npour pouvoir repatcher",u"Game already patched !\n\nEdit 'fix.conf' file\nand put value to 0\nto be able to repatch"]
l_g_patch=[u"Le jeu a bien été patché !",u"Game patched successfuly !"]

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, u"PC GAMES Updater/Launcher V3.1 By -Fawn-",style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER)
        global l_bonjour,gbox6

        
        ###########INITIALIZING#################
        
        #Init file config adress
        self.load_serv()
        
        #Shaped window
        self.hasShape = False
        self.delta = wx.Point(0,0)
        
        ImgDir = (getcwd()+u"\\img\\FOND.png")
        self.fond = wx.Image(ImgDir, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.SetClientSize((self.fond.GetWidth(), self.fond.GetHeight()))
        self.panel = Panel(self)
        self.panel.Show()
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.fond, 0,0, True)
        self.SetWindowShape()
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)

        #Icone
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(getcwd()+u"\\img\\logo.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
        #Bouton donation // DONATE BUTTON
        self.button_don = wx.Button(self.panel, -1, l_donate[0])
        self.Bind(wx.EVT_BUTTON, self.donate, self.button_don)

        #Bouton patch
        self.button_patch = wx.Button(self.panel, -1, l_btn_patch[0])
        self.Bind(wx.EVT_BUTTON, self.fix_pangya, self.button_patch)

        #Progress bar
        self.gauge = wx.Gauge(self.panel, size = (930, 25), style =  wx.GA_HORIZONTAL)

        #Progress text
        self.txtProg = TransparentText(self.panel,-1,"")
        self.txtProg.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        
        #gauge text
        self.txtGauge = TransparentText(self.panel,-1,"")
        self.txtGauge.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        
        #Btn chck_maj
        self.chck_maj = wx.Button(self.panel,-1,l_update[0])
        self.Bind(wx.EVT_BUTTON, self.thread_update, self.chck_maj)

        #Btn start_game
        self.start_g=wx.Button(self.panel,-1,l_start[0])
        self.Bind(wx.EVT_BUTTON, self.launch_g,self.start_g )
        self.start_g.Disable()

        #Btn go fofo // BUTTON WEBSITE
        self.go_fofo = wx.Button(self.panel,-1,l_site[0])
        self.Bind(wx.EVT_BUTTON, self.fofo, self.go_fofo)
        
        #widgets
        self.AffichTxt=wx.TextCtrl(self.panel,-1,size=(220,288),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.AffichTxt.SetBackgroundColour(u'BLACK')
        self.AffichTxt.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.BOLD))
        self.AffichTxt.SetForegroundColour(u"FOREST GREEN")

        #Init Params
        self.Recup_Params()

        #Init batch
        if file_is_ok==1:
            self.write_batch()
        ########################################

        # Coder systeme pour changer texte de bienvenue ici
        if file_is_ok==1:
            try:
                file = urllib.request.urlopen(tab_line[6])
                for line in file:
                    l_bonjour.append(line.decode(u"ansi"))
                l_bonjour=''.join(l_bonjour)
                self.AffichTxt.AppendText(l_bonjour+"\n\n -Dev Contact :\n fawn06220@gmail.com")
            except:
                self.AffichTxt.AppendText("Erreur URL de serveur d'update\n\nError update server URL"+"\n\n -Dev Contact :\n fawn06220@gmail.com")


        #serv on/off
        try:
            r = requests.get(tab_line[0])
            if r.status_code==200:
                ImgDir2 = (getcwd()+u"\\img\\serv_on.png")#150x25 px
            else:
                ImgDir2 = (getcwd()+u"\\img\\serv_off.png")
        except:
            ImgDir2 = (getcwd()+u"\\img\\serv_off.png")
        img_serv = wx.Image(ImgDir2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.img=wx.StaticBitmap(self.panel, -1, img_serv)

        #News
        self.browser = wx.html2.WebView.New(self.panel,-1,size=(370,200))
        try:
            self.browser.LoadURL(tab_line[5])
        except:
            self.browser.LoadURL("")
        #########################################
        
        
        #Sizer Updater
        gbox0 = wx.GridBagSizer(1,1)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.chck_maj,(0,0))
        gbox0.Add(self.go_fofo,(0,2))
        
        #Sizer MaJ
        gbox1 = wx.GridBagSizer(1,1)
        gbox1.SetEmptyCellSize((10,10))
        gbox1.Add(self.AffichTxt,(0,1))
        
        #Sizer Launcher
        gbox2 = wx.GridBagSizer(1,1)
        gbox2.SetEmptyCellSize((10,10))
        gbox2.Add(self.start_g,(0,0))

        #Donate
        gbox3 = wx.GridBagSizer(1,1)
        gbox3.SetEmptyCellSize((10,10))
        gbox3.Add(self.button_don,(0,0))
        
        #UPDATE
        self.box0 = TransparentBox(self.panel, -1 ,l_updater[0])
        bsizer0 = wx.StaticBoxSizer(self.box0, wx.HORIZONTAL)
        sizerH0 = wx.BoxSizer(wx.VERTICAL)
        sizerH0.Add(gbox0, 0, wx.ALL|wx.CENTER, 10)
        bsizer0.Add(sizerH0, 1, wx.EXPAND, 0)

        #INFOS
        self.box1 = TransparentBox(self.panel, -1, l_info[0])
        bsizer1 = wx.StaticBoxSizer(self.box1, wx.HORIZONTAL)
        sizerH1 = wx.BoxSizer(wx.VERTICAL)
        sizerH1.Add(gbox1, 0, wx.ALL|wx.CENTER, 10)
        bsizer1.Add(sizerH1, 1, wx.EXPAND, 0)

        #LAUNCH
        self.box2 = TransparentBox(self.panel, -1, l_launch[0])
        bsizer2 = wx.StaticBoxSizer(self.box2, wx.HORIZONTAL)
        sizerH2 = wx.BoxSizer(wx.VERTICAL)
        sizerH2.Add(gbox2, 0, wx.ALL|wx.CENTER, 10)
        bsizer2.Add(sizerH2, 1, wx.EXPAND, 0)

        #PAYPAL
        self.box3 = TransparentBox(self.panel, -1, l_paypal[0])
        bsizer3 = wx.StaticBoxSizer(self.box3, wx.HORIZONTAL)
        sizerH3 = wx.BoxSizer(wx.VERTICAL)
        sizerH3.Add(gbox3, 0, wx.ALL|wx.CENTER, 10)
        bsizer3.Add(sizerH3, 1, wx.EXPAND, 0)

        #Creation barre d'outils
        self.CreerBarreOutils()

        #Sizer config
        gbox4 = wx.GridBagSizer(1,1)
        gbox4.SetEmptyCellSize((10,10))
        gbox4.Add(toolbar,(0,2),flag=wx.ALIGN_RIGHT)
        gbox4.Add(self.button_patch,(0,0))
        
        #CONFIG
        self.box4 = TransparentBox(self.panel, -1, l_settings[0])
        bsizer4 = wx.StaticBoxSizer(self.box4, wx.HORIZONTAL)
        sizerH4 = wx.BoxSizer(wx.VERTICAL)
        sizerH4.Add(gbox4, 0, wx.ALL|wx.CENTER, 10)
        bsizer4.Add(sizerH4, 1, wx.EXPAND, 0)

        #Sizer progress bar
        gbox5 = wx.GridBagSizer(1,1)
        gbox5.SetEmptyCellSize((10,10))
        gbox5.Add(self.gauge,(0,0))
        gbox5.Add(self.txtProg,(1,0))
        gbox5.Add(self.txtGauge,(2,0))

        #PROGRESS BAR
        self.box5= TransparentBox(self.panel, -1, l_progress[0])
        bsizer5 = wx.StaticBoxSizer(self.box5, wx.HORIZONTAL)
        sizerH5 = wx.BoxSizer(wx.VERTICAL)
        sizerH5.Add(gbox5, 0, wx.ALL|wx.CENTER, 10)
        bsizer5.Add(sizerH5, 1, wx.EXPAND, 0)

        #Sizer serv on/off
        gbox6 = wx.GridBagSizer(1,1)
        gbox6.SetEmptyCellSize((10,10))
        gbox6.Add(self.img,(0,0))

        #SERV ON/OFF
        self.box6= TransparentBox(self.panel, -1, l_onoff[0])
        bsizer6 = wx.StaticBoxSizer(self.box6, wx.HORIZONTAL)
        sizerH6 = wx.BoxSizer(wx.VERTICAL)
        sizerH6.Add(gbox6, 0, wx.ALL|wx.CENTER, 10)
        bsizer6.Add(sizerH6, 1, wx.EXPAND, 0)

        #Sizer news
        gbox7 = wx.GridBagSizer(1,1)
        gbox7.SetEmptyCellSize((10,10))
        gbox7.Add(self.browser,(0,0))

        #NEWS
        self.box7= TransparentBox(self.panel, -1, l_news[0])
        bsizer7 = wx.StaticBoxSizer(self.box7, wx.HORIZONTAL)
        sizerH7 = wx.BoxSizer(wx.VERTICAL)
        sizerH7.Add(gbox7, 0, wx.ALL|wx.CENTER, 10)
        bsizer7.Add(sizerH7, 1, wx.EXPAND, 0)


        #--------Ajustement du sizer----------
        vSizer1 = wx.BoxSizer(wx.VERTICAL)
        vSizer1.Add(bsizer4, 0,wx.ALL|wx.EXPAND, 10)
        vSizer1.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        vSizer1.Add(bsizer2, 0,wx.ALL|wx.EXPAND, 10)
        vSizer1.Add(bsizer3, 0,wx.ALL|wx.EXPAND, 10)
        
        vSizer2 = wx.BoxSizer(wx.VERTICAL,)
        vSizer2.Add(bsizer1, 0,wx.ALL|wx.EXPAND, 10)

        vSizer3 = wx.BoxSizer(wx.VERTICAL,)
        vSizer3.Add(bsizer6, 0,wx.ALL|wx.EXPAND, 10)
        vSizer3.Add(bsizer7, 0,wx.ALL|wx.EXPAND, 10)
        

        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer1.Add(bsizer5, 0,wx.ALL|wx.EXPAND, 10)
        

        hmainSizer=wx.BoxSizer(wx.HORIZONTAL)
        hmainSizer.Add(vSizer1, 0,wx.ALL|wx.EXPAND, 10)
        hmainSizer.Add(vSizer2, 0,wx.ALL|wx.EXPAND, 10)
        hmainSizer.Add(vSizer3, 0,wx.ALL|wx.EXPAND, 10)

        vmainSizer=wx.BoxSizer(wx.VERTICAL)
        vmainSizer.Add(hmainSizer, 0,wx.ALL|wx.EXPAND, 10)
        vmainSizer.Add(hSizer1, 0,wx.ALL|wx.EXPAND, 10)
        

        self.panel.SetSizer(vmainSizer)
        self.panel.Layout()
        
######FIX FOR PANGYA GAME CAN ERASE IF NOT NEEDED !########################################### (Don't forget to erase the call to this func)
    def fix_pangya(self,evt):
        with open(u"fix.conf",u"r")as fix_r:
            mem_fix=fix_r.readline()
            if mem_fix==u"0":
                try:
                    os_bit=platform.architecture()[0]
                    if os_bit=="64bit":
                        keyVal = r'SOFTWARE\Wow6432Node\Ntreev\PangYa_Th'
                    else:
                        keyVal = r'SOFTWARE\Ntreev\PangYa_Th'
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, keyVal)
                    winreg.SetValueEx(key, u"Launcher Version", 0,  winreg.REG_SZ, u"v3.1")
                    winreg.SetValueEx(key, u"Argument", 0,  winreg.REG_SZ, u"not_used")
                    winreg.SetValueEx(key, u"Launcher", 0,  winreg.REG_SZ, u"Updater_Launcher.exe")
                    winreg.SetValueEx(key, u"Install_Dir", 0,  winreg.REG_SZ, u"C:\Pangya eXtremV2")
                    winreg.SetValueEx(key, u"PatchNum", 0,  winreg.REG_SZ, u"184")
                    winreg.SetValueEx(key, u"IntegratedPak", 0,  winreg.REG_SZ, u"projectg500+.pak")
                    winreg.SetValueEx(key, u"Ver", 0,  winreg.REG_SZ, u"TH.R4.584.04")
                    winreg.CloseKey(key)
                    with open(u"fix.conf",u"w")as fix_w:
                        fix_w.write(u"1")
                    self.AffichTxt.Clear()
                    self.AffichTxt.SetForegroundColour(u"FOREST GREEN")
                    self.AffichTxt.AppendText(l_g_patch[0])
                except:
                    self.AffichTxt.Clear()
                    self.AffichTxt.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                    self.AffichTxt.SetForegroundColour(u"RED")
                    self.AffichTxt.AppendText(l_err_patch[0]+"\n\n"+l_admin[0])     #l_admin language key (del if needed)
                    self.chck_maj.Disable()
            else:
                self.AffichTxt.Clear()
                self.AffichTxt.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                self.AffichTxt.SetForegroundColour(u"RED")
                self.AffichTxt.AppendText(l_patch[0])
                self.button_patch.Disable()
            
###########################################################################################

    def SetWindowShape(self, evt=None):
        r = wx.Region(self.fond,wx.TransparentColour)
        self.hasShape = self.SetShape(r)

    def OnDoubleClick(self, evt):
        if self.hasShape:
            self.SetShape(wx.Region())
            self.hasShape = False
        else:
            self.SetWindowShape()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.fond, 0,0, True)

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        pos = self.ClientToScreen(evt.GetPosition())
        origin = self.GetPosition()
        self.delta = wx.Point(pos.x - origin.x, pos.y - origin.y)

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            pos = self.ClientToScreen(evt.GetPosition())
            newPos = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.Move(newPos)

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def thread_serv(self,evt):
        thread = threading.Thread(target=self.servonoff)
        thread.start()
        
    def thread_update(self,evt):
        thread = threading.Thread(target=self.updater)
        thread.start()

    def no_internet(self):
        global no_net
        alert=wx.MessageDialog(self,l_err_net[0], l_net_title[0],wx.OK | wx.ICON_ERROR)
        alert.ShowModal()
        self.start_g.Disable()
        no_net=1
    
    def donate(self,evt):
        url=u"https://www.paypal.com/paypalme/noobpythondev"
        webbrowser.open(url)
        evt.Skip()

    def Recup_Params(self):# Recup donnees de client_config.conf
        global tab_line,file_config_changed,file_is_ok,no_net
        tab_line=[]
        #RECUP PARAMS
        try:
            response = requests.get(mem_url)
            if response.status_code==200:
                for line in response.text.splitlines():
                    ligne_clean=line.rstrip()
                    tab_line.append(ligne_clean)
                    file_is_ok=1
                    no_net=0
        except:
            self.AffichTxt.Clear()
            self.AffichTxt.SetForegroundColour(u"RED")
            self.AffichTxt.AppendText(l_err_net[0])
            #Disable net connected buttons#
            self.no_internet()
            ###############################
            file_is_ok=0
            
        
    def CreerBarreOutils(self): # Pour creation de la barre d'outils
        global toolbar
      
        taille=(32,32) #Definition d'une variable de taille pour les icones.
        toolbar = wx.ToolBar(self.panel,size=(90,40)) #Definition des attributs de la barre d'outils.
        toolbar.SetBackgroundColour("WHITE")
        img_settings=wx.Image(getcwd()+u"\\img\\SETTINGS.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        img_exit=wx.Image(getcwd()+u"\\img\\exit.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        tool_settings=toolbar.AddTool(ID_SETTINGS,u"Settings",img_settings,shortHelp=str(l_aide_set[0]))

        toolbar.AddSeparator()

        tool_exit=toolbar.AddTool(ID_EXIT,u"Exit",img_exit,shortHelp=str(l_aide_exit[0]))
        
        toolbar.Realize() #Creation de la barre d'outils.

        self.Bind(wx.EVT_TOOL,self.settings,tool_settings)
        self.Bind(wx.EVT_TOOL,self.on_close,tool_exit)

    def settings(self,evt):
        global file_config_changed,serv_file_config,exist_conf
        
        dlg=GetData(self,title=l_set_dlg[0])

        #Show actual file adress
        self.load_serv()
        dlg.file_config_txt_vide.SetLabel(mem_url)

        dlg.ShowModal()
        if dlg.ShowModal()==wx.ID_OK:
            #file_config
            serv_file_config=dlg.file_config_val
            if (dlg.file_config_val!=u"http://" and dlg.file_config_val!=""):
                file_config_changed=1
                self.save_serv(dlg.file_config_val)
                self.write_batch()
        evt.Skip()
                
        
    def fofo(self,evt): 
        global tab_line,file_config_changed

        #Load new file hack
        if file_config_changed==1:
            self.load_serv()
            self.Recup_Params()
            
        if file_is_ok==1:
            url=tab_line[1].rstrip()
            webbrowser.open(url)
        else:
            self.AffichTxt.Clear()
            self.AffichTxt.SetForegroundColour(u"RED")
            self.AffichTxt.AppendText(l_err_net[0])
            self.start_g.Disable()
        evt.Skip()
            
    def load_serv(self):
        global mem_url
        with open(u"file_config.conf",u"r") as file_config:
            mem_url=file_config.readline()
            
    def save_serv(self,s_url):
        with open(u"file_config.conf",u"w") as file_config:
                file_config.write(s_url)
        
    def write_batch(self):
        global tab_line
        exe_name=tab_line[3].rstrip()
        with open(u"start_game.bat",u"w") as start:
            start.writelines([u"@echo off \n",
                                u"Start "+exe_name])
                
    def launch_g(self,evt):
        global file_is_ok
        
        if file_is_ok==1:
            os.system(u"start_game.bat")
            self.on_close(evt)
        else:
            alert=wx.MessageDialog(self,l_bad_exe[0], l_exe[0] ,wx.OK | wx.ICON_ERROR)
            alert.ShowModal()
            self.start_g.Disable()
            self.AffichTxt.Clear()
            self.AffichTxt.SetForegroundColour(u"RED")
            self.AffichTxt.AppendText(l_err_bat[0])

    def md5Checksum(self,filePath,url):
        m = hashlib.md5()
        if url==None:
            with open(filePath, u'rb') as fh:
                m = hashlib.md5()
                while True:
                    data = fh.read(8192)
                    if not data:
                        break
                    m.update(data)
                return base64.b64encode(m.digest()).decode('ascii')
                
        else:
            self.gauge.Pulse()
            try:
                r = requests.head(url)
                return r.headers['Content-MD5']
                no_net=0
            except:
                self.no_internet()
        
    def updater(self):
        global tab_line,file_config_changed,file_is_ok,no_net
        tab_remote=[]
        tab_local=[]
        liste_loc_ext=[]
        mem_pak=[]
        folder_ok=0
        chunk_size=1024


        self.load_serv()
        if mem_url!="":
            file_config_changed=1
        #Load new file hack
            self.Recup_Params()
            #self.refresh_app()

            if file_is_ok==1:
                #FOLDER EXISTS VERIF
                if(tab_line[4]==u"none"):
                    folder_ok=1
                if exists(getcwd()+u"\\"+tab_line[4]):
                    folder_ok=2

                if folder_ok==1 or folder_ok==2:
                    #REMOTE
                    liste_ext=tab_line[2].rstrip().split(u",")
                    ext = tuple(liste_ext)
                    for elem in liste_ext:
                        elem = u"*."+elem
                        liste_loc_ext.append(elem)
                    tpl_loc_ext=tuple(liste_loc_ext)
                    url = tab_line[0].rstrip()
                    if url[-1:]==u"/":
                        pass
                    else:
                        url=url+u"/"
                    try:
                        r = requests.get(url,stream=True).text
                        soup = BeautifulSoup(r, u'html.parser')
                        links_pak=[url + u'/' + node.get(u'href') for node in soup.find_all(u'a') if node.get(u'href').endswith(ext)]
                        if len(links_pak)!=0:
                            for file in links_pak:
                                nom_de_fichier=file.rsplit(u'/',1)[1]
                                tab_remote.append(nom_de_fichier)
                        else:
                            self.AffichTxt.Clear()
                            self.AffichTxt.SetForegroundColour(u"RED")
                            self.AffichTxt.AppendText(l_err_parse[0])
                            return
                        no_net=0
                    except:
                        self.no_internet()
                        #LOCAL
                    if tab_line[4]==u"none":
                        for files in tpl_loc_ext:
                            tab_local.extend(glob.glob(files))
                    else:
                        tab_local=os.listdir(getcwd()+u"\\"+tab_line[4])
                    #difference
                    tab_local, tab_remote=set(tab_local), set(tab_remote)
                    ver_diff=tab_remote.difference(tab_local)
                    lst_ver_diff=sorted(list(ver_diff))
        
                    #meme fichiers
                    ver_same=tab_remote.intersection(tab_local)
                    lst_ver_same=sorted(list(ver_same))
                
                    if lst_ver_same!=[]:
                        j=0
                        while j<len(lst_ver_same):
                            #taille fichier local identique
                            if tab_line[4]==u"none":
                                checksum_fichier_local=self.md5Checksum(lst_ver_same[j],None)
                            else:
                                checksum_fichier_local=self.md5Checksum(getcwd()+u"\\"+tab_line[4]+u"\\"+lst_ver_same[j],None)
                            #taille fichier distant identique
                            url_de_fichier_dist=url+lst_ver_same[j]
                            ########################
                            checksum_fichier_dist=self.md5Checksum(None,url_de_fichier_dist)
                            nom_de_pak_dist=url_de_fichier_dist.rsplit(u'/',1)[1]
                            self.txtProg.SetLabel(l_checksum[0]+nom_de_pak_dist)
                            ########################
                            rep = requests.get(url_de_fichier_dist, stream=True)
                            total_size = int(rep.headers.get(u'content-length', 0))
                            
                            #Check
                            if checksum_fichier_local!=checksum_fichier_dist:
                                if total_size>=(1024*1024):
                                    chunk_size=1024*1024
                                    n=round(total_size/(1024*1024))
                                    u=u"MB"
                                elif total_size>=(1024*1024*1024):
                                    chunk_size=1024*1024*1024
                                    n=round(total_size/(1024*1024*1024))
                                    u=u"GB"
                                else:
                                    n=round(total_size/1024)
                                    u=u"KB"
                                inc=0
                                self.gauge.SetRange(n)
                                if tab_line[4]!=u"none":
                                    self.txtProg.SetLabel(l_txtProg[0]+nom_de_pak_dist)
                                    with open(getcwd()+u"\\"+tab_line[4].rstrip()+u"\\"+nom_de_pak_dist,u"wb") as fichier_dl:
                                        for chunk in rep.iter_content(chunk_size=chunk_size):
                                            fichier_dl.write(chunk)#DL
                                            inc+=1
                                            if inc>=n:
                                                self.txtGauge.SetLabel(str(n)+"/"+str(n)+u)
                                                self.gauge.SetValue(n)
                                            else:
                                                self.txtGauge.SetLabel(str(inc)+"/"+str(n)+u)
                                                self.gauge.SetValue(inc)
                                        mem_pak.append("-"+nom_de_pak_dist)
                                else:
                                    self.txtProg.SetLabel(l_txtProg[0]+nom_de_pak_dist)
                                    with open(nom_de_pak_dist,u"wb") as fichier_dl:
                                        for chunk in rep.iter_content(chunk_size=chunk_size):
                                            fichier_dl.write(chunk)#DL
                                            inc+=1
                                            if inc>=n:
                                                self.txtGauge.SetLabel(str(n)+"/"+str(n)+u)
                                                self.gauge.SetValue(n)
                                            else:
                                                self.txtGauge.SetLabel(str(inc)+"/"+str(n)+u)
                                                self.gauge.SetValue(inc)
                                        mem_pak.append("-"+nom_de_pak_dist)
                            self.txtProg.SetLabel("")
                            self.txtGauge.SetLabel("")
                            j+=1
                        self.AffichTxt.Clear()
                        self.AffichTxt.SetForegroundColour(u"FOREST GREEN")
                        self.AffichTxt.AppendText(u"\n"+str(len(mem_pak))+l_maj_up[0]+u"\n")
                        for paks in mem_pak:
                            self.AffichTxt.AppendText(paks+u"\n")
                        self.AffichTxt.AppendText(u"\n"+l_all_up[0])
                        self.chck_maj.Disable()
                        self.start_g.Enable()
                        self.gauge.SetValue(0)
                        self.txtProg.SetLabel("")
                        self.txtGauge.SetLabel("")
                    else:
                        if lst_ver_diff!=[]:
                            x=0
                            while x<len(lst_ver_diff):
                                url_de_fichier_diff=url+lst_ver_diff[x]
                                nom_de_pak=url_de_fichier_diff.rsplit(u'/',1)[1]
                                try:
                                    rep = requests.get(url_de_fichier_diff, stream=True)
                                    no_net=0
                                except:
                                    self.no_internet()
                                total_size_diff = int(rep.headers.get(u'content-length', 0))
                                if total_size_diff>=(1024*1024):
                                    chunk_size=1024*1024
                                    n=round(total_size_diff/(1024*1024))
                                    u=u"MB"
                                elif total_size_diff>=(1024*1024*1024):
                                    chunk_size=1024*1024*1024
                                    n=round(total_size_diff/(1024*1024*1024))
                                    u=u"GB"
                                else:
                                    n=round(total_size_diff/1024)
                                    u=u"KB"
                                inc=0
                                self.gauge.SetRange(n)
                                if tab_line[4]!=u"none":
                                    self.txtProg.SetLabel(l_txtProg[0]+nom_de_pak)
                                    with open(getcwd()+u"\\"+tab_line[4].rstrip()+u"\\"+nom_de_pak,u"wb") as fichier_dl:
                                        for chunk in rep.iter_content(chunk_size=chunk_size):                                            
                                            fichier_dl.write(chunk)#DL
                                            inc+=1
                                            if inc>=n:
                                                self.txtGauge.SetLabel(str(n)+"/"+str(n)+u)
                                                self.gauge.SetValue(n)
                                            else:
                                                self.txtGauge.SetLabel(str(inc)+"/"+str(n)+u)
                                                self.gauge.SetValue(inc)
                                        mem_pak.append(u"-"+nom_de_pak)
                                else:
                                    self.txtProg.SetLabel(l_txtProg[0]+nom_de_pak)
                                    with open(nom_de_pak,u"wb") as fichier_dl:
                                        for chunk in rep.iter_content(chunk_size=chunk_size):
                                            fichier_dl.write(chunk)#DL
                                            inc+=1
                                            if inc>=n:
                                                self.txtGauge.SetLabel(str(n)+"/"+str(n)+u)
                                                self.gauge.SetValue(n)
                                            else:
                                                self.txtGauge.SetLabel(str(inc)+"/"+str(n)+u)
                                                self.gauge.SetValue(inc)
                                        mem_pak.append(u"-"+nom_de_pak)
                                self.txtProg.SetLabel("")
                                self.txtGauge.SetLabel("")
                                x+=1
                            self.AffichTxt.Clear()
                            self.AffichTxt.SetForegroundColour(u"FOREST GREEN")
                            self.AffichTxt.AppendText(u"\n"+str(len(mem_pak))+l_maj_up[0]+u"\n")
                            for paks in mem_pak:
                                self.AffichTxt.AppendText(paks+u"\n")
                            self.AffichTxt.AppendText(u"\n"+l_all_up[0])
                            self.chck_maj.Disable()
                            self.start_g.Enable()
                            self.gauge.SetValue(0)
                            self.txtProg.SetLabel("")
                            self.txtGauge.SetLabel("")
                        else:
                            self.AffichTxt.Clear()
                            self.AffichTxt.SetForegroundColour(u"RED")
                            self.AffichTxt.AppendText(l_err_ext[0])
                            for elem in liste_loc_ext:
                                self.AffichTxt.AppendText(u"-"+str(elem)+u"\n")
                            self.AffichTxt.AppendText(l_ici[0])
                            self.start_g.Disable()
                else:
                    alert=wx.MessageDialog(self,l_bad_file[0], l_404_file[0] ,wx.OK | wx.ICON_ERROR)
                    alert.ShowModal()
                    self.start_g.Disable()
        else:
            alert=wx.MessageDialog(self,l_bad_serv[0], l_404[0] ,wx.OK | wx.ICON_ERROR)
            alert.ShowModal()
            self.start_g.Disable()
    

    def on_close(self,evt):#On detruit tout :)
        self.Destroy()

class Panel(wx.Panel):
    def __init__(self, parent):
        #POS important pour l'affichage en 1280x800
        wx.Panel.__init__(self, parent, -1,pos=(140,140) ,size=(1000, 600,),style=wx.TRANSPARENT_WINDOW)
    
        

class GetData(wx.Dialog):
    def __init__(self, parent,title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size= (650,250))
        self.panel = wx.Panel(self,wx.ID_ANY)
        
        #file_config
        self.lbl_file_config = wx.StaticText(self.panel, label=l_file_config[0], pos=(20,20))
        self.file_config = wx.TextCtrl(self.panel, value=u"http://", pos=(180,20), size=(300,-1))
        self.file_config_txt = wx.StaticText(self.panel,label=l_file_config_txt[0],pos=(180,50))
        self.file_config_txt_vide = wx.StaticText(self.panel,label=u"",pos=(180,70))
        self.file_config_txt_vide.SetForegroundColour(u"BLUE")
        self.file_config_txt_vide.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.BOLD))
        self.file_config.Disable()
        #Checkbox and text Security anti trolls
        self.secu_txt = wx.StaticText(self.panel,label=l_secu_txt[0],pos=(10,100))
        self.secu_txt.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.BOLD))
        self.secu_txt.SetForegroundColour(u"RED")
        self.secu_box=wx.CheckBox(self.panel, label = l_check[0],pos = (290,160))
        self.Bind(wx.EVT_CHECKBOX,self.onChecked,self.secu_box)
        #Boutons
        self.saveButton =wx.Button(self.panel, wx.ID_OK, pos=(230,190))
        self.closeButton =wx.Button(self.panel, wx.ID_CANCEL, pos=(330,190))
        #Disable save button on init
        self.saveButton.Disable()
        #Btn Events
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        #Event Close
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def onChecked(self,evt):
        if self.secu_box.IsChecked(): 
            self.file_config.Enable()
            self.saveButton.Enable()
        else:
            self.file_config.Disable()
            self.saveButton.Disable()
            
    def SaveConnString(self,evt):
        self.file_config_val=self.file_config.GetValue()
        self.Destroy()
        evt.Skip()
        
    def OnQuit(self, evt):
        self.Destroy()

class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition,
             size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_TEXT, self.on_text_change)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()

    def on_text_change(self,event):
        self.Refresh()
        event.Skip()

class TransparentBox(wx.StaticBox):
  def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition,
             size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW , name='transparenttext'):
    wx.StaticBox.__init__(self, parent, id, label, pos, size, style, name)

    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
    self.Bind(wx.EVT_SIZE, self.on_size)

  def on_paint(self, event):
    bdc = wx.PaintDC(self)
    dc = wx.GCDC(bdc)

    font_face = wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "ARIAL BLACK" )
    font_color = "BLACK"

    dc.SetFont(font_face)
    dc.SetTextForeground(font_color)
    dc.DrawText(self.GetLabel(), 0, 0)

  def on_size(self, event):
    self.Refresh()
    event.Skip()
    
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, None)
        frame.Show(True)
        frame.Centre()
        return True
 
if __name__=='__main__':    
 
    app = MyApp(0)
    app.MainLoop()

#DEV By GARBEZ FRANCOIS(FAWN) 06/01/2020 (v3.1)
#DEV By GARBEZ FRANCOIS(FAWN) 20/12/2020 (v3.0)
#DEV By GARBEZ FRANCOIS(FAWN) 20/12/2020 (v2.1)
#DEV By GARBEZ FRANCOIS(FAWN) 01/02/2019 (v2.0)
#DEV By GARBEZ FRANCOIS(FAWN) 21/01/2019 (v1.0)
#DEV By GARBEZ FRANCOIS(FAWN) 30/12/2018 (v0.3a)
#DEV By GARBEZ FRANCOIS(FAWN) 29/12/2018 (v0.2a)
#DEV By GARBEZ FRANCOIS(FAWN) 13/12/2018 (v0.1a)

##
##                                                                              █████▒▄▄▄       █     █░███▄    █ 
##                                                                            ▓██   ▒▒████▄    ▓█░ █ ░█░██ ▀█   █ 
##                                                                            ▒████ ░▒██  ▀█▄  ▒█░ █ ░█▓██  ▀█ ██▒
##                                                                            ░▓█▒  ░░██▄▄▄▄██ ░█░ █ ░█▓██▒  ▐▌██▒
##                                                                            ░▒█░    ▓█   ▓██▒░░██▒██▓▒██░   ▓██░
##                                                                             ▒ ░    ▒▒   ▓▒█░░ ▓░▒ ▒ ░ ▒░   ▒ ▒ 
##                                                                             ░       ▒   ▒▒ ░  ▒ ░ ░ ░ ░░   ░ ▒░
##                                                                             ░ ░     ░   ▒     ░   ░    ░   ░ ░ 
##                                                                                         ░  ░    ░            ░ 
##                                                                                                               
