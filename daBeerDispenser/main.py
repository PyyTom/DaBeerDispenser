import datetime,sqlite3,sys
db=sqlite3.connect('Dispenser.db')
cdb=db.cursor()
cdb.execute('create table if not exists dispensers(id integer primary key autoincrement,name text,price float,flow_volume float,stock float)')
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
Builder.load_file('kvs/Dispenser.kv')
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.popup import Popup
class Dispenser(Screen):
    def tap_close(self,j,open_time):
        close_time =datetime.datetime.now()
        self.ids.close_time_label.text=str(close_time.strftime('%Y-%m-%d %H:%M:%S'))
        seconds = close_time - open_time
        if seconds.seconds>=22:
            pop_full=Popup(title='GLASS FULL',size_hint=(None,None),size=(1000,100))
            pop_full.open()
            litres=22*j[3]
            bill=j[2]*j[3]*22
            seconds=22
        else:
            litres=seconds.seconds*j[3]
            bill=j[2]*j[3]*seconds.seconds
        self.ids.bill_label.text=str(seconds)+' SECONDS\n'+str(litres)+' LITRES\n'+str(bill)+' $'
        cdb.execute('update dispensers set stock=stock-? where id=?',(litres,j[0],))
        db.commit()
    def tap_open(self,j):
        self.ids.open_time_label.text=''
        self.ids.close_time_label.text=''
        self.ids.bill_label.text=''
        open_time=datetime.datetime.now()
        self.ids.open_time_label.text=str(open_time.strftime('%Y-%m-%d %H:%M:%S'))
        self.ids.close.on_press=lambda: self.tap_close(j,open_time)
class Admin(Screen):
    def save(self,name,price,flow_volume,load):
        if cdb.execute('select * from dispensers where name=?',(name.text,)).fetchall()==[]:
            cdb.execute('insert into dispensers(name,price,flow_volume,stock) values(?,?,?,?)',(name.text,price.text,flow_volume.text,load.text,))
            db.commit()
        else:
            cdb.execute('update dispensers set price=?,flow_volume=?,stock=stock+? where name=?',(price.text,flow_volume.text,load.text,name.text))
            db.commit()
        pop_saved=Popup(title='SAVED',size_hint=(None,None),size=(1000,100))
        pop_saved.open()
        self.back()
    def back(self):
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'dispenser'
class app(MDApp):
    beers = cdb.execute('select * from dispensers').fetchall()
    def build(self):
        Window.maximize()
        sm=ScreenManager()
        sm.add_widget(Dispenser(name='dispenser'))
        sm.add_widget(Admin(name='admin'))
        return sm
    def tl(self):
        pop_tl=Popup(title='Tomas La torre - Valencia - 2023',size_hint=(None,None),size=(1000,100))
        pop_tl.open()
    def daBeerDispenser(self):
        pop_dbd=Popup(title='Beer tap dispenser',size_hint=(None,None),size=(1000,100))
        pop_dbd.open()
    def rviewer(self):
        pop_dbd=Popup(title='Rviewer - Barcelona',size_hint=(None,None),size=(1000,100))
        pop_dbd.open()
    def admin(self):
        MDApp.get_running_app().root.current='admin'
    def xit(self):
        db.close()
        sys.exit()
if __name__=='__main__':app().run()