#!/usr/bin/env python
#-*- coding:UTF-8 -*-#
import gobject
import gtk
import appindicator
import atindicator
import thread
import time

import gettext 
PACKAGE = 'indicator-antithief'
gettext.bindtextdomain(PACKAGE,'/usr/share/locale')
gettext.textdomain(PACKAGE)
_ = gettext.gettext


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
    about.set_comments("Antithieft enjoy it ^_^")
    about.set_website("https://github.com/frankyue/indicator-antithief")
    #about.set_logo(gtk.gdk.pixbuf_new_from_file("battery.png"))
    about.run()
    about.destroy()

def help_dialog(w):
    dialog = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE
                               ,_('Please read the wiki')+"\nhttps://github.com/frankyue/indicator-antithief/wiki/Usage")
    dialog.run()
    dialog.destroy()

def setting_dialog(w):
    dialog = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,
                               _("config in path")+"\"/etc/antithief.conf\"")
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
  menu_items = gtk.MenuItem(_('start'))
  menu.append(menu_items)
  menu_items.connect("activate",alarmcmd,"start")
  menu_items.show()


  # menu item 2
  menu_items = gtk.MenuItem(_('stop'))
  menu.append(menu_items)
  menu_items.connect("activate",alarmcmd,"stop")
  menu_items.show()
  ind.set_menu(menu)


  # separator
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()

  # menu item 3
  menu_items = gtk.MenuItem(_('setting'))
  menu.append(menu_items)
  menu_items.connect("activate",setting_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # menu item 4
  menu_items = gtk.MenuItem(_('about'))
  menu.append(menu_items)
  menu_items.connect("activate",about_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # menu item 4
  menu_items = gtk.MenuItem(_('help'))
  menu.append(menu_items)
  menu_items.connect("activate",help_dialog)
  menu_items.show()
  ind.set_menu(menu)

  # separator
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()

  # menu item 5
  menu_items = gtk.MenuItem(_('Quit'))
  menu.append(menu_items)
  menu_items.connect("activate",ui_quit)
  menu_items.show()
  ind.set_menu(menu)

  gtk.main()
