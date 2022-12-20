from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import *
import sys, json, copy
import numpy as np
import seaborn as sns
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Arc, Circle

class CustomDialog(QDialog):
    def __init__(self, parent=None, mess=None, title=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(270, 90)
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(mess)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MySpinBox(QDoubleSpinBox):
    def __init__(self, ind, params=dict()):
        super().__init__(**params)
        self.ind = ind

class OpenWindow(QMainWindow):
    __data = {
        'robotype': 'Декарт',
        'movetype': 'Позиционное',
        'param_dec': [10.0, 6.0, 2.0, 0.002],
        'coord_dec': [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        'param_cil': [1.5, 0.1, 0.002, 0.6, 0.4, 0.2, 6.0, 2.0],
        'coord_cil': [-1.5, 1.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0],
        'param_scr': [1.5, 0.1, 0.002, 0.6, 0.4, 0.2, 6.0, 2.0],
        'coord_scr': [-1.5, 1.5, -2.5, 2.5, -6.280, 6.280, 0.1, 0.4],
        'engine': [0.001, 0.001, 0.001, 0.001, 100.0, 250.0, 30.0, 30.0, 26.0, 26.0,
                   27.0, 27.0, 0.002, 0.002, 0.002, 0.002, 0.0, 0.0, 0.0, 0.0],
        'reg': [200.0, 200.0, 200.0, 200.0, 0.0, 0.0, 0.0, 0.0, 30.0, 30.0, 30.0, 30.0],
        'calc': [16.0, 0.008, 0.016, 0.016],
        'line': [0.0, 1.0, 0.0, 1.0, 1.0],
        'circle': [0.5, 0.5, 0.5, 0.5],
        'line_or_circle': 'line',
        'ciclogram': [[_ for _ in range(1, 10)],
                      [0.5, 1] * 4 + [0],
                      [0.3, 0.6] * 4 + [0],
                      [0.2, 0.5] * 4 + [0],
                      [0.15, 0.3] * 4 + [0]]
    }
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Робот")
        self.setMinimumSize(535, 400)
        menu = self.menuBar()

        self.path_to_file = None
        self.data = copy.deepcopy(self.__data)

        #СПРАВОЧНАЯ ИНФОРМАЦИЯ------------------------------------------------------------------------------------------
        menu1 = menu.addMenu("Справочная информация")

        action1_about = QAction("About", self)
        action1_about.triggered.connect(self.show1_about_window)
        action1_robot_img = QAction("Схема робота", self)
        action1_robot_img.triggered.connect(self.show1_robot_img_window)
        action1_help = QAction("Помощь", self)
        action1_help.triggered.connect(self.show1_help_window)

        menu1.addAction(action1_about)
        menu1.addAction(action1_robot_img)
        menu1.addAction(action1_help)

        #СОХРАНЕНИЯ-----------------------------------------------------------------------------------------------------
        menu2 = menu.addMenu("Сохранения")

        action2_new = QAction("Новый", self)
        action2_new.triggered.connect(self.show2_new_window)
        action2_load = QAction("Загрузить", self)
        action2_load.triggered.connect(self.show2_load_window)
        action2_save = QAction("Сохранить", self)
        action2_save.triggered.connect(self.show2_save_window)
        action2_save_as = QAction("Сохранить как", self)
        action2_save_as.triggered.connect(self.show2_saveas_window)

        menu2.addAction(action2_new)
        menu2.addAction(action2_load)
        menu2.addAction(action2_save)
        menu2.addAction(action2_save_as)

        #РЕЖИМ РАБОТЫ---------------------------------------------------------------------------------------------------
        menu3 = menu.addMenu("Режим работы")

        action3_rob = QAction("Тип робота", self)
        action3_rob.triggered.connect(self.show3_select_robotype)
        action3_mov = QAction("Тип движения", self)
        action3_mov.triggered.connect(self.show3_select_movetype)

        menu3.addAction(action3_rob)
        menu3.addAction(action3_mov)

        #НАСТРОЙКА ПАРАМЕТРОВ-------------------------------------------------------------------------------------------
        menu4 = menu.addMenu("Настройка параметров")

        action4_param_dec = QAction("Конструктивные параметры", self)
        action4_param_dec.triggered.connect(self.show4_select_param_dec)
        action4_coord_dec = QAction("Ограничение по координатам", self)
        action4_coord_dec.triggered.connect(self.show4_select_coord_dec)

        action4_param_cil = QAction("Конструктивные параметры", self)
        action4_param_cil.triggered.connect(self.show4_select_param_cil)
        action4_coord_cil = QAction("Ограничение по координатам", self)
        action4_coord_cil.triggered.connect(self.show4_select_coord_cil)

        action4_param_scr = QAction("Конструктивные параметры", self)
        action4_param_scr.triggered.connect(self.show4_select_param_scr)
        action4_coord_scr = QAction("Ограничение по координатам", self)
        action4_coord_scr.triggered.connect(self.show4_select_coord_scr)

        menu4_1 = menu4.addMenu("Робот")
        menu4_1_dec = menu4_1.addMenu("Декарт")
        menu4_1_dec.addAction(action4_param_dec)
        menu4_1_dec.addAction(action4_coord_dec)

        menu4_1_cil = menu4_1.addMenu("Цилиндр")
        menu4_1_cil.addAction(action4_param_cil)
        menu4_1_cil.addAction(action4_coord_cil)

        menu4_1_scr = menu4_1.addMenu("Скара")
        menu4_1_scr.addAction(action4_param_scr)
        menu4_1_scr.addAction(action4_coord_scr)

        action4_engine = QAction("Параметры двигателей", self)
        action4_engine.triggered.connect(self.show4_select_engine)
        action4_reg = QAction("Параметры регуляторов", self)
        action4_reg.triggered.connect(self.show4_select_reg)

        menu4_2 = menu4.addMenu("Система управления")
        menu4_2.addAction(action4_engine)
        menu4_2.addAction(action4_reg)

        action4_calc = QAction("Вычислитель", self)
        action4_calc.triggered.connect(self.show4_select_calc)
        menu4_3 = menu4.addAction(action4_calc)

        action4_pos_move = QAction("Позиционное", self)
        action4_pos_move.triggered.connect(self.show4_select_pos_move)
        action4_cont_line = QAction("Прямая", self)
        action4_cont_line.triggered.connect(self.show4_select_cont_line)
        action4_cont_circle = QAction("Окружность", self)
        action4_cont_circle.triggered.connect(self.show4_select_cont_circle)

        menu4_4 = menu4.addMenu("Движение")
        menu4_4.addAction(action4_pos_move)
        menu4_4_cont = menu4_4.addMenu("Контурное")
        menu4_4_line = menu4_4_cont.addAction(action4_cont_line)
        menu4_4_circle = menu4_4_cont.addAction(action4_cont_circle)

        #РАСЧЁТ---------------------------------------------------------------------------------------------------------
        menu5 = menu.addMenu("Расчёт")

        action5_show_area = QAction("Рабочая область", self)
        action5_show_area.triggered.connect(self.show5_workspace)
        action5_plot = QAction("График", self)

        menu5.addAction(action5_show_area)
        menu5.addAction(action5_plot)

    #СПРАВОЧНАЯ ИНФОРМАЦИЯ ФУНКЦИИ--------------------------------------------------------------------------------------
    def show1_about_window(self, checked):
        self.w1_about = QWidget()
        self.w1_about.setFixedSize(220, 160)

        about = QLabel("Моделирование роботов\n Декарт, Цилинр, Скара\n Дипломный проект 2022-2023")
        about.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay1_about = QGridLayout()
        lay1_about.addWidget(about)

        self.w1_about.setLayout(lay1_about)
        self.w1_about.setWindowTitle("About")
        self.w1_about.show()

    def show1_robot_img_window(self, checked):
        self.w1_robot_img = QWidget()
        self.w1_robot_img.setFixedSize(500, 400)

        if self.data['robotype'] == 'Декарт':
            pixmap = QPixmap("РоботДекарт.png")
        elif self.data['robotype'] == 'Цилиндр':
            pixmap = QPixmap("РоботЦилиндр.png")
        elif self.data['robotype'] == 'Скара':
            pixmap = QPixmap("РоботСкара.png")

        pixmap = pixmap.scaled(500, 400)
        label = QLabel(self.w1_robot_img)
        label.setPixmap(pixmap)

        self.w1_robot_img.setWindowTitle("Схема робота")
        self.w1_robot_img.show()

    def show1_help_window(self, checked):
        self.w1_help = QWidget()
        self.w1_help.setFixedSize(690, 520)
        help1 = QLabel("ПАКЕТ ПРИКЛАДНЫХ ПРОГРАММ\n «МОДЕЛИРОВАНИЕ РОБОТОВ»\n")
        help_text_file = open('help.txt', encoding='utf-8')
        help_text = help_text_file.read()
        help2 = QLabel(help_text)
        help_text_file.close()

        help1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay1_help = QGridLayout()
        lay1_help.addWidget(help1)
        lay1_help.addWidget(help2)

        self.w1_help.setLayout(lay1_help)
        self.w1_help.setWindowTitle("Помощь")
        self.w1_help.show()

    #СОХРАНЕНИЯ ФУНКЦИИ-------------------------------------------------------------------------------------------------
    def show2_new_window(self, checked):
        dig = CustomDialog(self, "Вы уверены, что хотите сбросить\n все настройки и начать заново?", "Внимание!")
        if dig.exec():
            self.path_to_file = None
            self.data = copy.deepcopy(self.__data)

    def show2_load_window(self, checked):
        load_file_name = QFileDialog.getOpenFileName(self, 'Выберите файл для загрузки')
        load_file_path = load_file_name[0]
        if load_file_path:
            with open(load_file_path, 'r', encoding='utf-8') as load_file:
                self.data = json.load(load_file)
            self.path_to_file = load_file_path

    def show2_save_window(self, checked):
        if self.path_to_file:
            with open(self.path_to_file, 'w', encoding='utf-8') as save_file:
                json.dump(self.data, save_file)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Выберите файл для сохранения')
            file_path = file_name[0] + '.json'
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.data, save_file)
                self.path_to_file = file_path

    def show2_saveas_window(self, checked):
        saveas_file_name = QFileDialog.getSaveFileName(self, 'Выберите файл для сохранения')
        saveas_file_path = saveas_file_name[0]
        if saveas_file_path:
            with open(saveas_file_path + '.json', 'w', encoding='utf-8') as save_file:
                json.dump(self.data, save_file)
            self.path_to_file = saveas_file_path

    #РЕЖИМ РАБОТЫ ФУНКЦИИ-----------------------------------------------------------------------------------------------
    def show3_select_robotype(self, checked):
        self.w3_robot = QWidget()
        self.w3_robot.setFixedSize(300, 120)

        check_robot1 = QCheckBox('Декарт')
        check_robot2 = QCheckBox('Цилиндр')
        check_robot3 = QCheckBox('Скара')

        self.rob_dict = {
            'Декарт': check_robot1,
            'Цилиндр': check_robot2,
            'Скара': check_robot3
        }

        self.rob_dict[self.data['robotype']].setChecked(True)

        check_robot1.stateChanged.connect(self.show3_uncheck1)
        check_robot2.stateChanged.connect(self.show3_uncheck1)
        check_robot3.stateChanged.connect(self.show3_uncheck1)

        lay3_robot = QGridLayout()
        lay3_robot.addWidget(check_robot1)
        lay3_robot.addWidget(check_robot2)
        lay3_robot.addWidget(check_robot3)

        self.w3_robot.setLayout(lay3_robot)
        self.w3_robot.setWindowTitle("Тип робота")
        self.w3_robot.show()

    def show3_uncheck1(self, state):
        if state:
            if self.sender() == self.rob_dict['Декарт']:
                self.rob_dict['Цилиндр'].setChecked(False)
                self.rob_dict['Скара'].setChecked(False)
                self.data['robotype'] = 'Декарт'

            elif self.sender() == self.rob_dict['Цилиндр']:
                self.rob_dict['Декарт'].setChecked(False)
                self.rob_dict['Скара'].setChecked(False)
                self.data['robotype'] = 'Цилиндр'

            elif self.sender() == self.rob_dict['Скара']:
                self.rob_dict['Декарт'].setChecked(False)
                self.rob_dict['Цилиндр'].setChecked(False)
                self.data['robotype'] = 'Скара'

    def show3_select_movetype(self, checked):
        self.w3_move = QWidget()
        self.w3_move.setFixedSize(300, 120)

        check_move1 = QCheckBox('Позиционное')
        check_move2 = QCheckBox('Контурное')

        self.move_dict = {
            'Позиционное': check_move1,
            'Контурное': check_move2,
        }

        self.move_dict[self.data['movetype']].setChecked(True)

        check_move1.stateChanged.connect(self.show3_uncheck2)
        check_move2.stateChanged.connect(self.show3_uncheck2)

        lay3_move = QGridLayout()
        lay3_move.addWidget(check_move1)
        lay3_move.addWidget(check_move2)

        self.w3_move.setLayout(lay3_move)
        self.w3_move.setWindowTitle("Тип движения")
        self.w3_move.show()

    def show3_uncheck2(self, state):
        if state:
            if self.sender() == self.move_dict['Позиционное']:
                self.move_dict['Контурное'].setChecked(False)
                self.data['movetype'] = 'Позиционное'

            elif self.sender() == self.move_dict['Контурное']:
                self.move_dict['Позиционное'].setChecked(False)
                self.data['movetype'] = 'Контурное'

    #НАСТРОЙКА ПАРАМЕТРОВ ФУНКЦИИ---------------------------------------------------------------------------------------
    def show4_select_param_dec(self, checked):
        self.w4_param_dec = QWidget()
        self.w4_param_dec.setFixedSize(500, 100)

        label1_param_dec = QLabel('Масса 1-го звена')
        label2_param_dec = QLabel('Масса 2-го звена')
        label3_param_dec = QLabel('Масса 3-го звена')
        label4_param_dec = QLabel('Момент инерции')

        param_dec = self.data['param_dec']
        input1_param_dec = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_dec[0])
        input1_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 0))
        input2_param_dec = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_dec[1])
        input2_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 1))
        input3_param_dec = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_dec[2])
        input3_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 2))
        input4_param_dec = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0,value = param_dec[3])
        input4_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 3))

        grid4_param_dec = QGridLayout()
        grid4_param_dec.addWidget(label1_param_dec, 0, 0)
        grid4_param_dec.addWidget(label2_param_dec, 0, 1)
        grid4_param_dec.addWidget(label3_param_dec, 0, 2)
        grid4_param_dec.addWidget(label4_param_dec, 0, 3)
        grid4_param_dec.addWidget(input1_param_dec, 1, 0)
        grid4_param_dec.addWidget(input2_param_dec, 1, 1)
        grid4_param_dec.addWidget(input3_param_dec, 1, 2)
        grid4_param_dec.addWidget(input4_param_dec, 1, 3)

        self.w4_param_dec.setLayout(grid4_param_dec)
        self.w4_param_dec.setWindowTitle("Конструктивные параметры Декарт")
        self.w4_param_dec.show()

    def show4_change_param_dec(self, change, key):
        self.data['param_dec'][key] = change

    def show4_select_coord_dec(self, checked):
        self.w4_coord_dec = QWidget()
        self.w4_coord_dec.setFixedSize(500, 150)

        label1_coord_dec = QLabel('Xmin')
        label2_coord_dec = QLabel('Xmax')
        label3_coord_dec = QLabel('Ymin')
        label4_coord_dec = QLabel('Ymax')
        label5_coord_dec = QLabel('Q3min')
        label6_coord_dec = QLabel('Q3max')
        label7_coord_dec = QLabel('Zmin')
        label8_coord_dec = QLabel('Zmax')

        coord_dec = self.data['coord_dec']
        input1_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[0])
        input1_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 0))
        input2_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[1])
        input2_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 1))
        input3_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[2])
        input3_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 2))
        input4_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[3])
        input4_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 3))
        input5_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_dec[4])
        input5_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 4))
        input6_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_dec[5])
        input6_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 5))
        input7_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[6])
        input7_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 6))
        input8_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[7])
        input8_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 7))

        grid4_coord_dec = QGridLayout()
        grid4_coord_dec.addWidget(label1_coord_dec, 0, 0)
        grid4_coord_dec.addWidget(label2_coord_dec, 0, 1)
        grid4_coord_dec.addWidget(label3_coord_dec, 0, 2)
        grid4_coord_dec.addWidget(label4_coord_dec, 0, 3)
        grid4_coord_dec.addWidget(input1_coord_dec, 1, 0)
        grid4_coord_dec.addWidget(input2_coord_dec, 1, 1)
        grid4_coord_dec.addWidget(input3_coord_dec, 1, 2)
        grid4_coord_dec.addWidget(input4_coord_dec, 1, 3)

        grid4_coord_dec.addWidget(label5_coord_dec, 2, 0)
        grid4_coord_dec.addWidget(label6_coord_dec, 2, 1)
        grid4_coord_dec.addWidget(label7_coord_dec, 2, 2)
        grid4_coord_dec.addWidget(label8_coord_dec, 2, 3)
        grid4_coord_dec.addWidget(input5_coord_dec, 3, 0)
        grid4_coord_dec.addWidget(input6_coord_dec, 3, 1)
        grid4_coord_dec.addWidget(input7_coord_dec, 3, 2)
        grid4_coord_dec.addWidget(input8_coord_dec, 3, 3)

        self.w4_coord_dec.setLayout(grid4_coord_dec)
        self.w4_coord_dec.setWindowTitle("Ограничение по координатам Декарт")
        self.w4_coord_dec.show()

    def show4_change_coord_dec(self, change, key):
        self.data['coord_dec'][key] = change

    def show4_select_param_cil(self, checked):
        self.w4_param_cil = QWidget()
        self.w4_param_cil.setFixedSize(500, 180)

        label1_param_cil = QLabel('Момент 1-го звена')
        label2_param_cil = QLabel('Момент 2-го звена')
        label3_param_cil = QLabel('Момент 3-го звена')
        label4_param_cil = QLabel('Длина 1-го звена')
        label5_param_cil = QLabel('Длина 2-го звена')
        label6_param_cil = QLabel('Расстояние')
        label7_param_cil = QLabel('Масса 2-го звена')
        label8_param_cil = QLabel('Масса 3-го звена')

        param_cil = self.data['param_cil']
        input1_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[0])
        input1_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 0))
        input2_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[1])
        input2_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 1))
        input3_param_cil = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = param_cil[2])
        input3_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 2))
        input4_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[3])
        input4_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 3))
        input5_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[4])
        input5_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 4))
        input6_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[5])
        input6_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 5))
        input7_param_cil = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_cil[6])
        input7_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 6))
        input8_param_cil = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_cil[7])
        input8_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 7))

        grid4_param_cil = QGridLayout()
        grid4_param_cil.addWidget(label1_param_cil, 0, 0)
        grid4_param_cil.addWidget(label2_param_cil, 0, 1)
        grid4_param_cil.addWidget(label3_param_cil, 0, 2)
        grid4_param_cil.addWidget(label4_param_cil, 0, 3)
        grid4_param_cil.addWidget(input1_param_cil, 1, 0)
        grid4_param_cil.addWidget(input2_param_cil, 1, 1)
        grid4_param_cil.addWidget(input3_param_cil, 1, 2)
        grid4_param_cil.addWidget(input4_param_cil, 1, 3)

        grid4_param_cil.addWidget(label5_param_cil, 2, 0)
        grid4_param_cil.addWidget(label6_param_cil, 2, 1)
        grid4_param_cil.addWidget(label7_param_cil, 2, 2)
        grid4_param_cil.addWidget(label8_param_cil, 2, 3)
        grid4_param_cil.addWidget(input5_param_cil, 3, 0)
        grid4_param_cil.addWidget(input6_param_cil, 3, 1)
        grid4_param_cil.addWidget(input7_param_cil, 3, 2)
        grid4_param_cil.addWidget(input8_param_cil, 3, 3)

        self.w4_param_cil.setLayout(grid4_param_cil)
        self.w4_param_cil.setWindowTitle("Конструктивные параметры Цилиндр")
        self.w4_param_cil.show()

    def show4_change_param_cil(self, change, key):
        self.data['param_cil'][key] = change

    def show4_select_coord_cil(self, checked):
        self.w4_coord_cil = QWidget()
        self.w4_coord_cil.setFixedSize(500, 150)

        label1_coord_cil = QLabel('Q1min')
        label2_coord_cil = QLabel('Q1max')
        label3_coord_cil = QLabel('A2min')
        label4_coord_cil = QLabel('A2max')
        label5_coord_cil = QLabel('Q3min')
        label6_coord_cil = QLabel('Q3max')
        label7_coord_cil = QLabel('Zmin')
        label8_coord_cil = QLabel('Zmax')

        coord_cil = self.data['coord_cil']
        input1_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[0])
        input1_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 0))
        input2_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[1])
        input2_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 1))
        input3_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_cil[2])
        input3_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 2))
        input4_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001,  maximum=1, minimum=0, value=coord_cil[3])
        input4_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 3))
        input5_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[4])
        input5_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 4))
        input6_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[5])
        input6_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 5))
        input7_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_cil[6])
        input7_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 6))
        input8_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_cil[7])
        input8_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 7))

        grid4_coord_cil = QGridLayout()
        grid4_coord_cil.addWidget(label1_coord_cil, 0, 0)
        grid4_coord_cil.addWidget(label2_coord_cil, 0, 1)
        grid4_coord_cil.addWidget(label3_coord_cil, 0, 2)
        grid4_coord_cil.addWidget(label4_coord_cil, 0, 3)
        grid4_coord_cil.addWidget(input1_coord_cil, 1, 0)
        grid4_coord_cil.addWidget(input2_coord_cil, 1, 1)
        grid4_coord_cil.addWidget(input3_coord_cil, 1, 2)
        grid4_coord_cil.addWidget(input4_coord_cil, 1, 3)

        grid4_coord_cil.addWidget(label5_coord_cil, 2, 0)
        grid4_coord_cil.addWidget(label6_coord_cil, 2, 1)
        grid4_coord_cil.addWidget(label7_coord_cil, 2, 2)
        grid4_coord_cil.addWidget(label8_coord_cil, 2, 3)
        grid4_coord_cil.addWidget(input5_coord_cil, 3, 0)
        grid4_coord_cil.addWidget(input6_coord_cil, 3, 1)
        grid4_coord_cil.addWidget(input7_coord_cil, 3, 2)
        grid4_coord_cil.addWidget(input8_coord_cil, 3, 3)

        self.w4_coord_cil.setLayout(grid4_coord_cil)
        self.w4_coord_cil.setWindowTitle("Ограничение по координатам Цилиндр")
        self.w4_coord_cil.show()

    def show4_change_coord_cil(self, change, key):
        self.data['coord_cil'][key] = change

    def show4_select_param_scr(self, checked):
        self.w4_param_scr = QWidget()
        self.w4_param_scr.setFixedSize(500, 180)

        label1_param_scr = QLabel('Момент 1-го звена')
        label2_param_scr = QLabel('Момент 2-го звена')
        label3_param_scr = QLabel('Момент 3-го звена')
        label4_param_scr = QLabel('Длина 1-го звена')
        label5_param_scr = QLabel('Длина 2-го звена')
        label6_param_scr = QLabel('Расстояние')
        label7_param_scr = QLabel('Масса 2-го звена')
        label8_param_scr = QLabel('Масса 3-го звена')

        param_scr = self.data['param_scr']
        input1_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[0])
        input1_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 0))
        input2_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[1])
        input2_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 1))
        input3_param_scr = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = param_scr[2])
        input3_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 2))
        input4_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[3])
        input4_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 3))
        input5_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[4])
        input5_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 4))
        input6_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[5])
        input6_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 5))
        input7_param_scr = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_scr[6])
        input7_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 6))
        input8_param_scr = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_scr[7])
        input8_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 7))

        grid4_param_scr = QGridLayout()
        grid4_param_scr.addWidget(label1_param_scr, 0, 0)
        grid4_param_scr.addWidget(label2_param_scr, 0, 1)
        grid4_param_scr.addWidget(label3_param_scr, 0, 2)
        grid4_param_scr.addWidget(label4_param_scr, 0, 3)
        grid4_param_scr.addWidget(input1_param_scr, 1, 0)
        grid4_param_scr.addWidget(input2_param_scr, 1, 1)
        grid4_param_scr.addWidget(input3_param_scr, 1, 2)
        grid4_param_scr.addWidget(input4_param_scr, 1, 3)

        grid4_param_scr.addWidget(label5_param_scr, 2, 0)
        grid4_param_scr.addWidget(label6_param_scr, 2, 1)
        grid4_param_scr.addWidget(label7_param_scr, 2, 2)
        grid4_param_scr.addWidget(label8_param_scr, 2, 3)
        grid4_param_scr.addWidget(input5_param_scr, 3, 0)
        grid4_param_scr.addWidget(input6_param_scr, 3, 1)
        grid4_param_scr.addWidget(input7_param_scr, 3, 2)
        grid4_param_scr.addWidget(input8_param_scr, 3, 3)

        self.w4_param_scr.setLayout(grid4_param_scr)
        self.w4_param_scr.setWindowTitle("Конструктивные параметры Скара")
        self.w4_param_scr.show()

    def show4_change_param_scr(self, change, key):
        self.data['param_scr'][key] = change

    def show4_select_coord_scr(self, checked):
        self.w4_coord_scr = QWidget()
        self.w4_coord_scr.setFixedSize(500, 150)

        label1_coord_scr = QLabel('Q1min')
        label2_coord_scr = QLabel('Q1max')
        label3_coord_scr = QLabel('Q2min')
        label4_coord_scr = QLabel('Q2max')
        label5_coord_scr = QLabel('Q3min')
        label6_coord_scr = QLabel('Q3max')
        label7_coord_scr = QLabel('Zmin')
        label8_coord_scr = QLabel('Zmax')

        coord_scr = self.data['coord_scr']
        input1_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[0])
        input1_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 0))
        input2_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[1])
        input2_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 1))
        input3_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[2])
        input3_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 2))
        input4_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[3])
        input4_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 3))
        input5_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=6.280, minimum=-6.280, value=coord_scr[4])
        input5_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 4))
        input6_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=6.280, minimum=-6.280, value=coord_scr[5])
        input6_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 5))
        input7_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_scr[6])
        input7_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 6))
        input8_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_scr[7])
        input8_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 7))

        grid4_coord_scr = QGridLayout()
        grid4_coord_scr.addWidget(label1_coord_scr, 0, 0)
        grid4_coord_scr.addWidget(label2_coord_scr, 0, 1)
        grid4_coord_scr.addWidget(label3_coord_scr, 0, 2)
        grid4_coord_scr.addWidget(label4_coord_scr, 0, 3)
        grid4_coord_scr.addWidget(input1_coord_scr, 1, 0)
        grid4_coord_scr.addWidget(input2_coord_scr, 1, 1)
        grid4_coord_scr.addWidget(input3_coord_scr, 1, 2)
        grid4_coord_scr.addWidget(input4_coord_scr, 1, 3)

        grid4_coord_scr.addWidget(label5_coord_scr, 2, 0)
        grid4_coord_scr.addWidget(label6_coord_scr, 2, 1)
        grid4_coord_scr.addWidget(label7_coord_scr, 2, 2)
        grid4_coord_scr.addWidget(label8_coord_scr, 2, 3)
        grid4_coord_scr.addWidget(input5_coord_scr, 3, 0)
        grid4_coord_scr.addWidget(input6_coord_scr, 3, 1)
        grid4_coord_scr.addWidget(input7_coord_scr, 3, 2)
        grid4_coord_scr.addWidget(input8_coord_scr, 3, 3)

        self.w4_coord_scr.setLayout(grid4_coord_scr)
        self.w4_coord_scr.setWindowTitle("Ограничение по координатам Скара")
        self.w4_coord_scr.show()

    def show4_change_coord_scr(self, change, key):
        self.data['coord_scr'][key] = change

    def show4_select_engine(self, checked):
        self.w4_engine = QWidget()
        self.w4_engine.setFixedSize(500, 280)

        label1_eng = QLabel('J1')
        label2_eng = QLabel('J2')
        label3_eng = QLabel('J3')
        label4_eng = QLabel('J4')
        label5_eng = QLabel('n1')
        label6_eng = QLabel('n2')
        label7_eng = QLabel('n3')
        label8_eng = QLabel('n4')
        label9_eng = QLabel('U1max')
        label10_eng = QLabel('U2max')
        label11_eng = QLabel('U3max')
        label12_eng = QLabel('U4max')
        label13_eng = QLabel('Ku1')
        label14_eng = QLabel('Ku2')
        label15_eng = QLabel('Ku3')
        label16_eng = QLabel('Ku4')
        label17_eng = QLabel('Kq1')
        label18_eng = QLabel('Kq2')
        label19_eng = QLabel('Kq3')
        label20_eng = QLabel('Kq4')

        eng = self.data['engine']
        input1_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[0])
        input1_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 0))
        input2_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[1])
        input2_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 1))
        input3_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[2])
        input3_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 2))
        input4_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[3])
        input4_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 3))
        input5_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[4])
        input5_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 4))
        input6_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[5])
        input6_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 5))
        input7_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[6])
        input7_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 6))
        input8_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[7])
        input8_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 7))
        input9_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[8])
        input9_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 8))
        input10_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[9])
        input10_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 9))
        input11_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[10])
        input11_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 10))
        input12_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[11])
        input12_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 11))
        input13_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[12])
        input13_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 12))
        input14_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[13])
        input14_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 13))
        input15_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[14])
        input15_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 14))
        input16_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[15])
        input16_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 15))
        input17_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[16])
        input17_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 16))
        input18_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[17])
        input18_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 17))
        input19_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[18])
        input19_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 18))
        input20_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[19])
        input20_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 19))

        grid4_eng = QGridLayout()
        grid4_eng.addWidget(label1_eng, 0, 0)
        grid4_eng.addWidget(label2_eng, 0, 1)
        grid4_eng.addWidget(label3_eng, 0, 2)
        grid4_eng.addWidget(label4_eng, 0, 3)
        grid4_eng.addWidget(input1_eng, 1, 0)
        grid4_eng.addWidget(input2_eng, 1, 1)
        grid4_eng.addWidget(input3_eng, 1, 2)
        grid4_eng.addWidget(input4_eng, 1, 3)

        grid4_eng.addWidget(label5_eng, 2, 0)
        grid4_eng.addWidget(label6_eng, 2, 1)
        grid4_eng.addWidget(label7_eng, 2, 2)
        grid4_eng.addWidget(label8_eng, 2, 3)
        grid4_eng.addWidget(input5_eng, 3, 0)
        grid4_eng.addWidget(input6_eng, 3, 1)
        grid4_eng.addWidget(input7_eng, 3, 2)
        grid4_eng.addWidget(input8_eng, 3, 3)

        grid4_eng.addWidget(label9_eng, 4, 0)
        grid4_eng.addWidget(label10_eng, 4, 1)
        grid4_eng.addWidget(label11_eng, 4, 2)
        grid4_eng.addWidget(label12_eng, 4, 3)
        grid4_eng.addWidget(input9_eng, 5, 0)
        grid4_eng.addWidget(input10_eng, 5, 1)
        grid4_eng.addWidget(input11_eng, 5, 2)
        grid4_eng.addWidget(input12_eng, 5, 3)

        grid4_eng.addWidget(label13_eng, 6, 0)
        grid4_eng.addWidget(label14_eng, 6, 1)
        grid4_eng.addWidget(label15_eng, 6, 2)
        grid4_eng.addWidget(label16_eng, 6, 3)
        grid4_eng.addWidget(input13_eng, 7, 0)
        grid4_eng.addWidget(input14_eng, 7, 1)
        grid4_eng.addWidget(input15_eng, 7, 2)
        grid4_eng.addWidget(input16_eng, 7, 3)

        grid4_eng.addWidget(label17_eng, 8, 0)
        grid4_eng.addWidget(label18_eng, 8, 1)
        grid4_eng.addWidget(label19_eng, 8, 2)
        grid4_eng.addWidget(label20_eng, 8, 3)
        grid4_eng.addWidget(input17_eng, 9, 0)
        grid4_eng.addWidget(input18_eng, 9, 1)
        grid4_eng.addWidget(input19_eng, 9, 2)
        grid4_eng.addWidget(input20_eng, 9, 3)

        self.w4_engine.setLayout(grid4_eng)
        self.w4_engine.setWindowTitle("Параметры двигателей")
        self.w4_engine.show()

    def show4_change_eng(self, change, key):
        self.data['engine'][key] = change

    def show4_select_reg(self, checked):
        self.w4_reg = QWidget()
        self.w4_reg.setFixedSize(500, 200)

        label1_reg = QLabel('Кп1')
        label2_reg = QLabel('Кп2')
        label3_reg = QLabel('Кп3')
        label4_reg = QLabel('Кп4')
        label5_reg = QLabel('Ки1')
        label6_reg = QLabel('Ки2')
        label7_reg = QLabel('Ки3')
        label8_reg = QLabel('Ки4')
        label9_reg = QLabel('Кд1')
        label10_reg = QLabel('Кд2')
        label11_reg = QLabel('Кд3')
        label12_reg = QLabel('Кд4')

        reg = self.data['reg']
        input1_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[0])
        input1_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 0))
        input2_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[1])
        input2_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 1))
        input3_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[2])
        input3_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 2))
        input4_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[3])
        input4_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 3))
        input5_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[4])
        input5_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 4))
        input6_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[5])
        input6_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 5))
        input7_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[6])
        input7_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 6))
        input8_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[7])
        input8_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 7))
        input9_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[8])
        input9_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 8))
        input10_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[9])
        input10_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 9))
        input11_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[10])
        input11_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 10))
        input12_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[11])
        input12_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 11))

        grid4_reg = QGridLayout()
        grid4_reg.addWidget(label1_reg, 0, 0)
        grid4_reg.addWidget(label2_reg, 0, 1)
        grid4_reg.addWidget(label3_reg, 0, 2)
        grid4_reg.addWidget(label4_reg, 0, 3)
        grid4_reg.addWidget(input1_reg, 1, 0)
        grid4_reg.addWidget(input2_reg, 1, 1)
        grid4_reg.addWidget(input3_reg, 1, 2)
        grid4_reg.addWidget(input4_reg, 1, 3)

        grid4_reg.addWidget(label5_reg, 2, 0)
        grid4_reg.addWidget(label6_reg, 2, 1)
        grid4_reg.addWidget(label7_reg, 2, 2)
        grid4_reg.addWidget(label8_reg, 2, 3)
        grid4_reg.addWidget(input5_reg, 3, 0)
        grid4_reg.addWidget(input6_reg, 3, 1)
        grid4_reg.addWidget(input7_reg, 3, 2)
        grid4_reg.addWidget(input8_reg, 3, 3)

        grid4_reg.addWidget(label9_reg, 4, 0)
        grid4_reg.addWidget(label10_reg, 4, 1)
        grid4_reg.addWidget(label11_reg, 4, 2)
        grid4_reg.addWidget(label12_reg, 4, 3)
        grid4_reg.addWidget(input9_reg, 5, 0)
        grid4_reg.addWidget(input10_reg, 5, 1)
        grid4_reg.addWidget(input11_reg, 5, 2)
        grid4_reg.addWidget(input12_reg, 5, 3)

        self.w4_reg.setLayout(grid4_reg)
        self.w4_reg.setWindowTitle("Параметры регуляторов")
        self.w4_reg.show()

    def show4_change_reg(self, change, key):
        self.data['reg'][key] = change

    def show4_select_calc(self, checked):
        self.w4_calc = QWidget()
        self.w4_calc.setFixedSize(500, 100)

        label1_calc = QLabel('Разрядность')
        label2_calc = QLabel('Такт управления')
        label3_calc = QLabel('Такт обмена')
        label4_calc = QLabel('Постоянная фильтра')

        calc = self.data['calc']
        input1_calc = QDoubleSpinBox(maximum = 32, minimum = 2, value = calc[0])
        input1_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 0))
        input2_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[1])
        input2_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 1))
        input3_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[2])
        input3_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 2))
        input4_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[3])
        input4_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 3))

        grid4_calc = QGridLayout()
        grid4_calc.addWidget(label1_calc, 0, 0)
        grid4_calc.addWidget(label2_calc, 0, 1)
        grid4_calc.addWidget(label3_calc, 0, 2)
        grid4_calc.addWidget(label4_calc, 0, 3)
        grid4_calc.addWidget(input1_calc, 1, 0)
        grid4_calc.addWidget(input2_calc, 1, 1)
        grid4_calc.addWidget(input3_calc, 1, 2)
        grid4_calc.addWidget(input4_calc, 1, 3)

        self.w4_calc.setLayout(grid4_calc)
        self.w4_calc.setWindowTitle("Параметры вычислителей")
        self.w4_calc.show()

    def show4_change_calc(self, change, key):
        self.data['calc'][key] = change

    def show4_select_pos_move(self, checked):
        self.w4_pos_move = QWidget()
        self.w4_pos_move.setFixedSize(800, 300)

        labels = ['t', 'q1', 'q2', 'q3', 'q4']
        pos_move_dict = {
            't': 100,
            'q1': 300,
            'q2': 300,
            'q3': 400,
            'q4': 400
        }

        grid4_pos_move = QGridLayout()
        for row, label in enumerate(labels):
            value_label = QLabel(label)
            grid4_pos_move.addWidget(value_label, row, 0)
            for col in range(9):
                params = {
                    'decimals': 2,
                    'value': self.data['ciclogram'][row][col],
                    'minimum': -pos_move_dict[label],
                    'maximum': pos_move_dict[label]
                }
                sp_box = MySpinBox([row, col], params)
                sp_box.valueChanged.connect(self.show4_get_pos_values)
                grid4_pos_move.addWidget(sp_box, row, col + 1)

        self.w4_pos_move.setLayout(grid4_pos_move)
        self.w4_pos_move.setWindowTitle('Циклограмма')
        self.w4_pos_move.show()

    def show4_get_pos_values(self, change):
        row, col = self.sender().ind
        self.data['ciclogram'][row][col] = change

    def show4_select_cont_line(self, checked):
        self.w4_cont_line = QWidget()
        self.w4_cont_line.setFixedSize(500, 100)
        show_graph_line = QPushButton('Показать')
        show_graph_line.clicked.connect(self.show4_set_line_workspace)

        label1_cont_line = QLabel('x1')
        label2_cont_line = QLabel('x2')
        label3_cont_line = QLabel('y1')
        label4_cont_line = QLabel('y2')
        label5_cont_line = QLabel('Скорость')

        line = self.data['line']
        input1_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[0])
        input1_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 0))
        input2_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[1])
        input2_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 1))
        input3_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[2])
        input3_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 2))
        input4_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[3])
        input4_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 3))
        input5_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[4])
        input5_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 4))

        grid4_cont_line = QGridLayout()
        grid4_cont_line.addWidget(label1_cont_line, 0, 0)
        grid4_cont_line.addWidget(label2_cont_line, 0, 1)
        grid4_cont_line.addWidget(label3_cont_line, 0, 2)
        grid4_cont_line.addWidget(label4_cont_line, 0, 3)
        grid4_cont_line.addWidget(label5_cont_line, 0, 4)
        grid4_cont_line.addWidget(input1_cont_line, 1, 0)
        grid4_cont_line.addWidget(input2_cont_line, 1, 1)
        grid4_cont_line.addWidget(input3_cont_line, 1, 2)
        grid4_cont_line.addWidget(input4_cont_line, 1, 3)
        grid4_cont_line.addWidget(input5_cont_line, 1, 4)
        grid4_cont_line.addWidget(show_graph_line, 2, 4)

        self.w4_cont_line.setLayout(grid4_cont_line)
        self.w4_cont_line.setWindowTitle("Прямая")
        self.w4_cont_line.show()

    def show4_change_line(self, change, key):
        self.data['line'][key] = change

    def show4_set_line_workspace(self):
        self.data['line_or_circle'] = 'line'
        self.w4_cont_line.close()

    def show4_select_cont_circle(self, checked):
        self.w4_cont_circle = QWidget()
        self.w4_cont_circle.setFixedSize(400, 100)
        show_graph_circle = QPushButton('Показать')
        show_graph_circle.clicked.connect(self.show4_set_circle_workspace)

        label1_cont_circle = QLabel('x')
        label2_cont_circle = QLabel('y')
        label3_cont_circle = QLabel('r')
        label4_cont_circle = QLabel('Скорость')

        circle = self.data['circle']
        input1_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[0])
        input1_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 0))
        input2_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[1])
        input2_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 1))
        input3_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[2])
        input3_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 2))
        input4_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[3])
        input4_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 3))

        grid4_cont_circle = QGridLayout()
        grid4_cont_circle.addWidget(label1_cont_circle, 0, 0)
        grid4_cont_circle.addWidget(label2_cont_circle, 0, 1)
        grid4_cont_circle.addWidget(label3_cont_circle, 0, 2)
        grid4_cont_circle.addWidget(label4_cont_circle, 0, 3)
        grid4_cont_circle.addWidget(input1_cont_circle, 1, 0)
        grid4_cont_circle.addWidget(input2_cont_circle, 1, 1)
        grid4_cont_circle.addWidget(input3_cont_circle, 1, 2)
        grid4_cont_circle.addWidget(input4_cont_circle, 1, 3)
        grid4_cont_circle.addWidget(show_graph_circle, 2, 3)

        self.w4_cont_circle.setLayout(grid4_cont_circle)
        self.w4_cont_circle.setWindowTitle("Окружность")
        self.w4_cont_circle.show()

    def show4_change_circle(self, change, key):
        self.data['circle'][key] = change

    def show4_set_circle_workspace(self):
        self.data['line_or_circle'] = 'circle'
        self.w4_cont_circle.close()

    def show5_workspace(self):
        if self.data['robotype'] == 'Декарт':
            self.my_plot = QWidget()
            self.my_plot.setWindowTitle(f'Рабочая область: {self.data["robotype"]}')
            self.my_plot.setFixedSize(600, 600)
            layout = QVBoxLayout(self.my_plot)
            x_ticks = np.linspace(-1, 1, 11)
            y_ticks = np.linspace(0, 2, 11)

            static_canvas = FigureCanvas(Figure(figsize=(12, 8)))

            layout.addWidget(static_canvas)

            sns.set_style('whitegrid')
            self._static_ax = static_canvas.figure.subplots()
            self._static_ax.plot()
            self._static_ax.set_xlim([-1, 1])
            self._static_ax.set_ylim([0, 2])
            self._static_ax.set_xticks(x_ticks)
            self._static_ax.set_yticks(y_ticks)
            self._static_ax.fill_between([0, 1], [0, 0], [1, 1], color='C0', alpha=0.3)

        elif self.data['robotype'] == 'Цилиндр':
            self.my_plot = QWidget()
            self.my_plot.setWindowTitle(f'Рабочая область: {self.data["robotype"]}')
            self.my_plot.setFixedSize(600, 600)
            layout = QVBoxLayout(self.my_plot)
            x_ticks = np.linspace(-1, 1, 11)
            y_ticks = np.linspace(0, 2, 11)

            static_canvas = FigureCanvas(Figure(figsize=(12, 8)))

            layout.addWidget(static_canvas)

            sns.set_style('whitegrid')
            self._static_ax = static_canvas.figure.subplots()
            self._static_ax.plot()
            self._static_ax.set_xlim([-1, 1])
            self._static_ax.set_ylim([0, 2])

        elif self.data['robotype'] == 'Скара':
            self.my_plot = QWidget()
            self.my_plot.setWindowTitle(f'Рабочая область: {self.data["robotype"]}')
            self.my_plot.setFixedSize(600, 600)
            layout = QVBoxLayout(self.my_plot)
            x_ticks = np.linspace(-1, 1, 11)
            y_ticks = np.linspace(0, 2, 11)

            static_canvas = FigureCanvas(Figure(figsize=(12, 8)))

            layout.addWidget(static_canvas)

            sns.set_style('whitegrid')
            self._static_ax = static_canvas.figure.subplots()
            self._static_ax.plot()
            self._static_ax.set_xlim([-1, 1])
            self._static_ax.set_ylim([0, 2])

        if self.data['movetype'] == 'Контурное':
            if self.data['line_or_circle'] == 'circle':
                x, y, r = self.data['circle'][:3]
                circle = Circle((x, y), r, fill=False, edgecolor='green')
                self._static_ax.add_patch(circle)
        self.my_plot.show()

app = QApplication(sys.argv)
window = OpenWindow()
window.show()
app.exec()