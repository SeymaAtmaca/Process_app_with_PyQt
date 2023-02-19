from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QPixmap,QColor,QPalette
from pymongo import MongoClient
import pandas as pd
from datetime import *

project_val = {
    'project_name': '',
    'project_code': '0000',
    'start_time': '00.00.0000',
    'end_time': '00.00.0000',
    'personInCharge': 'Non',
    'calisanId': [],
    'ana_baslik': [],
    'project_info' : ''
}


process_val = {
    'project_name': 'project',
    'project_code': '0000',
    'start_time': '00.00.0000',
    'end_time': '00.00.0000',
    'person': 'Non',
    'main_title': []
}

mains = []



class App(QDialog):
    def __init__(self, parent=None):

        self.lorem = "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem I\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,\n Lorem Ipsum wegwehas been the industry's standard dummy text ever since the 1500s,psum wegwehas been the industry's standard dummy text ever since the 1500s, \nwhen an unknown prinwegawgeter took a galley of type and scrambled it to make \n a type specimen book. It has survived not only five centuries, but also the leap into \n electronic typesetting, remaining essentially unchanged. It was \n popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,\n  and more recently with desktop publishing software like Aldus \n PageMaker including versions of \n Lorem Ipsum.Why do we use it?It is a long established fact that a reader will be \n distracted by the readable content of a page when looking at its layout. \n The point of using Lorem Ipsum is that it has a more-or-less normal \n distribution of letters, as opposed to using 'Content here,\n content here', making it look like readable English. Many desktop\n publishing packages and web page editors now use Lorem Ipsum as \n their default model text, and a search for 'lorem ipsum' will uncover many\n  web sites still in their infancy. Various versions have evolved over \n the years, sometimes by accident, sometimes on purpose (injected humour and the like).Where does it come from?Contrary to popular belief, \n Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin \n literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at \n Hampden-Sydney College in Virginia, looked up one of the\n  more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical\n  literature, discovered the undoubtable source. Lorem Ipsum comes from sections \n 1.10.32 and 1.10.33 of de Finibus Bonorum et Malorum (The Extremes of Good and Evil) by Cicero, written\n  in 45 BC. This book is a treatise on the theory of ethics, \n very popular during the Renaissance. The first line of Lorem Ipsum,\n  Lorem ipsum dolor sit amet.., comes from a line in section 1.10.32."

        super(App, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.members = []
        self.flag_project = 0
        self.column_val = 0

        self.connect_db()
        self.resize(450, 70)
        self.styleComBox = QComboBox()
        self.styleComBox.addItems(QStyleFactory.keys())
        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.topGroupBox = QGroupBox("Top Group")

        self.create_Project_TopGroupBox()
        self.create_Project_BottomGroupBox()

        disableWidgetsCheckBox.toggled.connect(
            self.ProjetTopGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.ProjetBottomGroupBox.setDisabled)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.ProjetTopGroupBox, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.ProjetBottomGroupBox, 1, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 0)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("Table GUI")

    def create_Project_TopGroupBox(self):
        self.ProjetTopGroupBox = QGroupBox("Project Name")

        self.projectlayout = QHBoxLayout()
        self.cb = QComboBox()
        self.prjnameselect = QLabel('Project: ')
        self.projectlayout.addWidget(self.prjnameselect)
        self.extract_projects()
        self.projectlayout.addWidget(self.cb)
        self.prjcalendar = QPushButton('Calendar')
        self.projectlayout.addWidget(self.prjcalendar)
        self.prjdelete = QPushButton('Delete Project')
        self.projectlayout.addWidget(self.prjdelete)
        self.prjprocess = QPushButton('Add Process')
        self.projectlayout.addWidget(self.prjprocess)

        self.ProjetTopGroupBox.setLayout(self.projectlayout)

    def create_Project_BottomGroupBox(self):
        self.ProjetBottomGroupBox = QGroupBox("bottom group")
        self.new_btn_layout = QVBoxLayout()

        self.prjbtn = QPushButton('New')
        self.prjbtn.setCheckable(True)

        self.new_btn_layout.addWidget(self.prjbtn)
        self.prjbtn.clicked.connect(self.NewProject)
        self.prjdelete.clicked.connect(self.deleteProject)
        self.prjprocess.clicked.connect(self.add_process_exist_project)

        self.ProjetBottomGroupBox.setLayout(self.new_btn_layout)

    def deleteProject(self):
        self.records.delete_one({"project_name": self.cb.currentText()})
        self.cb.clear()
        self.extract_projects()
