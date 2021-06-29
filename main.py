from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime

from loandatabase import Database
database = Database()


Builder.load_file('design.kv')


class MainScreen(Screen):
    def goto_admin_page(self):
        self.manager.current = "adminfirst_screen"
    def goto_agent_page(self):
        self.manager.current = "agentfirst_screen"
    def goto_customer_page(self):
        self.manager.current = "customer_signin_screen"
#All Admin screen and works
class AdminScreenFirst(Screen):
    def go_to_adminsecond(self,uname,pword):
        with open("users.json") as file:
            users =json.load(file)
            if uname == users['admin']['username'] and users['admin']['password'] == pword:
                self.manager.current = "adminsecond_screen"
            else:
                self.ids.login_wrong.text = "Invalid Credentials.Please Contact the administrator"

class AdminScreenSecond(Screen):
    def go_to_adminpending(self):
        self.manager.current = "adminPending_screen"
    def go_to_adminapproved(self):
        self.manager.current = "approved_screen"
    def go_to_adminrejected(self):
        self.manager.current = "rejected_screen"

class AdminPendingScreen(Screen):
    def display(self):
        self.manager.current = "rv_screen"
#go on trying    
class RV(Screen):
    data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        for row in database.view():
            for col in row:
                self.data_items.append(col)
                #print(col)
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"

class APV(Screen):
    data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(APV, self).__init__(**kwargs)
        instr = "Approved"
        for row in database.viewrejec(instr):
            for col in row:
                self.data_items.append(col)
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"

class REV(Screen):
    data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(REV, self).__init__(**kwargs)
        instr = "Rejected"
        for row in database.viewrejec(instr):
            for col in row:
                self.data_items.append(col)
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"           


class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''
class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt
        inss = "Rejected"
        ccna = "Rahul"
        database.update(inss,ccna)
       
#end trying

#Agent Screen and Works
class AgentScreenFirst(Screen):
    def go_to_agentsecond(self,uname,pword):
        with open("agent.json") as file:
            users =json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.current = "agentsecond_screen"
            else:
                self.ids.login_wrong.text = "Invalid Credentials.Please Contact the administrator"
    def sign_up(self):
        self.manager.current = "agent_sign_up_screen"
    def forgot_password(self):
        self.manager.current = "agent_forgot_password_screen"

