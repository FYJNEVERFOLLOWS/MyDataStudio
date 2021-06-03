from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem
from PyQt5 import QtWidgets, QtCore
import sys

# items = ['Python', 'R', 'Java', 'C++', 'CSS']
items = ['FH1', 'FH2', 'FH3', 'FH5', 'FH9', 'FH10', 'HT1', 'HT2', 'HT3', 'HT5', 'HT6', 'HT7', 'LH1', 'LH2', 'LH3', 'ZS1']

class ComboCheckBox(QComboBox):
    def __init__(self, parent, items):  # items==[str,str...]
        super(ComboCheckBox, self).__init__(parent)
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)

        ############ 设置字体区 ############
        self.qLineEdit.setFont(QFont('宋体', 12))
        self.qListWidget.setFont(QFont('宋体', 12))
        self.setFont(QFont('宋体', 12))
        self.setFont(QFont('宋体', 12))
        self.setFont(QFont('宋体', 12))
        self.setFont(QFont('宋体', 12))

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])
        self.qCheckBox[i].setFont(QFont('宋体', 12))

    def getCheckItems(self):
        checkedItems = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                checkedItems.append(self.qCheckBox[i].text())
        self.selectedrow_num = len(checkedItems)
        return checkedItems

    def show(self):
        show = ''
        Outputlist = self.getCheckItems()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in Outputlist:
            show += i + ';'
        if self.selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def All(self, state):
        if state == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif state == 1:
            if self.selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif state == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    comboBox1 = ComboCheckBox(Form, items)
    comboBox1.setGeometry(QtCore.QRect(10, 10, 100, 20))
    comboBox1.setMinimumSize(QtCore.QSize(100, 20))
    # comboBox1.loadItems(items)

    Form.show()
    sys.exit(app.exec_())