# _____________________________  project page _______________________________________

    def extract_projects(self):
        self.projects = self.records.find()
        for i in self.projects:
            self.cb.addItem(i['project_name'])
    def add_process_exist_project(self):
        self.ProjetTopGroupBox.deleteLater()
        self.ProjetBottomGroupBox.deleteLater()
        self.add_process_to_Project()
        self.resize(500, 350)
        disableWidgetsCheckBoxNew = QCheckBox("&Disable widgets")
        disableWidgetsCheckBoxNew.toggled.connect(
            self.addprocessGroupBox.setDisabled)
        self.mainLayout.addWidget(self.addprocessGroupBox, 0, 0)
        self.setWindowTitle("Members")

    def add_process_to_Project(self):
        self.choosenProject = self.cb.currentText()
        print(self.choosenProject)
        self.addprocessGroupBox = QGroupBox()
        self.addprocessLayout = QGridLayout()

        self.addprocessStartAt = QLabel("Start at ( T0 + ): ")
        self.addprocessFinishAt = QLabel("Finish at ( T0 + ): ")
        self.addprocessPersonInCharge = QLabel("Person: ")
        self.addprocessInfo = QLabel("Information: ")
        self.addprocessMainTitle = QLabel("Main Title: ")
        self.addprocessSubTitle = QLabel("Sub Title: ")

        self.subTitleList = QComboBox()
        self.mainTitleList = QComboBox()
        self.showMainTitle()
        
        self.mainTitleList.currentIndexChanged.connect(self.showsubTitle)
        self.addprocessLayout.addWidget(self.mainTitleList, 5, 2)
        self.addprocessLayout.addWidget(self.subTitleList, 5, 4)

        self.addprocessMainTitleBtn = QPushButton('Add Main Title')
        self.addprocessLayout.addWidget(self.addprocessMainTitleBtn, 7, 2)
        self.addprocessSubTitleBtn = QPushButton('Add Sub Title')
        self.addprocessLayout.addWidget(self.addprocessSubTitleBtn, 7, 3)

        self.deleteMainTitleBtn = QPushButton('Delete Main Title')
        self.addprocessLayout.addWidget(self.deleteMainTitleBtn, 8, 2)
        self.deleteSubTitleBtn = QPushButton('Delete Sub Title')
        self.addprocessLayout.addWidget(self.deleteSubTitleBtn, 8, 3)



        self.addprocessLayout.addWidget(self.addprocessStartAt, 1, 0, 1, 2)
        self.addprocessLayout.addWidget(self.addprocessFinishAt, 2, 0, 1, 2)
        self.addprocessLayout.addWidget(self.addprocessInfo, 4, 0, 1, 2)
        self.addprocessLayout.addWidget(self.addprocessPersonInCharge, 3, 0, 1, 2)
        self.addprocessLayout.addWidget(self.addprocessMainTitle, 5, 0)
        self.addprocessLayout.addWidget(self.addprocessSubTitle, 5, 3)

        self.addprocessStartAt_val = QLineEdit()
        self.addprocessFinishAt_val = QLineEdit()
        self.addprocessMainTitle_val = QLineEdit()
        self.addprocessSubTitle_val = QLineEdit()
        self.addprocessPersonInCharge_val = QLineEdit()
        self.addprocessInfo_val = QTextEdit()

        self.addprocessLayout.addWidget(self.addprocessStartAt_val, 1, 2, 1, 4)
        self.addprocessLayout.addWidget(self.addprocessFinishAt_val, 2, 2, 1, 4) 


        self.addprocessLayout.addWidget(self.addprocessMainTitle_val, 6, 2)
        self.addprocessLayout.addWidget(self.addprocessSubTitle_val, 6, 4)
        self.addprocessLayout.addWidget(self.addprocessPersonInCharge_val, 3, 2, 1, 4)
        self.addprocessLayout.addWidget(self.addprocessInfo_val, 4, 2, 1, 4)

        self.procesCreat = QPushButton('Create')
        self.addprocessLayout.addWidget(self.procesCreat, 7, 4)

        self.procesCreat.clicked.connect(self.create_table)
        self.addprocessSubTitleBtn.clicked.connect(self.addSubToMain)
        self.addprocessMainTitleBtn.clicked.connect(self.addNewMainTitle)

        self.deleteMainTitleBtn.clicked.connect(self.deleteMainTitleFunc)
        #self.deleteSubTitleBtn.clicked.connect(self.deleteSubTitleFunc)
        self.addprocessGroupBox.setLayout(self.addprocessLayout)

    def showsubTitle(self):
        self.subTitle = self.mainTitle_records.find({'main':self.mainTitleList.currentText()})
        self.subTitleList.clear()
        for i in self.subTitle:
            self.arr = i['sub_titles'] 
            for j in range(len(self.arr)) :
                print(self.arr)
                self.subTitleList.addItem(str(self.arr[j]))


    def deleteMainTitleFunc(self):
        self.getMains = self.mainTitle_records.find({'main':self.mainTitleList.currentText()}) 
        # self.mainTitle_records.delete_one({'main':self.mainTitleList.currentText()})
        # self.showMainTitle()
        

        arr = []
        tut = 0
        for i in self.getMains:
            print("ilk main : ")
            print(i['main'])
            tut = i['main']
            self.mainTitle_records.delete_one({'main':i['main']})
            print("son main: ")
            print(i['main'])
            
        for i in self.records.find({'project_name':self.choosenProject}):
            
            arr = list(i['ana_baslik'])
            print("ilk arr : ")
            print(arr)
            print("tut: ")
            print(tut )
            arr.remove(tut)
            print(arr)

            self.records.update_one(i,{"$set":{"ana_baslik":arr}})
        self.mainTitleList.clear()
        self.showMainTitle()

    def addSubToMain(self):
        if self.addprocessSubTitle_val.text() != "" :
            self.addMainId = self.mainTitle_records.find({'main':self.mainTitleList.currentText()}) 
            self.arr = []
            for i in self.addMainId:
                self.arr = i['sub_titles'] 

            self.arr.append(self.addprocessSubTitle_val.text())
            self.mainTitle_records.update_one({'main':self.mainTitleList.currentText()}, {"$set":{"sub_titles":self.arr}}) 
            self.addprocessSubTitle_val.setText("")
            self.subTitleList.clear()
            self.subTitleList.addItems(self.arr)

   
    def addNewMainTitle(self):

        self.mainTitle_val = {
            'main': '',
            'sub_titles': [],
        }
        #add new main title function
        if self.addprocessMainTitle_val.text() != "":
            self.choosenMain = self.records.find({'project_name':self.choosenProject})
            self.mainTitle_val['main'] = self.addprocessMainTitle_val.text()
            mains.append(self.addprocessMainTitle_val.text())
            print(mains)

            try: 
                if self.get_mainTitles() == 1 :
                    self.mainTitle_records.insert_one(self.mainTitle_val)
                    self.records.update_many({'project_name':self.choosenProject}, 
                                                {'$push':{'ana_baslik':self.addprocessMainTitle_val.text()}})

                    self.mainTitleList.addItem(self.addprocessMainTitle_val.text())
                    print("array deger : " + str(self.mainArray))
                    print("en son deger: " + str(self.addprocessMainTitle_val.text()))
                    self.addprocessMainTitle_val.clear()
                else:
                    print("eklenemez")
            except Exception as e:
                print(e)
                print("Bu daha önce eklenmiş")

    def get_mainTitles(self):
        
        self.mainArray = []
        for i in self.choosenMain:
            self.mainArray.append(i['ana_baslik'])  #mainArray, seçili projenin bütün mainlerini tutuyor.
            
        if self.addprocessMainTitle_val.text() not in str(self.mainArray):
            print("eklenmek istenen değer: " + self.addprocessMainTitle_val.text()) 
            return 1
        else:
            return 0
            

    def showMainTitle(self):
        
        if self.flag_project == 0:
            self.mainTitles =self.mainTitle_records.find()

            self.choosenMain = self.records.find({'project_name':self.choosenProject})  # seçilen proje database den çekilir
            for i in self.choosenMain:
                self.dene = i['ana_baslik'] 

            for i in range(len(self.dene)):
                self.mainTitleList.addItem(self.dene[i])

            self.subTitle = self.mainTitle_records.find({'main':self.mainTitleList.currentText()})
            for i in self.subTitle:
                self.arr = i['sub_titles'] 
                for j in range(len(self.arr)) :
                        self.subTitleList.addItem(str(self.arr[j]))
        elif self.flag_project == 1:
            for i in range(len(mains)):
                self.mainTitleList.addItem(mains[i])
            self.subTitle = self.mainTitle_records.find({'main':self.mainTitleList.currentText()})
            for i in self.subTitle:
                self.arr3 = i['sub_titles'] 
                for j in range(len(self.arr3)) :
                        self.subTitleList.addItem(str(self.arr3[j]))
        
        

    def NewProject(self):
        # eski sayfanın silindiği kısım
        self.choosenProject = self.cb.currentText()
        self.ProjetBottomGroupBox.deleteLater()
        self.ProjetTopGroupBox.deleteLater()
        self.show()
        self.flag_project = 1

        self.resize(500, 200)
        disableWidgetsCheckBoxNew = QCheckBox("&Disable widgets")
        self.create_NewProject_BottomGroupBox()
        disableWidgetsCheckBoxNew.toggled.connect(self.NewProjetBottomGroupBox.setDisabled)

        self.mainLayout.addWidget(self.NewProjetBottomGroupBox, 1, 0)
        self.setWindowTitle("New Page")


    def create_NewProject_BottomGroupBox(self):
        self.NewProjetBottomGroupBox = QGroupBox("Project ")
        self.createNewProjectLayout = QGridLayout()

        self.newProjectName = QLabel("Project Name: ")
        self.newProjectCode = QLabel("Project Code: ")
        self.newT0 = QLabel("T0: ")
        self.lastTime = QLabel("Last Time: ")
        self.newProjectInfo = QLabel("Information: ")

        self.createNewProjectLayout.addWidget(self.newProjectName)
        self.createNewProjectLayout.addWidget(self.newProjectCode)
        self.createNewProjectLayout.addWidget(self.newT0)
        self.createNewProjectLayout.addWidget(self.lastTime)
        self.createNewProjectLayout.addWidget(self.newProjectInfo)

        # ____ set status val label ____________

        self.newProjectName_val = QLineEdit()
        self.newProjectCode_val = QLineEdit()
        self.newT0_val = QLineEdit()
        self.lastTime_val = QLineEdit()
        self.newProjectInfo_val = QTextEdit()

        self.createNewProjectLayout.addWidget(self.newProjectName_val, 0, 1)
        self.createNewProjectLayout.addWidget(self.newProjectCode_val, 1, 1)
        self.createNewProjectLayout.addWidget(self.newT0_val, 2, 1)
        self.createNewProjectLayout.addWidget(self.lastTime_val, 3, 1)
        self.createNewProjectLayout.addWidget(self.newProjectInfo_val, 4, 1)

        self.newPrjNextBtn = QPushButton('Next', self)

        self.newPrjNextBtn.clicked.connect(self.NewProjectmembers)
        self.createNewProjectLayout.addWidget(self.newPrjNextBtn, 5, 1)

        self.newProjectName_val.setText("")
        self.newT0_val.setText("")
        self.lastTime_val.setText("")

        self.NewProjetBottomGroupBox.setLayout(self.createNewProjectLayout)

    def NewProjectmembers(self):
        project_val["project_name"] = self.newProjectName_val.text()
        project_val["project_code"] = self.newProjectCode_val.text()
        project_val["start_time"] = self.newT0_val.text() # datetime.strptime(self.newT0_val.text(),'%d.%m.%Y').date()
        project_val["end_time"] = self.lastTime_val.text() #datetime.strptime(self.lastTime_val.text(),"%d.%m.%Y").date()
        project_val["project_info"] = self.newProjectInfo_val.toPlainText()


        #self.NewProjetTopGroupBox.deleteLater()
        self.NewProjetBottomGroupBox.deleteLater()
        self.show()

        self.resize(450, 250)
        disableWidgetsCheckBoxNew = QCheckBox("&Disable widgets")
        self.create_NewProjectmembers()
        disableWidgetsCheckBoxNew.toggled.connect(
            self.NewProjetmemberGroupBox.setDisabled)

        self.mainLayout.addWidget(self.NewProjetmemberGroupBox, 0, 0)
        self.setWindowTitle("Members")

    def create_NewProjectmembers(self):
        self.NewProjetmemberGroupBox = QGroupBox("Project Members")
        self.newmemberLayout = QGridLayout()

        self.ProjectmemberName = QLabel("Name: ")
        self.ProjectmemberSurname = QLabel("Surname: ")
        self.ProjectMemberTask = QLabel("Task: ")
        self.newmemberLayout.addWidget(self.ProjectmemberName)
        self.newmemberLayout.addWidget(self.ProjectmemberSurname)
        self.newmemberLayout.addWidget(self.ProjectMemberTask)

        # ____ set status val label ____________

        self.ProjectmemberName_val = QLineEdit()
        self.ProjectmemberSurname_val = QLineEdit()
        self.ProjectMemberTask_val = QLineEdit()

        self.newmemberLayout.addWidget(self.ProjectmemberName_val, 0, 1)
        self.newmemberLayout.addWidget(self.ProjectmemberSurname_val, 1, 1)
        self.newmemberLayout.addWidget(self.ProjectMemberTask_val, 2, 1)

        self.NewMemberAddBtn = QPushButton('Add')
        self.newmemberLayout.addWidget(self.NewMemberAddBtn, 3, 1)
        self.NewMemberCreateBtn = QPushButton('Create')
        self.newmemberLayout.addWidget(self.NewMemberCreateBtn, 3, 4)

        self.memberList = QComboBox()
        # _____________ konumunu ayarla _____ 2-2 şeklinde ayarla __________
        self.newmemberLayout.addWidget(self.memberList, 4, 1, 1, 2)
        self.NewMemberAddBtn.clicked.connect(self.saveAndAddNew)
        self.NewMemberCreateBtn.clicked.connect(self.add_process)

        self.ProjectmemberName_val.setText("")
        self.ProjectmemberSurname_val.setText("")
        self.ProjectMemberTask_val.setText("")

        self.NewProjetmemberGroupBox.setLayout(self.newmemberLayout)

    def saveAndAddNew(self):

        self.member = self.ProjectmemberName_val.text() + " " + self.ProjectmemberSurname_val.text()
        self.memberList.insertItem(len(self.memberList), self.member)
        self.choosenMain = self.records.find({'project_name':self.choosenProject})
        self.concat = self.ProjectmemberName_val.text() + " " +  self.ProjectmemberSurname_val.text() +  " " + self.ProjectMemberTask_val.text()


        self.members.append(self.concat)
        #print(str(self.members))
        #print("Concat : "+ concat + str(type(concat)))

        #self.records.update_many({'project_name':self.choosenProject}, {'$push':{'ana_baslik':self.addprocessMainTitle_val.text()}})
        #self.records.update_many({'project_name':self.choosenMain}, {'$push':{'calisanId':concat}})

        self.ProjectmemberName_val.setText("")
        self.ProjectmemberSurname_val.setText("")
        self.ProjectMemberTask_val.setText("")    


    def add_process(self):

        self.NewProjetmemberGroupBox.deleteLater()
        self.show()

        self.resize(500, 350)
        disableWidgetsCheckBoxNew = QCheckBox("&Disable widgets")
        self.create_process()
        disableWidgetsCheckBoxNew.toggled.connect(
            self.processGroupBox.setDisabled)

        self.mainLayout.addWidget(self.processGroupBox, 0, 0)
        self.setWindowTitle("Members")

    def create_process(self):

        self.processGroupBox = QGroupBox("New Process")
        self.processLayout = QGridLayout()
        self.processStartAt,self.processFinishAt,self.processPersonInCharge = QLabel("Start at ( T0 + ): "), QLabel("Finish at ( T0 + ): "), QLabel("Person In Charge: ")
        self.processInfo, self.MainTitle, self.SubTitle = QLabel("Information: "), QLabel("Main Title: "), QLabel("Sub Title: ")
        self.processSubTitleBtn, self.processMainTitleBtn = QPushButton('Add Sub Title'), QPushButton('Add Main Title')
        self.subTitleList, self.mainTitleList  = QComboBox(), QComboBox()
       
        self.processLayout.addWidget(self.mainTitleList, 5, 2)
        self.processLayout.addWidget(self.subTitleList, 5, 4)
        self.showMainTitle()
        self.mainTitleList.currentIndexChanged.connect(self.showsubTitle)

        self.processLayout.addWidget(self.processStartAt, 1, 0, 1, 2)
        self.processLayout.addWidget(self.processFinishAt, 2, 0, 1, 2)
        self.processLayout.addWidget(self.processInfo, 4, 0, 1, 2)
        self.processLayout.addWidget(self.processPersonInCharge, 3, 0, 1, 2)
        self.processLayout.addWidget(self.MainTitle, 5, 0)
        self.processLayout.addWidget(self.SubTitle, 5, 3)
        self.processLayout.addWidget(self.processSubTitleBtn, 8, 4)
        self.processLayout.addWidget(self.processMainTitleBtn, 8, 2)

        self.processSubTitleBtn.clicked.connect(self.addSubToMain)
        self.processMainTitleBtn.clicked.connect(self.addNewMainTitle)

        self.processStartAt_val = QLineEdit()
        self.processFinishAt_val = QLineEdit()
        self.addprocessMainTitle_val = QLineEdit()
        self.addprocessSubTitle_val = QLineEdit()
        self.processPersonInCharge_val = QLineEdit()
        self.processInfo_val = QTextEdit()

        self.processLayout.addWidget(self.processStartAt_val, 1, 2, 1, 4)
        self.processLayout.addWidget(self.processFinishAt_val, 2, 2, 1, 4)
        self.processLayout.addWidget(self.addprocessMainTitle_val, 7, 2)
        self.processLayout.addWidget(self.addprocessSubTitle_val, 7, 4)
        self.processLayout.addWidget(self.processPersonInCharge_val, 3, 2, 1, 4)
        self.processLayout.addWidget(self.processInfo_val, 4, 2, 1, 4)

        self.procesCreat = QPushButton('Create')
        self.processLayout.addWidget(self.procesCreat, 8, 5)

        self.procesCreat.clicked.connect(self.create_table)
        self.processGroupBox.setLayout(self.processLayout)


    def sendProcessToDatabase(self):
       
        if self.flag_project == 1 : #yeni oluşturulan proje
            print("flag 1")
            project_val["personInCharge"] = self.processPersonInCharge_val.text()
            project_val["calisanId"] = self.members
            project_val["ana_baslik"] = mains
            self.records.insert_one(project_val)

            self.process = {
                'project_name': project_val["project_name"],
                'project_code': project_val["project_code"],
                'start_time': project_val["start_time"],
                'end_time': project_val["end_time"],
                'personInCharge': self.processPersonInCharge_val.text(),
                'calisanId': self.members,
                'main_title': mains,
            }
            self.process_records.insert_one(self.process)

        elif self.flag_project == 0:        #mevcut proje
            print("gelen proje ismi: ",self.choosenProject)
            self.choosen = self.records.find({'project_name':self.choosenProject})
            for i in self.choosen:
                self.process2 = {
                    'project_name': i['project_name'],
                    'project_code': i['project_code'],
                    'start_time': self.addprocessStartAt_val.text(),
                    'end_time': self.addprocessFinishAt_val.text(),
                    'personInCharge': self.addprocessPersonInCharge.text(),
                    'calisanId': self.members,
                    'main_title': mains
                }
            self.process_records.insert_one(self.process2)


    def create_table(self):  # tablo ayarları burada yapılıyor
        self.sendProcessToDatabase()
        # self.processGroupBox.deleteLater()
        self.show()
        disableWidgetsCheckBoxNew = QCheckBox("&Disable widgets")
        self.table()
        disableWidgetsCheckBoxNew.toggled.connect(self.createTable.setDisabled)
        disableWidgetsCheckBoxNew.toggled.connect(self.TabelPage.setDisabled)

        self.mainLayout.addWidget(self.createTable, 0, 0)
        self.setWindowTitle("Table")

    def table(self):  # tablo oluşturulan yer burası
        self.resize(1400, 870)
        self.showMaximized()
        self.createTable = QTabWidget()
        tab1hbox = QGridLayout()
        self.TabelPage = QGroupBox("Project Name")
        self.createTable.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.TabelPage.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)


        self.tableprojectName = QLabel("Project: ")
        self.tableprojectVal = QLabel()
        self.tableColors = QComboBox()
        self.subTitleList = QComboBox() 
        self.tableInfo = QTextEdit()
        self.excelButton = QPushButton("Export to Excel")
        self.tableInfo.setText(project_val['project_info'])
        self.tableprojectInfo = QLabel()
        self.setWindowTitle("Table")
        self.tableColors.addItems({'pink','blue','yellow','red','orange','green','grey'})
        if self.flag_project == 1:
            self.tableprojectName.setText(project_val["project_name"])
        else : self.tableprojectName.setText(self.choosenProject)

        tab1hbox.addWidget(self.mainTitleList,8,10)
        self.showMainTitle()
        self.showsubTitle()
        tab1hbox.addWidget(self.subTitleList,8,11)
        tab1hbox.addWidget(self.tableprojectName,0,1)
        tab1hbox.addWidget(self.tableColors,0,2)
        tab1hbox.addWidget(self.tableInfo,2,10,6,2)
        tab1hbox.addWidget(self.excelButton,9,10)

        tab1 = QWidget()
        self.tableWidget = QTableWidget(200,20)   # kaça kaçlık olacağını vermiş
        self.excelButton.clicked.connect(self.exportExcel)
        #_________________

        self.projectForRow = self.records.find({'project_name':self.tableprojectName.text()})
        self.rows = []
        for i in self.projectForRow:
            for k in range(len(i['ana_baslik'])):
                self.rows.append(str(i['ana_baslik'][k]))
        
        liste = list()
        #self.getColumnsCount()
        for k in range(self.tableWidget.columnCount()):
            liste.append(str(k + 1))
        self.tableWidget.setHorizontalHeaderLabels(liste)    

        
        self.tableWidget.setVerticalHeaderLabels(self.rows)
        

        tab1hbox.addWidget(self.tableWidget,1,1,10,8)
        tab1.setLayout(tab1hbox)
        
        self.tableWidget.selectionModel().selectionChanged.connect(self.colored) # bu kısım seçilen hücreler için işlem yapabilme fonksiyonu
        #_______________
        #self.setStyleSheet('selection-background-color:red')
        
        self.createTable.addTab(tab1, "&Table")
    
    def getColumnsCount(self):
        self.columnCount = (project_val['end_time']-project_val['start_time'])//1125
        print(self.columnCount)
 
    def colored(self, selected,deselected):
        for x in selected.indexes():
            print('Selected Cell Location Row: {0}, Column: {1}'.format(x.row(),x.column()))
            # palette = self.tableWidget.palette()
            # brush = palette.brush(QPalette.Background)
            # brush.setColor(QColor('red'))
            self.setStyleSheet('selection-background-color:red;background-attachment: scroll;')
            #self.tableWidget.item(x.row(),x.column()).setBackground(QColor(100,100,50))
            #self.tableWidget.item(x.row(),x.column()).setS

            # pallete = self.tableWidget.palette()
            # hightlight_brush = pallete.brush(QPalette.Highlight)
            # hightlight_brush.setColor(QColor('red'))
            # pallete.setBrush(QPalette.Highlight, hightlight_brush)
            # self.tableWidget.setPalette(pallete)
        

        # for x in deselected.indexes():
        #     print('Selected Cell Location Row: {0}, Column: {1}'.format(x.row(),x.column()))

    def exportExcel(self):
        columnHeaders = []

        for j in range(self.tableWidget.model().columnCount()):
            columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders)

        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                if item:= self.tableWidget.item(row,col):
                    df.at[row, columnHeaders[col]] = self.tableWidget.item(row,col).text()

        df.to_excel('ExcelFile.xlsx', index=False)


    def connect_db(self):

        self.client = MongoClient("..")
        self.db = self.client.get_database('project_collection')
        self.records = self.db.projects

        self.process_db = self.client.get_database('process_collection')
        self.process_records = self.process_db.process

        self.mainTitle_db = self.client.get_database('mainTitle_collection')
        self.mainTitle_records = self.mainTitle_db.mainTitle


app = QApplication(sys.argv)
gallery = App()
gallery.show()
sys.exit(app.exec())