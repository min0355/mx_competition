# 13 번 수정하는 파일임 (kym)


import os
import re
import sys

import pandas as pd

from PySide6.QtCore import Qt, QCoreApplication, QItemSelectionModel
from PySide6.QtWidgets import (QApplication, QFileDialog, QHeaderView, QHBoxLayout, 
                               QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                               QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
                               QDialog, QDialogButtonBox, QFormLayout, QLabel, QVBoxLayout, 
                               QLineEdit, QLabel, QTabWidget, QMessageBox)
from PySide6.QtGui import QColor
from PySide6 import QtGui
import string

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)



'''
TO DO LIST 

1. ape 삭제 -> 완료 
2. 실행 시 전체 창, 품번이 다 보이는 열 너비로 default 세팅 -> 완료 
3. 프로그램 실행 창 제목 입력 -> 완료
4. 삭제 품번 체크 반영되도록 수정 -> 완료 
5. 품번, PREFIX, 수량, 단위는 정확히 입력 필요하고 품명은 대충 넣어도 되도록 -> bom 완성도를 위해선 정확히 넣는걸로
6. 엑셀 저장 -> 완료
7. 버튼 순서 및 이름 수정 ->  완료
8. excel save 시 parent 정보 추가 -> 완료
9. 최종 테이블 화면 색상 표시 (추가, 변경) -> 완료
10. PARENT 가 무첨자일때 A 로 변경 되지 않는 문제 -> 완료
15. LP 소개 추가 -> 완료 (간단히 LP 명만 기재)
12. 상단 버튼 최종 정리 (버튼 종류별로 색상 구분되면 편할 듯, 서치 버튼 좀 더 넓게 => 완료)  



11. EXE 파일로 만드는 방법 (PYTHON 미 설치에도 쓸 수 있도록) -> 김영진 매니저  



13. 첨자가 설변 품번 개수만큼 올라가는 것 수정 (신규 품번 추가 + 설변 품번, 삭제 품번 모두 첨자는 1 번만 변경되어야 함.)
14. 11 자리 품번 외엔 PARENT 자동 첨자 변경이 되지 않음  
16. 정규식 추가 (품번 잘못 입력 시 알림 창) -> 알림 이 후 다시 창이 뜨도록 수정 필요, 정규식 촘촘히 채울 것  
17. 상단 버튼 tap 
18. 생성해야 할 품번 리스트 별도 출력 (확인용) -> 새 창으로 출력 되나 품번이 중복되거나 오류 첨자로 표기되는 등의 문제가 있음. 굳이 필요한지? 
19. 삭제, 삽입 된 행도 고려하여 저장된 엑셀 파일을 그대로 복붙 할 수 있도록 최종 저장 BOM 구성
20. FLAG 기입  
21. 리턴 버튼 추가

'''

def tree_to_dataframe(tree_widget):
    data = []
    
    def visit_node(node, parent=None, level=0):
        if parent is not None:
            row = [level, parent]
            row.append(node.text(1))  # Add PREFIX

            # Add text and background color for each column
            for j in range(tree_widget.columnCount()):
                bg_color = node.background(j).color()
                if bg_color.isValid():  # Check if the background color is valid
                    if bg_color == QColor.fromRgbF(0, 0, 0, 1):  # Check if the background color is black
                        row.append({'text': node.text(j), 'bg_color': Qt.white})  # Use white as the background color
                    else:
                        row.append({'text': node.text(j), 'bg_color': bg_color})
                else:
                    row.append({'text': node.text(j), 'bg_color': Qt.white})  # Use white as the default background color
                
            row.pop(4)  # Remove CLASS for ITM
            data.append(row)

        for i in range(node.childCount()):
            visit_node(node.child(i), node.text(0), level + 1)

    for i in range(tree_widget.topLevelItemCount()):
        item = tree_widget.topLevelItem(i)
        visit_node(item)

    columns = ["LVL", "PARENT", "PREFIX", "ITM", "ITM_DESC", "QTY", "UOM", "SRC", "PROC", "THREAD"]
    df = pd.DataFrame(data, columns=columns)
    return df

# class MyTreeWidgetItem(QTreeWidgetItem):
#     def __init__(self, parent=None):
#         super(MyTreeWidgetItem, self).__init__(parent)

