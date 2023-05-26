import sys
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QLabel,QHBoxLayout,QVBoxLayout,QPushButton,QFileDialog,QAction,QToolBar,QMenuBar,QStatusBar,QColorDialog,QMenu
from PyQt5.QtGui import QPen,QPainter,QBrush,QColor,QPixmap,QIcon
from PyQt5.QtCore import Qt,QSize,QRect,QPoint

COLORS = [
  "#414168",
  "#3a7fa7",
  "#8fd970",
  "#35e3e3",
  "#5ebb49",
  "#000000",
  "#458352",
  "#dcd37b",
  "#ffd035",
  "#fffee5",
  "#141923",
  "#cc9245",
  "#a15c3e",
  "#a42f3b",
  "#f45b7a",
  "#c24998",
  "#81588d",
  "#bcb0c2",
  "#ffffff",
]
COLORS=COLORS[::-1]

class Canvas(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent

        # self._pixmap=QPixmap(width,height)
        self._pixmap=QPixmap(900,600)
        # self._pixmap.fill(Qt.white)
        self._pixmap.fill(QColor(255,255,255,245))
        self.setPixmap(self._pixmap)
        # coordinates
        self.last_x,self.last_y=None,None

        self.pen_color=QColor(Qt.black)
        self.background_color=QColor(Qt.white)

        self.eraser_on=False

        # track coordinates for polygon
        self.all_points_vector=[]
        self.polygon_points=[]
        self.isTracking=False

        # opened_image_properties
        self.image_pixmap_width=None
        self.image_pixmap_height=None
        self.image_pixmap_format=None

        # __status_bar_configuration__
        self.status_label=QLabel()
        self.status_label.setStyleSheet('''
            color:white;
            font-size:30px;
            font-family:consolas;
            background-color:rgba(0,0,0,95)
            ''')
        self.status_label.setText("Tracing disabled")
        self.parent.status_bar.addWidget(self.status_label)
        

    def set_pen_color(self,color):
        # print(color)
        self.pen_color=QColor(color)

    def mouseMoveEvent(self, event):
        # print(event.pos())
        if self.isTracking:
            # print('hello')
            self.polygon_points.append(event.pos())

        if self.last_x==None:
            self.last_x,self.last_y=event.x(),event.y()
            return
        
            

        painter=QPainter(self.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        pen=QPen()
        pen.setColor(self.pen_color)
        # print(self.pen_color.getRgb())
        pen.setWidth(3)
        painter.setPen(pen)

        if self.eraser_on:
            rect=QRect(event.x(),event.y(),50,50)
            painter.eraseRect(rect)
            

        else:
            painter.drawLine(self.last_x,self.last_y,event.x(),event.y())
        
        self.last_x,self.last_y=event.x(),event.y()

        painter.end()
        self.update()

    def mouseReleaseEvent(self, event):
        self.last_x,self.last_y=None,None

    def drawPolygon(self,all_points):
        painter=QPainter(self.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        # pen=QPen()
        # pen.setWidth(2)
        # pen.setColor(self.pen_color)
        # painter.setPen(pen)
        brush=QBrush()
        brush.setColor(self.pen_color)
        # brush.setStyle(Qt.Dense1Pattern)
        brush.setStyle(Qt.SolidPattern)
        
        painter.setBrush(brush)
        for points in all_points:
            painter.drawPolygon(points)

        painter.end()
        self.update()

    
    def start_tracking_points(self):
        self.polygon_points=[]
        self.isTracking=True
        self.status_label.setText("Tracing enabled")

    def stop_tracking_points(self):
        self.all_points_vector.append(self.polygon_points)
        self.polygon_points=[]
        self.isTracking=False
        self.status_label.setText("Tracing disabled")
        # self.parent.status_bar.setVisible(False)

    def print_track_points(self):
        # print(len(self.polygon_points))
        # print(self.polygon_points)
        self.drawPolygon(self.all_points_vector)

    def clear_track_points(self):
        self.polygon_points=[]

    
    def clear_canvas(self):
        # self._pixmap.fill(Qt.white)
        self._pixmap.fill(QColor(255,255,255,30))
        self.setPixmap(self._pixmap)
        self.polygon_points=[]
        self.all_points_vector=[]
        self.isTracking=False

    def set_eraser_on(self):
        self.eraser_on=True

    def set_eraser_off(self):
        self.eraser_on=False


    def set_image_pixmap_for_canvas(self):

        filename,_=QFileDialog.getOpenFileName(self,"Select Image","","All Files(*);;png(*.png);;jpg(*.jpg);;jpeg(*.jpeg)")
        # print(_.format())
        if filename:
            image=QPixmap(filename)
            # print(filename.split("."))
            lst=filename.split(".")
            self.image_pixmap_format=lst[len(lst)-1]
            
            self.image_pixmap_width=image.width()
            self.image_pixmap_height=image.height()
            # print("(",self.image_pixmap_width,self.image_pixmap_height,")")
            self.setPixmap(image.scaled(self.width(),self.height(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
            # self.setStyleSheet("background-image : url(saved.png);")
            


    
    def save_image_pixmap_of_canvas(self):
        filename,_=QFileDialog.getSaveFileName(self,"Save Image as",'',"All Files(*);;png(*.png);;jpg(*.jpg);;jpeg(*.jpeg)")

        if filename and self.image_pixmap_width!=None:
            image=self.pixmap()
            image=image.scaled(self.image_pixmap_width,self.image_pixmap_height,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            # image.setIccProfile("sRGB")
            # print(self.image_pixmap_format)
            image.save(filename,self.image_pixmap_format)

    
    def select_color(self):
        color=QColorDialog(Qt.black,self).getColor()
        self.pen_color=color
        # print(dialog.toRgb())

    def set_background_color(self):
        color=QColorDialog(Qt.white,self).getColor()
        self.background_color=color

    def fill_background_color(self):
        self.pixmap().fill(self.background_color)
        # self.drawPolygon(self.all_points_vector)

            



class QPaletteButton(QPushButton):
    def __init__(self,color):
        super().__init__()
        self.setFixedSize(QSize(25,25))
        self.setStyleSheet("background-color:{};".format(color))


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            QMenuBar {
                background-color:rgba(255,255,255,150);
                color: #FFFFFF;
                font-size:24px;
                font-family:consolas;
                padding-top:10px;    
                padding-left:10px;    
            }
            QMenuBar::item {
                spacing: 3px;
                color: #000000;
                font-size: 26px;
            }
            QMenuBar::item:selected {
                background-color: rgb(200,200,200);
            }
            QMenu {
                background-color: #332233;
                color: #FFFFFF;
                font-size:20px;
                font-family:consolas;
                padding: 5px 10px;
            }
        """)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(50)
        
        # Initialize the flag
        self.is_moving = False
        
        # Store the initial mouse position
        self.mouse_pos = None


    def mouseDoubleClickEvent(self, event):
        # Check if the event position is within the menubar area
        menubar_rect = self.geometry()
        if menubar_rect.contains(event.pos()) and (event.pos().x()>150):
            self.is_moving = True
            self.mouse_pos = event.globalPos()
            
    def mouseMoveEvent(self, event):
        if self.is_moving:
            # Calculate the new window position
            diff = event.globalPos() - self.mouse_pos
            new_pos = self.parent().pos() + diff
            self.parent().move(new_pos)
            self.mouse_pos = event.globalPos()
            
    def mouseReleaseEvent(self, event):
        # if self.is_moving:
        self.is_moving = False
        self.mouse_pos = None



class MainWindow(QMainWindow):
    global COLORS
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Painting")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        xpos=self.width()-self.width()//4
        ypos=self.height()-self.height()//2

        desktoprect=QApplication.desktop().availableGeometry(self)
        center=desktoprect.center()

        self.setGeometry(center.x()-(2*self.width()//3),center.y()-(2*self.height()//3),self.width(),self.height())

        # self.setGeometry(xpos,ypos,self.width(),self.height())
        # self.setFixedSize(900,600)


        # __status_bar__
        self.status_bar=QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setSizeGripEnabled(False) # to remove the dots in the bottom-right corner
        self.status_bar.setStyleSheet('''
            padding:1px 1px;
            ''')

        widget=QWidget()
        widget.setStyleSheet("margin:0px;")
        # self._canvas=Canvas(self,self.width(),self.height())
        self._canvas=Canvas(self)

        self._canvas.setStyleSheet("margin:0px;")

        self._layout=QVBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)

        hor=QHBoxLayout()

        self.add_color_palette(hor)

        self._layout.addWidget(self._canvas)
        self._layout.addLayout(hor)

        widget.setLayout(self._layout)

        self.setCentralWidget(widget)

        # __menu_bar__
        self.createMenuBar()

        # __tool_bar__
        self.createToolBar()

        
        # print(self.width(),self.height())


    def add_color_palette(self,layout):
        global COLORS
        for color in COLORS:
            button=QPaletteButton(color)
            layout.addWidget(button)
            button.pressed.connect(lambda color=color:self._canvas.set_pen_color(color))

    def createMenuBar(self):

        menu=MenuBar(self)

        # __file__menu_item__
        file=menu.addMenu("File")
        
        newCanvas=QAction("New",self)
        newCanvas.setShortcut("Ctrl+N")
        newCanvas.triggered.connect(self._canvas.clear_canvas)
        file.addAction(newCanvas)

        openImage=QAction("Open",self)
        openImage.setShortcut("Ctrl+O")
        openImage.triggered.connect(self._canvas.set_image_pixmap_for_canvas)
        file.addAction(openImage)

        saveImage=QAction("Save",self)
        saveImage.setShortcut("Ctrl+S")
        saveImage.triggered.connect(self._canvas.save_image_pixmap_of_canvas)
        file.addAction(saveImage)

        quit_app=QAction("Save",self)
        quit_app.setShortcut("Esc")
        quit_app.triggered.connect(self.close)
        file.addAction(quit_app)

        self.setMenuBar(menu)

    
    def createToolBar(self):
        toolbar=QToolBar("Toolbar")
        toolbar.setStyleSheet('''
        QToolBar{
            background-color:rgba(250,250,250,80);
            spacing: 20px;
        }        
        ''')
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(40,40))
        self.addToolBar(Qt.LeftToolBarArea,toolbar)

        pen=QAction(QIcon("icons/pencil.png"),"Pencil",toolbar)
        pen.triggered.connect(self._canvas.set_eraser_off)
        toolbar.addAction(pen)

        # eraser=QAction(QIcon("icons/eraser.png"),"Pencil",toolbar)
        # eraser.triggered.connect(self._canvas.set_eraser_on)
        # toolbar.addAction(eraser)

        start=QAction(QIcon("icons/start.png"),"Start Tracing",toolbar)
        start.triggered.connect(self._canvas.start_tracking_points)
        toolbar.addAction(start)

        stop=QAction(QIcon("icons/stop.png"),"Stop Tracing",toolbar)
        stop.triggered.connect(self._canvas.stop_tracking_points)
        toolbar.addAction(stop)

        fill=QAction(QIcon("icons/fill.png"),"Fill the polygon",toolbar)
        fill.triggered.connect(self._canvas.print_track_points)
        toolbar.addAction(fill)

        color=QAction(QIcon("icons/colour.png"),"Color",toolbar)
        color.triggered.connect(self._canvas.select_color)
        toolbar.addAction(color)

    
    def contextMenuEvent(self, event):
        contextMenu=QMenu(self._canvas)

        select_color=QAction("select background color",self)
        select_color.triggered.connect(self._canvas.set_background_color)
        contextMenu.addAction(select_color)

        fill_color=QAction("fill background",self)
        fill_color.triggered.connect(self._canvas.fill_background_color)
        contextMenu.addAction(fill_color)

        contextMenu.exec_(event.globalPos())




        




    def keyPressEvent(self, event):
        key=event.key()
        
        if key==Qt.Key_S:
            # print("start")
            self._canvas.start_tracking_points()

        if key==Qt.Key_X:
            # print("stop")
            self._canvas.stop_tracking_points()

        if key==Qt.Key_P:
            # print("print")
            self._canvas.print_track_points()

        if key==Qt.Key_O:
            self._canvas.set_image_pixmap_for_canvas()

        if key==Qt.Key_C:
            self._canvas.save_image_pixmap_of_canvas()

        if key==Qt.Key_E:
            self._canvas.set_eraser_on()

        if key==Qt.Key_Escape:
            self.close()

        



if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