class AgentSignUpScreen(Screen):
    def add_user(self,uname,pword,bankid):
        with open("agent.json") as file:
            users = json.load(file)
        users[uname] = {'username' : uname , 'password' : pword, 'bankID' : bankid,
            'created_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open("agent.json" , 'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_successful_screen"

class AgtForgotPasswordScreen(Screen):
    def fetch_answer(self,uname,bankid):
        try:
            with open("agent.json") as file:
                users =json.load(file)
                if uname in users and users[uname]['bankID'] == bankid:
                    answr = users[uname]['password']
                    self.ids.answer.text = answr
                else:
                    self.ids.answer.text = "Please type the Username or BankID Correctly"
        except KeyError:
            pass
    def go_to_loginpage(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "agentfirst_screen"

class AgentScreenSecond(Screen):
    def go_to_agentviewloans(self):
        self.manager.current = "viewall_loans"
    def go_to_agentaddloan(self):
        self.manager.current = "agentadd_loan"

class VV(Screen):
    data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(VV, self).__init__(**kwargs)
        #self.data = [{'text': str(v)} for v in range(50)]
        #self.get_users()
        for row in database.view():
            for col in row:
                self.data_items.append(col)
                #print(col)
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"   

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, vv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            vv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, vv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        
class AgentAddScreen(Screen):
    def go_to_interestrate(self,ltype,itype):
        ltype = ltype.lower()
        itype = itype.lower()
        if itype == "fixed":
            if ltype == "property":
                self.ids.interestrate.text = "9.00% p.a. - 9.10% p.a"
            elif ltype == "education":
                self.ids.interestrate.text = "7.97% p.a. - 10.05% p.a." 
            elif ltype == "personal":
                self.ids.interestrate.text = "9.20% p.a. to 13.65% p.a."
            elif ltype == "business":
                self.ids.interestrate.text = "10.70% p.a. to 14.00% p.a."
            else:
                self.ids.interestrate.text = "Invalid.Please type from the options"
        elif itype == "variable":
            self.ids.interestrate.text = "Depends on the Market Rate"
        else:
            self.ids.interestrate.text = "Invalid Entry"
    def go_to_confirm(self,customer,blance,ltype,itype,tenure,security):
        with open("loandata.json") as file:
            users = json.load(file)
        users[customer] = {'CustomerName' : customer , 'Balance' : blance, 'LoanType' : ltype,
            'InterestType' : itype,'Tenure' : tenure,'Security' : security}
        with open("loandata.json" , 'w') as file:
            json.dump(users,file)
        #print(users)
        self.manager.current = "agent_add_successfull_screen"
    
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"

class AgentAddSuccessful(Screen):
    def go_to_fetchdata(self,cname):
        try:
            with open("loandata.json") as file:
                users =json.load(file)
                if cname in users :
                    tenure = users[cname]['Tenure']
                    self.ids.tenure.text = f"Tenure : {tenure} Years"
                    balance = users[cname]['Balance']
                    self.ids.balance.text = f"Balance : {balance} Rupees"
                    itype = users[cname]['InterestType']
                    self.ids.itype.text = f"Interest Type : {itype}"
                    ltype = users[cname]['LoanType']
                    self.ids.ltype.text = f"Loan Type : {ltype}"
                    security = users[cname]['Security']
                    self.ids.security.text = f"Security : {security}"
                    if itype == "fixed":
                        if ltype == "property":
                            inter = 9.00
                            self.ids.interest.text = "Interest Rate : 9.00% p.a."
                            nr = int(tenure) * 12
                            emi = (int(balance) * 0.0075 * pow(1.0075,nr) ) / (pow(1.0075,nr) - 1)
                            emi = round(emi,2)
                            self.ids.moninst.text = f"Monthly Instalment : {str(emi)} Rupees"
                            totall = emi * nr
                            totall = round(totall,2)
                            self.ids.tpay.text = f"Total Loan Payment : {str(totall)} Rupees "
                        elif ltype == "education":
                            inter = 9.01
                            self.ids.interest.text = "Interest Rate : 9.01% p.a." 
                            nr = int(tenure) * 12
                            emi = (int(balance) * 0.0075 * pow(1.0075,nr) ) / (pow(1.0075,nr) - 1)
                            emi = round(emi,2)
                            self.ids.moninst.text = f"Monthly Instalment : {str(emi)} Rupees"
                            totall = emi * nr
                            totall = round(totall,2)
                            self.ids.tpay.text = f"Total Loan Payment : {str(totall)} Rupees "
                        elif ltype == "personal":
                            inter = 11.425
                            self.ids.interest.text = "Interest Rate : 11.425% p.a."
                            nr = int(tenure) * 12
                            emi = (int(balance) * 0.00952 * pow(1.00952,nr) ) / (pow(1.00952,nr) - 1)
                            emi = round(emi,2)
                            self.ids.moninst.text = f"Monthly Instalment : {str(emi)} Rupees"
                            totall = emi * nr
                            totall = round(totall,2)
                            self.ids.tpay.text = f"Total Loan Payment : {str(totall)} Rupees "
                        elif ltype == "business":
                            inter = 12.35
                            self.ids.interest.text = "Interest Rate : 12.35% p.a."
                            nr = int(tenure) * 12
                            emi = (int(balance) * 0.01029 * pow(1.01029,nr) ) / (pow(1.01029,nr) - 1)
                            emi = round(emi,2)
                            self.ids.moninst.text = f"Monthly Instalment : {str(emi)} Rupees"
                            totall = emi * nr
                            totall = round(totall,2)
                            self.ids.tpay.text = f"Total Loan Payment : {str(totall)} Rupees "
                    elif itype == "variable":
                        self.ids.interest.text = "Interest Rate : Dependent on Market"
                        inter = 10.00
                        nr = int(tenure) * 12
                        emi = (int(balance) * 0.00833 * pow(1.00833,nr) ) / (pow(1.00833,nr) - 1)
                        emi = round(emi,2)
                        self.ids.moninst.text = f"Monthly Instalment : {str(emi)} Rupees"
                        totall = emi * nr
                        totall = round(totall,2)
                        self.ids.tpay.text = f"Total Loan Payment : {str(totall)} Rupees "
                    instruc = "Waiting"
                    database.insert(cname,tenure,balance,ltype,itype,inter,security,totall,emi,instruc)
                else:
                    self.ids.tenure.text = "Please type the Customer Name Correctly"
                
        except KeyError:
            pass
    def go_to_applysuccessfull(self):
        self.manager.current = "agent_apply_successful_screen"

class AgentApplySuccesful(Screen):
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"

#Customer Screen and Works 

class CustomerSignInScreen(Screen):
    def go_to_customerecord(self,uname,pword):
        with open("customer.json") as file:
            users =json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.current = "customer_autheticate_screen"
            else:
                self.ids.login_wrong.text = "Invalid Credentials.Please Contact the administrator"
    def sign_up(self):
        self.manager.current = "customer_sign_up_screen"
    def forgot_password(self):
        self.manager.current = "customer_forgot_password_screen"

class CustomerAuthDisplay(Screen):
    def go_to_authenticate(self,cname):
        with open("loandata.json") as file:
            users =json.load(file)
            if cname in users :
                self.manager.current = "cv_screen"
            else:
                self.ids.gettt.text = "Invalid Customer Name"

class CustomerSignUpScreen(Screen):
    def add_user(self,uname,pword,qstn):
        with open("customer.json") as file:
            users = json.load(file)
        users[uname] = {'username' : uname , 'password' : pword, 'question' : qstn,
            'created_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open("customer.json" , 'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_successful_screen"

class SignUpSuccessfulScreen(Screen):
    def go_to_login_page(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"

class CusForgotPasswordScreen(Screen):
    def fetch_answer(self,uname,qstn):
        try:
            with open("customer.json") as file:
                users =json.load(file)
                if uname in users and users[uname]['question'] == qstn:
                    answr = users[uname]['password']
                    self.ids.answer.text = answr
                else:
                    self.ids.answer.text = "Please type the Username or Question's Answer Correctly"
        except KeyError:
            pass
    def go_to_loginpage(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "customer_signin_screen"
#Customerviewloan Screen

class CV(Screen):
    data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(CV, self).__init__(**kwargs)
        name = "krrr"
        for row in database.viewspecific(name):
            for col in row:
                self.data_items.append(col)
    
    def logout_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "mainfirst_screen"
#Customer Screen and Works ends 

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()

#to see json file press shift alt f