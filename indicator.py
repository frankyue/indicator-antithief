#!/usr/bin/env python
#-*- coding:UTF-8 -*-#
import gobject
import gtk
import appindicator
import atindicator
import thread
import time


anti = atindicator.Antithief()

def alarmcmd(w,cmd):
    anti.alarmcmd(cmd)                   

def ui_quit(self):
    thread.start_new_thread(anti.alarmcmd,('stop',))
    time.sleep(2)
    gtk.main_quit()

def about_dialog(w):
    about = gtk.AboutDialog()
    about.set_program_name("Antithief")
    about.set_version("0.1")
    about.set_copyright("2011-2012(c) fraknyue <frankyue1019@gmail.com>")
    about.set_comments("Read the help comments")
    about.set_website("github://")
    #about.set_logo(gtk.gdk.pixbuf_new_from_file("battery.png"))
    about.run()
    about.destroy()

def help_dialog(w):
    dialog = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE
                               ,"""\n使用方法及注意事项:
    1.保证电源线连接电脑
    2.点击start(5秒后自动锁屏)
    3.当电源线拔出或者合上电脑时，电脑自动报警
                    (可选 拍照并上传,发短信提醒)
    4.只有重新接上电源后,电脑停止报警
    5.请尽量先停止软件，然后退出""")
    dialog.run()
    dialog.destroy()

def setting_dialog(w):
    dialog = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,
                               "config in path \"/usr/share/antithief/Antithief.cfg\"")
    dialog.run()
    dialog.destroy()


if __name__ == "__main__":
  ind = appindicator.Indicator ("Antithief-client",
                              "indicator-antithief",
                              appindicator.CATEGORY_OTHER)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("indicator-antithief")

  # create a menu
  menu = gtk.Menu()

  # create some 
  # menu item 1
  buf = "Start"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",alarmcmd,"start")
  menu_items.show()


  # menu item 2
  buf = "Stop"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",alarmcmd,"stop")
  menu_items.show()
  ind.set_menu(menu)


  # separator
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()

  # menu item 3
  buf = "Setting"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",setting_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # menu item 4
  buf = "About"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",about_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # menu item 4
  buf = "Help"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",help_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # separator
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()

  # menu item 5
  buf = "Quit"
  menu_items = gtk.MenuItem(buf)
  menu.append(menu_items)
  menu_items.connect("activate",ui_quit)
  menu_items.show()
  ind.set_menu(menu)

  gtk.main()