class MyTreeWidget(QTreeWidget):
     
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)

        self.setHeaderLabels(["CLASS", "PREFIX", "ITM_DESC", "QTY", "UOM", "SRC", "PROC", "THREAD"])
        self.setAlternatingRowColors(True)
        self.header().setSectionResizeMode(QHeaderView.Interactive)
        self.itemClicked.connect(self.item_clicked)

    def do_search(self, term):
        clist = self.findItems(term, Qt.MatchContains | Qt.MatchRecursive)

        sel = self.selectionModel()
        for item in clist:
            index = self.indexFromItem(item)
            sel.select(index, QItemSelectionModel.Select)
        
    def set_item_background_color(self, item, color):
        for i in range(self.columnCount()):
            item.setBackground(i, color)

    def item_clicked(self, item, column):
       self.parent().load_item_properties(item)

class DataFrameDialog(QDialog):
    def __init__(self, parent=None):
        super(DataFrameDialog, self).__init__(parent)

        self.setWindowTitle('BOM Comparison')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)  # Add maximize button to the dialog

        self.left_table = QTableWidget()
        self.right_table = QTableWidget()

        layout = QVBoxLayout()

        # Create table title labels
        left_table_title = QLabel("OLD BOM")
        right_table_title = QLabel("NEW BOM")

        # Create a horizontal layout for table titles
        title_layout = QHBoxLayout()
        title_layout.addWidget(left_table_title)
        title_layout.addWidget(right_table_title)

        # Add the title layout to the main layout
        layout.addLayout(title_layout)

        table_layout = QHBoxLayout()
        table_layout.addWidget(self.left_table)
        table_layout.addWidget(self.right_table)
        layout.addLayout(table_layout)
        self.setLayout(layout)

    def show_dataframes(self, old_df, new_df):
        self.show_dataframe(self.left_table, old_df)
        self.show_dataframe(self.right_table, new_df)
        self.compare_and_highlight_differences(old_df, new_df)
        self.sync_table_scrollbars()
        self.show()

    def show_dataframe(self, table, df):
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                cell_data = df.iat[i, j]
                if isinstance(cell_data, dict):  # Check if cell_data is a dictionary
                    item = QTableWidgetItem(cell_data['text'])
                    item.setBackground(cell_data['bg_color'])
                else:
                    item = QTableWidgetItem(str(cell_data))                    
                table.setItem(i, j, item)

    def compare_and_highlight_differences(self, old_df, new_df):
        # Create a set of row labels for each dataframe
        old_row_labels = set(old_df.index)
        new_row_labels = set(new_df.index)

        # Find missing rows in old_df
        missing_rows = new_row_labels - old_row_labels

        # Insert missing rows into the old_df table with a blue background
        for row_label in missing_rows:
            new_row_index = new_df.index.get_loc(row_label)
            self.left_table.insertRow(new_row_index)
            for j in range(old_df.shape[1]):
                item = QTableWidgetItem("")
                item.setBackground(Qt.yellow)
                self.left_table.setItem(new_row_index, j, item)
                
    def sync_table_scrollbars(self):
        def sync_scrollbars(value):
            self.left_table.verticalScrollBar().setValue(value)
            self.right_table.verticalScrollBar().setValue(value)

        left_scrollbar = self.left_table.verticalScrollBar()
        right_scrollbar = self.right_table.verticalScrollBar()

        left_scrollbar.valueChanged.connect(sync_scrollbars)
        right_scrollbar.valueChanged.connect(sync_scrollbars)   

class AddRowDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        self.setWindowTitle("Add New Row")

        vbox = QVBoxLayout()

        form_layout = QFormLayout()
        self.class_edit = QLineEdit()
        self.prefix_edit = QLineEdit()
        self.itm_desc_edit = QLineEdit()
        self.qty_edit = QLineEdit()
        self.uom_edit = QLineEdit()

        form_layout.addRow("Class:", self.class_edit)
        form_layout.addRow("Prefix:", self.prefix_edit)
        form_layout.addRow("ITM_DESC:", self.itm_desc_edit)
        form_layout.addRow("QTY:", self.qty_edit)
        form_layout.addRow("UOM:", self.uom_edit)

        vbox.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        vbox.addWidget(button_box)

        self.setLayout(vbox)
    
    def show_alert(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("Alert")
        alert.setText(message)
        alert.exec()


    def add_error_check(self):
        error_messages = []
        # Class 입력 규칙 검사
        rule1 = r'^\d{6}-\d{5}[A-Za-z]?$|\d{6}-\d{5}[A-Za-z]?-(M|m)$'   #6자리 숫자 다음에 + '-'+ 5자리 숫자 + 첨자 + m(소재품번?)
        rule2 = r'^S\d{7}$'                                             #S + 7자리
        rule3 = r'^R\d{5,6}[a-zA-Z]?$'                                  #R + 5, 6자리 + 첨자
        if not re.match(rule1, self.class_edit.text()) and not re.match(rule2, self.class_edit.text()) and not re.match(rule3, self.class_edit.text()):
            error_messages.append('품번 입력 규칙에 맞지 않습니다.')
        # Prefix 입력 규칙 검사
        if not self.prefix_edit.text().isdigit() or len(self.prefix_edit.text()) != 4:
            error_messages.append('Prefix는 4자리 숫자만 입력 가능합니다.')
        # 수량 입력 규칙 검사
        if not self.qty_edit.text().isdigit():
            error_messages.append('수량은 숫자만 입력 가능합니다.')
        # 에러메시지
        error_message = '\n'.join(error_messages)
        # 알림창 띄우기
        if error_message:
            self.show_alert(error_message)



    def get_row_data(self):
        self.add_error_check() #에러체크
       
        return [self.class_edit.text(), self.prefix_edit.text(), self.itm_desc_edit.text(),
                self.qty_edit.text(), self.uom_edit.text()]
    
    # 추가한 부분 (위)

    def do_search(self, term):
        clist = self.findItems(term, Qt.MatchContains | Qt.MatchRecursive)

        sel = self.selectionModel()
        for item in clist:
            index = self.indexFromItem(item)
            sel.select(index, QItemSelectionModel.Select)
            
            
    def set_item_background_color(self, item, color):
        for i in range(self.columnCount()):
            item.setBackground(i, color)

    def item_clicked(self, item, column):
        self.parent().load_item_properties(item)

    # 추가한 부분 (아래)


class ItemNameInformer(QDialog):
    def __init__(self, oldnames, updatednames, parent=None):
        super().__init__(parent)
        
        self.oldnames = oldnames
        self.updatednames = updatednames
 
        self.setWindowTitle("Old & Updated Items")

        vbox1 = QVBoxLayout()
        
        for item in self.oldnames:
            item_label = QLabel(item)
            vbox1.addWidget(item_label)
            
        vbox2 = QVBoxLayout()

        for item in self.updatednames:
            item_label = QLabel(item)
            vbox2.addWidget(item_label)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        
        self.setLayout(hbox)
    
class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # V2 
        self.change_node_name_executed = False


        self.setWindowTitle("BOM 자동 생성기 (Made by Ars Machina)")
        # self.resize(500, 600)  # 위젯 사이즈
        
        self.df_list = []
        self.old_names = []
        self.updated_names = []

        open_btn = QPushButton('엑셀 파일 열기', self)
        tree_btn = QPushButton('Tree구조 보기', self)
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(100) 
        
        search_button = QPushButton("Search")
        transform_btn = QPushButton('Transform to Table', self)
          
        tree_move_up_btn = QPushButton('Move Up', self)
        tree_move_down_btn = QPushButton('Move Down', self)
        tree_del_btn = QPushButton('잘못 입력된 행 삭제', self)

        tree_add_btn = QPushButton('신규 품번 추가', self)
        remove_btn = QPushButton('삭제 품번 체크', self)      
        # color_alt_row_btn = QPushButton('설변 품번 체크', self)
        # color_row_btn = QPushButton('지울 품번 체크', self)  

        # 수평 박스 배치
        hbox = QHBoxLayout()
        hbox.addWidget(open_btn)
        hbox.addWidget(tree_btn)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(search_button)
        
        hbox.addWidget(tree_move_up_btn)
        hbox.addWidget(tree_move_down_btn)   
        # hbox.addWidget(color_alt_row_btn)
        # hbox.addWidget(color_row_btn)  
        
        hbox.addWidget(tree_del_btn)     

        hbox.addWidget(tree_add_btn)
        hbox.addWidget(remove_btn)
        hbox.addWidget(transform_btn)        
                
        self.table = QTableWidget(self)
        self.qtree = MyTreeWidget(self)

        TableTreeBox = QHBoxLayout()
        TableTreeBox.addWidget(self.table)
        TableTreeBox.addWidget(self.qtree)
 

        change_name_label = QLabel("Change Name:")
        self.old_name_edit = QLineEdit()
        self.new_name_edit = QLineEdit()
        self.old_name_edit.setFixedWidth(100)  
        self.new_name_edit.setFixedWidth(100)  
        self.change_name_button = QPushButton("Change Name")

        right_hbox = QHBoxLayout()
        right_hbox.addWidget(change_name_label)
        right_hbox.addWidget(self.old_name_edit)
        right_hbox.addWidget(self.new_name_edit)
        right_hbox.addWidget(self.change_name_button)

        self.property_labels = ["CLASS", "PREFIX", "ITM_DESC", "QTY", "UOM", "SRC", "PROC", "THREAD"]
        self.property_lineedits = [QLineEdit() for _ in range(len(self.property_labels))]
        properties_layout = QHBoxLayout()
        for label, lineedit in zip(self.property_labels, self.property_lineedits):
            properties_layout.addWidget(QLabel(label))
            properties_layout.addWidget(lineedit)

        self.save_properties_btn = QPushButton("Save Properties")
        self.save_properties_btn.clicked.connect(self.save_item_properties)
        properties_layout.addWidget(self.save_properties_btn)

        right_hbox.addLayout(properties_layout)
        
        # 수직 박스 배치
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(right_hbox)
        vbox.addLayout(TableTreeBox)
        
        self.setLayout(vbox)

        # 시그널 연결
        open_btn.clicked.connect(self.clickOpenBtn)
        tree_btn.clicked.connect(self.clickTreeBtn)
        search_button.clicked.connect(self.on_search_button_clicked)
        self.change_name_button.clicked.connect(self.on_change_name_button_clicked)
        
        tree_add_btn.clicked.connect(self.clickTreeAddBtn)
        tree_del_btn.clicked.connect(self.clickTreeDelBtn)
        tree_move_up_btn.clicked.connect(self.clickTreeMoveUpBtn)
        tree_move_down_btn.clicked.connect(self.clickTreeMoveDownBtn)
        
        # color_alt_row_btn.clicked.connect(self.clickColorAltRowBtn)
        # color_row_btn.clicked.connect(self.clickColorRowBtn)
        remove_btn.clicked.connect(self.clickRemoveBtn)
        transform_btn.clicked.connect(self.on_transform_button_clicked)

        # Change background color of buttons and input windows
        change_name_color = "background-color: #FDEBD0;"

        self.old_name_edit.setStyleSheet(change_name_color)
        self.new_name_edit.setStyleSheet(change_name_color)
        self.change_name_button.setStyleSheet(change_name_color)

        for lineedit in self.property_lineedits:
            lineedit.setStyleSheet(change_name_color)

        self.save_properties_btn.setStyleSheet(change_name_color)


    def clickTreeAddBtn(self):
        selected_item = self.qtree.currentItem()


        if not selected_item:
            return

        dialog = AddRowDialog(self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            new_item_data = dialog.get_row_data()
            new_item = QTreeWidgetItem(new_item_data)

            # Set the background color of the new item to yellow
            yellow_background = QColor(255, 255, 0)
            for i in range(new_item.columnCount()):
                new_item.setBackground(i, yellow_background)

            selected_item.parent().insertChild(selected_item.parent().indexOfChild(selected_item) + 1, new_item)


        new_item_data = ['', '', '', '', '']
        new_item = QTreeWidgetItem(new_item_data)
        # selected_item.addChild(new_item) 


        # V2 추가 
        if not self.change_node_name_executed:
            self.execute_change_node_name()


    # v2 추가 
    def execute_change_node_name(self, start_item=None):
        old_name = self.old_name_edit.text()
        new_name = self.new_name_edit.text()

        if start_item is None:
            start_item = self.qtree.invisibleRootItem()

        self.change_node_name(old_name, new_name)
        self.change_node_name_executed = True


    def clickTreeDelBtn(self):
        selected_items = self.qtree.selectedItems()
        for item in selected_items:
            item.parent().removeChild(item)

    def clickTreeMoveUpBtn(self):
        selected_item = self.qtree.currentItem()
        if not selected_item or not selected_item.parent():
            return

        parent = selected_item.parent()
        index = parent.indexOfChild(selected_item)
        if index == 0:
            return

        parent.removeChild(selected_item)
        parent.insertChild(index - 1, selected_item)
        self.qtree.setCurrentItem(selected_item)

    def clickTreeMoveDownBtn(self):
        selected_item = self.qtree.currentItem()
        if not selected_item or not selected_item.parent():
            return

        parent = selected_item.parent()
        index = parent.indexOfChild(selected_item)
        if index == parent.childCount() - 1:
            return

        parent.removeChild(selected_item)
        parent.insertChild(index + 1, selected_item)
        self.qtree.setCurrentItem(selected_item)

    def clickRemoveBtn(self):
        selected_items = self.qtree.selectedItems()
        gray_background = QColor(192, 192, 192)

        for item in selected_items:
            for i in range(item.columnCount()):
                item.setBackground(i, gray_background)
            
            # 추가 
            item.setData(0, Qt.UserRole, "deleted")

        # V2 추가 
        if not self.change_node_name_executed:
                self.execute_change_node_name()


    # def clickColorRowBtn(self):
    #     selected_items = self.qtree.selectedItems()
    #     gray_background = QColor(192, 192, 192)

    #     for item in selected_items:
    #         for i in range(item.columnCount()):
    #             item.setBackground(i, gray_background)


    # def clickColorAltRowBtn(self):
    #     selected_items = self.qtree.selectedItems()
    #     sky_blue_background = QColor(135, 206, 235)

    #     for item in selected_items:
    #         for i in range(item.columnCount()):
    #             item.setBackground(i, sky_blue_background)
                
    def on_transform_button_clicked(self):
        df = tree_to_dataframe(self.qtree)
        self.df_list.append(df)
        old_df = self.df_list[2]
        new_df = self.df_list[3]
        # self.show_dataframe_on_table(self.df_list[-1])
        self.show_dataframe_in_popup(old_df, new_df) 

        for column in new_df.columns:
            new_df[column] = new_df[column].apply(lambda x: x['text'] if isinstance(x, dict) and 'text' in x else x)

        self.save_dataframe_to_excel(new_df)    # 엑셀 신규 bom 만 저장 
        
        NamesInformer = ItemNameInformer(self.old_names, self.updated_names)
        NamesInformer.exec()

    def show_dataframe_in_popup(self, old_df, new_df):
        dialog = DataFrameDialog(self)
        dialog.show_dataframes(old_df, new_df)
        dialog.setGeometry(100, 100, 1200, 800)
        dialog.exec()

    # def show_dataframe_on_table(self, df):
    #     self.table.setRowCount(df.shape[0])
    #     self.table.setColumnCount(df.shape[1])
    #     self.table.setHorizontalHeaderLabels(df.columns)

    #     for i in range(df.shape[0]):
    #         for j in range(df.shape[1]):
    #             self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

    def load_item_properties(self, item):
        for i in range(len(self.property_labels)):
            self.property_lineedits[i].setText(item.text(i))
        self.current_item = item

    def save_item_properties(self):
        for i in range(len(self.property_labels)):
            self.current_item.setText(i, self.property_lineedits[i].text())


    def increment_last_alpha(self, s):
        last_alpha = s[-1]
        if last_alpha in string.ascii_uppercase:
            index = string.ascii_uppercase.index(last_alpha)
            if index + 1 < len(string.ascii_uppercase):
                if index == 7 or index == 14:
                    s = s[:-1] + string.ascii_uppercase[index + 2]
                else:
                    s = s[:-1] + string.ascii_uppercase[index + 1]
            else:
                self.show_alert('Z 이상의 첨자 품번을 생성할 수 없습니다.')
        # This part of the code checks if the last character of a string is a digit
        elif last_alpha.isdigit():
        # If it is a digit, then 'A' is added to the end of the string
            s += 'A'     
                                
        return s
    


    def find_nodes_by_name(self, parent_item, name):
        result = []

        if parent_item is None:
            parent_item = self.qtree.invisibleRootItem()

        for i in range(parent_item.childCount()):
            child_item = parent_item.child(i)
            if child_item.text(0) == name:
                result.append(child_item)
            result.extend(self.find_nodes_by_name(child_item, name))

        return result
        

    def change_node_name(self, old_name, new_name):
        # Find all items by old_name
        items = self.find_nodes_by_name(None, old_name)

        for item in items:
            # Update the item's name
            item.setText(0, new_name)

            # Change the background color to red
            self.qtree.set_item_background_color(item, QtGui.QColor("red"))

            # Change parent node names and background color
            self.old_names.append(old_name)
            self.updated_names.append(new_name)
            self.change_node_and_ancestors(item.parent())
                    
    def change_node_and_ancestors(self, item):
        if item is None:
            return

        # Change the node name
        old_name = item.text(0)
        new_name = self.increment_last_alpha(old_name)
        self.old_names.append(old_name)
        self.updated_names.append(new_name)

        # Update the item's name
        if ('620203-' not in old_name) and ('620205-' not in old_name):
            item.setText(0, new_name)
        
        # Change the background color to red
        self.qtree.set_item_background_color(item, QtGui.QColor("red"))

        # Move to the next parent
        self.change_node_and_ancestors(item.parent())  

    
    # def update_tree(self):
    #     self.qtree.clear()
    #     self.clickTreeBtn()

    # def update_table(self):
    #     self.table.clear()
    #     self.initTableWidget(2)  

    def on_change_name_button_clicked(self):
        print("Change name button clicked")

        # V2  
        if not self.change_node_name_executed:
            start_item = self.qtree.currentItem()
            self.execute_change_node_name(start_item)
            


    def clickOpenBtn(self):
        file_path, ext = QFileDialog.getOpenFileName(self, '파일 열기', os.getcwd(), 'excel file (*.xls *.xlsx)')
        if file_path:
            self.df_list = self.loadData(file_path)
            self.initTableWidget(id=2)
                       

    def on_search_button_clicked(self):
        text = self.line_edit.text()
        self.qtree.selectionModel().clear()
        self.qtree.do_search(text)
  
    def clickTreeBtn(self):
        TreeWidget = self.qtree
        
        TreeWidget.setColumnCount(5)
        TreeWidget.setHeaderLabels(["CLASS", "PREFIX", "ITM_DESC", "QTY", "UOM", "SRC", "PROC", "THREAD"] )
        TreeWidget.setAlternatingRowColors(True)
        TreeWidget.header().setSectionResizeMode(QHeaderView.Interactive)
        
        # Use the new create_tree function instead of anytree
        self.create_tree(self.df_list[2], TreeWidget)

        TreeWidget.expandAll()

        TreeWidget.resizeColumnToContents(0)
        TreeWidget.resizeColumnToContents(1)
        TreeWidget.resizeColumnToContents(2)
        TreeWidget.resizeColumnToContents(3)
        TreeWidget.resizeColumnToContents(4)

    def create_tree(self, df, tree_widget):
        parent_dict = {}

        for index, row in df.iterrows():
            itm = row['ITM']
            parent_itm = row['PARENT']

            itm_data = [itm, row['PREFIX'], row['ITM_DESC'], str(row['QTY']),
                        row['UOM'], row['SRC'], row['PROC'], row['THREAD']]

            if parent_itm not in parent_dict:
                parent_dict[parent_itm] = QTreeWidgetItem(tree_widget, [parent_itm])

            itm_item = QTreeWidgetItem(parent_dict[parent_itm], itm_data)
            parent_dict[itm] = itm_item  
            
    def loadData(self, file_name):
        df_list = []        
        with pd.ExcelFile(file_name) as wb:            
            for i, sn in enumerate(wb.sheet_names):              
                try:
                    df = pd.read_excel(wb, sheet_name=sn)
                    if sn == "ECO_BOM": #ECO_BOM시트만 OLD BOM정리
                        df= df.iloc[3:,:11]
                        df.replace('\n','', regex=True, inplace=True)
                        df= df.rename(columns = df.iloc[0])
                        df= df.drop(df.index[0])
                        df.dropna(axis=0, how='all', inplace=True)
                        df= df
                        df= df.reset_index(drop=True)
                        
                except Exception as e:
                    print('File read error:', e)
                else:
                    df = df.fillna(0)
                    df.name = sn
                    df_list.append(df)
        return df_list
        
    def initTableWidget(self, id):
        # 테이블 위젯 값 쓰기
        self.table.clear()
        # select dataframe
        df = self.df_list[id]; 

        # table write        
        col = len(df.keys())
        self.table.setColumnCount(col)
        self.table.setHorizontalHeaderLabels(df.keys())
 
        row = len(df.index)
        self.table.setRowCount(row)
        self.writeTableWidget(df, row, col)

    def writeTableWidget(self, df, row, col):
        
        for r in range(row): 
            for c in range(col):
                item = QTableWidgetItem(str(df.iloc[r][c]))
                self.table.setItem(r, c, item) 
        self.table.resizeColumnsToContents()



    def save_dataframe_to_excel(self, df):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            df.to_excel(file_path, index=False)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    
    screen = app.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    margin = 30 
    w.setGeometry(margin, margin, screen_width - 2 * margin, screen_height - 2 * margin)
    
    w.show()
    sys.exit(app.exec())   
