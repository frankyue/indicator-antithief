#!/usr/bin/env python
#-*- coding:UTF-8 -*-#
#Auto-control the Banshee (pasue & play) when the computer
#get on charge or off


#1.depend list
#dbus 
#opencv
#gconf
#command play
#2.optional  depend
#cli-feition


import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

gobject.threads_init()
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
dbus.mainloop.glib.threads_init()

import os
import wave
import thread 
import time

from multiprocessing import Process
from subprocess import call

import gettext 
PACKAGE = 'indicator-antithief'
gettext.bindtextdomain(PACKAGE,'/usr/share/locale')
gettext.textdomain(PACKAGE)
_ = gettext.gettext


#optionalarm template
#paras[0] : optional file path
#def alarm_name(threadname,paras)

#capture the picture and upload to website
#paras[0] : optional file path
#paras[1] : Droppath
#paras[2] : photo num
def capture(threadname,paras):
    import cv
    imgname = paras[1]+'Dropbox/thief-'+str(paras[2])+'.jpg'
    cv.NamedWindow("camera", 1)
    capture = cv.CaptureFromCAM(0)
    img = cv.QueryFrame(capture)
    cv.SaveImage(imgname,img) 

    #then upload the pic
    #but, here upload to the dropbox

#Send message to alarm you
#paras[0] : optional file path
def sendmessage(threadname,paras):
    #    call('./sendmessage.sh',shell=True)
    call(paras[0]+'sendmessage.sh',shell=True)


class Antithief:
    def __init__(self):
        self.Running = 0
        self.lidstate = "suspend"
        self.volume = 30
        self.wavpath = ""
        self.opon = 0

        #optiona alarm parameters
        self.oppath = ""
        self.droppath = ""
        self.num = 0

        self.readconfig()

    def readconfig(self):
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read('/etc/antithief.conf')
        self.wavpath = config.get('setting','sound')
        self.opon = config.getint('setting','opon')
        self.oppath = config.get('setting','oppath')

        self.droppath = config.get('optional','dropboxpath')

    def alarmcmd(self,buf):
        if buf == "start":
            print "start"
            self.alarmstart()
        elif buf == "stop":
            print "stop"
            self.alarmstop()

    def alarmstop(self):
        self.Running = 0
        self.restore()

    def alarmstart(self):
        self.Running = 1
        self.setstatus(1)
        self.loudest(1)
        self.signal_wait()
        thread.start_new_thread(self.lockscreen,(None,))


    def alarm(self):
        #1.The basic alarm activities
        #self.playsound()
        thread.start_new_thread(self.playsound,(None,))
        
        #2.Optional alarm activities
        if self.opon == 1:
            thread.start_new_thread(self.optionalarm,(None,))

    #Before Play the sound
    #Make sure the sound volume is the loudest
    #toway 1:set loudest
    #      0:restore the volume
    def loudest(self,toway):
        sebus = dbus.SessionBus()
        od = sebus.get_object('org.ayatana.indicator.sound','/org/ayatana/indicator/sound/service')
        if toway == 1:
            self.volume = od.GetSinkVolume()
            od.SetSinkVolume(dbus.UInt32(100))
        else:
            od.SetSinkVolume(dbus.UInt32(self.volume))
    

    def Battery(self):
        sybus = dbus.SystemBus()
        check = sybus.get_object('org.freedesktop.UPower','/org/freedesktop/UPower')
        statue = dbus.Interface(check,'org.freedesktop.DBus.Properties')
        return statue.Get("org.freedesktop.UPower","OnBattery")


    #Just to play the alarm sound
    def playsound(self,threadname):
        playcmd = "play "+self.wavpath
        if self.Running == 1:
            while self.Battery() == 1:
                call(playcmd,shell=True)

    #Just to play the alarm sound
    #use pygame
#    def playsound(self,threadname,wavpath):
#        import pygame
#        pygame.init()
#        sound = pygame.mixer.Sound(wavpath)
#        if self.Running == 1:
#            while self.Battery() == 1:
#                sound.play()

    #Set the status while in Battery using
    #Make sure it still work when computer is closed
    #toway :1 set to blank 
    #       0 restore set
    def setstatus(self,toway):
        import gconf
        gvalue = gconf.Value(gconf.VALUE_STRING)
        gclient = gconf.client_get_default()
        gvalue = gclient.get('/apps/gnome-power-manager/buttons/lid_battery')
        if toway == 1:
            self.lidstate = gvalue.to_string()
            gvalue.set_string('blank')
            gclient.set('/apps/gnome-power-manager/buttons/lid_battery',gvalue)
        else:
            gvalue.set_string(self.lidstate)
            gclient.set('/apps/gnome-power-manager/buttons/lid_battery',gvalue)


    #After received the signal,Do what?
    #1.send a message to my phone
    #2.Play a sound to alarm the thief
    def signal_callback(self):
        print "catch the signal"
        if self.Running == 1:
            self.alarm()

    def lockscreen(self,threadname):
        #Notify
        import time
        nobus = dbus.SessionBus()
        noobj = nobus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
        notify = dbus.Interface(noobj,'org.freedesktop.Notifications')
        #ntc
        notify.Notify('Anti-thief',1,'',_("Attention"),
                      #'\t1.为得到清晰图片保证摄像头在明亮处-Keep webcam under the light to get a clear photo\n\t2.拔出耳机-Pull out the earphone\n\t3.电脑在5秒内锁屏-Screen will be lock in 5s'
                      _("1.Keep webcam under the light to get a clear photo")+"\n"+
                      _("2.Pull out the earphone")+"\n"+
                      _("3.Screen will be lock in 5s")
                      ,'','',20000)
        time.sleep(5)
        lockbus = dbus.SessionBus()
        locksc = lockbus.get_object('org.gnome.ScreenSaver','/')
        locksc.Lock()

    def signal_wait(self):
        sybus = dbus.SystemBus()
        sybus.add_signal_receiver(self.signal_callback,signal_name="Changed",dbus_interface="org.freedesktop.UPower")
    
    #restore the state before the alarm startup
    def restore(self):
        thread.start_new_thread(self.setstatus,(0,))
        thread.start_new_thread(self.loudest,(0,))

    #Write more ways of alarm activities
    #use thread
    #add your own ways to alarm yourself
    def optionalarm(self,threadname):
        print 'optionalarm'
        self.num = self.num + 1
        thread.start_new_thread(capture,("Capture",[self.oppath,self.droppath,self.num]))
        thread.start_new_thread(sendmessage,("Sendmessage",[self.oppath]))
