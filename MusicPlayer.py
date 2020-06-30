from PyQt5.QtWidgets import *
from PyQt5 import QtMultimedia,QtMultimediaWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Music_Player(QWidget):
    def __init__(self):
        super(Music_Player, self).__init__()
        self.setWindowTitle('Music Player-Pro')
        self.setWindowIcon(QIcon('music.png'))

        #Music Player MainWidget
        self.mediaplayer = QtMultimedia.QMediaPlayer()
        self.mediaplayer.positionChanged.connect(self.position)
        self.mediaplayer.durationChanged.connect(self.duration)
        self.player()
        self.show()

    def player(self):
        #Initializing the folder and song to be selected as None
        self.folder=None
        self.url = None
        self.lay=QVBoxLayout()

        #Creating Actions for the layout
        self.playbtn=QPushButton('Play')
        self.playbtn.setFont(QFont('Comic Sans MS', 10))
        self.playbtn.clicked.connect(self.play)
        self.playbtn.setIcon(QIcon('play.png'))
        self.playbtn.setMinimumSize(60,60)
        self.playbtn.setStyleSheet('border-radius:30px;background-color:lightgreen')

        self.pausebtn=QPushButton('Pause')
        self.pausebtn.clicked.connect(self.pause)
        self.pausebtn.setIcon(QIcon('pause.png'))
        self.pausebtn.setMinimumSize(60, 60)
        self.pausebtn.setStyleSheet('border-radius:30px;background-color:lightblue')
        self.pausebtn.setFont(QFont('Comic Sans MS', 10))

        self.stopbtn=QPushButton('Stop')
        self.stopbtn.clicked.connect(self.stop)
        self.stopbtn.setFont(QFont('Comic Sans MS', 10))
        self.stopbtn.setIcon(QIcon('stop.png'))
        self.stopbtn.setMinimumSize(60, 60)
        self.stopbtn.setStyleSheet('border-radius:30px;background-color:orange')
        self.hb=QHBoxLayout()
        self.hb.addWidget(self.playbtn)
        self.hb.addWidget(self.pausebtn)
        self.hb.addWidget(self.stopbtn)

        self.openfold=QPushButton('Select Folder')
        self.openfold.setFont(QFont('Comic Sans MS', 10))
        self.openfold.clicked.connect(self.openfolder)

        self.selbtn=QPushButton('Select Song')
        self.selbtn.setFont(QFont('Comic Sans MS', 10))
        self.selbtn.clicked.connect(self.openfile)

        self.lll=QLabel()
        self.lll.setPixmap(QPixmap('sond.png'))

        self.volume=QSlider()
        self.volume.setValue(100)
        self.volume.setMaximum(100)
        self.volume.setOrientation(Qt.Horizontal)
        self.volume.valueChanged.connect(self.volumeslider)

        self.lbl=QLabel('100')

        self.hb1=QHBoxLayout()
        self.hb1.addWidget(self.openfold)
        self.hb1.addWidget(self.selbtn)
        self.hb1.addWidget(self.lll)
        self.hb1.addWidget(self.volume)
        self.hb1.addWidget(self.lbl)

        self.hh=QHBoxLayout()

        self.hh.addWidget(QLabel(''))   #To get some space in between

        self.slider1 = QSlider()
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.sliderMoved.connect(self.set_position)
        self.slider1lbl1=QLabel('0.0')
        self.slider1lbl1.setFont(QFont('verdana',10))
        self.slider1lbl2=QLabel('0.0')
        self.slider1lbl2.setFont(QFont('verdana', 10))

        self.lab=QLabel('Currently Playing Song:None')
        self.lab.setFont(QFont('Comic Sans MS',15))

        self.hh.addWidget(self.slider1lbl1)
        self.hh.addWidget(self.slider1)
        self.hh.addWidget(self.slider1lbl2)

        self.hhhh=QHBoxLayout()
        self.hhhh.addWidget(self.lab)

        self.lay.addLayout(self.hb1)
        self.lay.addLayout(self.hb)
        self.lay.addLayout(self.hh)
        self.lay.addLayout(self.hhhh)
        # self.lay.addStretch(1)

        self.setLayout(self.lay)

    def play(self):
        #Function to check that if any song is selected or not
        if self.url:
            self.mediaplayer.play()
        else:
            QMessageBox.information(self,'Play','Please Select A Song First')

    def pause(self):
        self.mediaplayer.pause()

    def stop(self):
        self.mediaplayer.stop()

    def volumeslider(self):
        #For changing the volume of the music player
        self.mediaplayer.setVolume(self.volume.value())
        self.lbl.setText(str(self.volume.value()))

    def openfolder(self):
        #For Selecting a folder of songs
        self.list=QListWidget()
        self.folder=QFileDialog.getExistingDirectory(self,'Open Music Folder','E:\\')#Gets folder from The E:\\ Directory
        if self.folder!='E:/':#Checking If ANy Folder IS selected or not
            it=QDirIterator(self.folder) #Iterates over the files in folder
            it.next() #First File Is Stored In This
            i=0#Inserting items in ListWidget
            while it.hasNext(): #While folder has data
                st = it.fileInfo() #Information of the corresponding file
                if st.suffix()=='mp3':
                    self.list.insertItem(i,str(it.filePath()))
                    i+=1
                it.next()
            if i==0:
                QMessageBox.information(self,'Folder','No Music Files Detected')
            else:
                QMessageBox.information(self,'Folder','Folder Added Successfully')
        else:
            QMessageBox.information(self, 'Select Song', 'Please Select The Folder')
    def openfile(self):
        if self.folder and self.folder!='E:/': #If the folder is selected

            #This Is The New Dialog Which Have The list Of songs
            self.di=QDialog(self)
            self.di.setWindowTitle('Song List')
            self.bo=QVBoxLayout()
            self.bo.addWidget(self.list)
            self.di.setLayout(self.bo)
            self.okbutton=QPushButton('OK')
            self.okbutton.setFont(QFont('Comic Sans MS',20))
            self.okbutton.clicked.connect(self.setsong)
            self.bo.addWidget(self.okbutton)
            self.di.open()
        else:
            QMessageBox.information(self,'Select Song','Please Select The Folder')

    def setsong(self):
        L = str(self.list.currentItem().text())
        L = L.replace('E:/MusicFiles', '')
        self.lab.setText(f"Currently Playing Song:{L}")
        #setting up the name of the song in music player to play the song
        self.url=QUrl(str(self.list.currentItem().text()))
        self.content=QtMultimedia.QMediaContent(self.url)
        self.mediaplayer.setMedia(self.content)
        self.di.close()

    def position(self,position):
        #Second Slider Denoting The Position of the song played
        self.slider1.setValue(position)
        self.slider1lbl1.setText('%d:%02d' % (int(position / 60000), int((position / 1000) % 60)))
    def duration(self,duration):

        self.slider1lbl2.setText('%d:%02d' % (int(duration / 60000), int((duration / 1000) % 60)))#Complete Duration of the song
        self.slider1.setRange(0,duration)#Setting The range of the slider  be

    def set_position(self,position):
        #If The song is moved forward or backward through slider it will set its current position
        self.mediaplayer.setPosition(position)

if __name__=='__main__':
    app=QApplication(sys.argv)
    wind=Music_Player()
    sys.exit(app.exec())