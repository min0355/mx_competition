

    # 만일 품번이 틀릴 경우 에러 메시지 출력
    new_part_pattern = r'^\d{6}-\d{5}[A-Za-z]?$|\d{6}-\d{5}[A-Za-z]?-(M|m)$'   # 오직 111111-11111(영문) 만 인식 
    remove_part_pattern = r'(^\d{6}-\d{5}[A-Za-z]?)|(R\d{5}[A-Za-z]?$)|(r\d{5}[A-Za-z]?$)|(\d{6})|(^C\d{8}[A-Za-z]?$)|(^c\d{8}[A-Za-z]?$)|(^L\d{8}[A-Za-z]?$)|(^l\d{8}[A-Za-z]?$)|(^S\d{7})|(^s\d{7})|(^P\d{8})|(^p\d{8})|(^\d{6}-\d{5}[A-Za-z]?$-M)|(^\d{6}-\d{5}[A-Za-z]?$-m)|(^EBUSH\d{4})|(^ebush\d{4})|^R\d{6}[A-Za-z]?$|^r\d{6}[A-Za-z]?$|(^MVZP\d{3})|(^mvzp\d{3})|(^EHOSE\d{4}[A-Za-z]?$)|(^ehose\d{4}[A-Za-z]?$)|(^ETUBN\d{4})|(^etubn\d{4})'
    # 111111-11111(영문), R*****(영문), r*****(영문), 123456, C12345678(영문), L12345678(영문), S1234567, P12345678, 123456-12345(영문)-M, EBUSH1234, R******(영문), MVZP123, EHOSE1234(영문), ETUBN1234 
    
    change_part_pattern = r'(^\d{6}-\d{5}[A-Za-z]?)|(R\d{5}[A-Za-z]?$)|(r\d{5}[A-Za-z]?$)|(\d{6})|(^C\d{8}[A-Za-z]?$)|(^c\d{8}[A-Za-z]?$)|(^L\d{8}[A-Za-z]?$)|(^l\d{8}[A-Za-z]?$)|(^S\d{7})|(^s\d{7})|(^P\d{8})|(^p\d{8})|(^\d{6}-\d{5}[A-Za-z]?$-M)|(^\d{6}-\d{5}[A-Za-z]?$-m)|(^EBUSH\d{4})|(^ebush\d{4})|^R\d{6}[A-Za-z]?$|^r\d{6}[A-Za-z]?$|(^MVZP\d{3})|(^mvzp\d{3})|(^EHOSE\d{4}[A-Za-z]?$)|(^ehose\d{4}[A-Za-z]?$)|(^ETUBN\d{4})|(^etubn\d{4})'
    change_quantity_pattern = r'\b\d{1,3}\b'   # 숫자 3 자리까지만 인식
    
    # 제거 정규식에 추가 해야 할 품번 형식 (좀 더 확인해야 함.)
    # C12345678(영문)  (^C\d{8}[A-Za-z]?$)|(^c\d{8}[A-Za-z]?$)
    # L12345678(영문)  (^L\d{8}[A-Za-z]?$)|(^l\d{8}[A-Za-z]?$)
    # S1234567         (^S\d{7})|(^s\d{7}))
    # P12345678        (^P\d{8})|(^p\d{8}))
    # 123456-12345(영문)-M   (\d{6}-\d{5}[A-Za-z]?-(M|m)$)
    # EBUSH1234              (^EBUSH\d{4})|(^ebush\d{4})
    # R123456                (R\d{6}[A-Za-z]?$)|(r\d{6}[A-Za-z]?$)
    # MVZP123                (^MVZP\d{3})|(^mvzp\d{3})
    # EHOSE1234(영문)        (^EHOSE\d{4}[A-Za-z]*$)
    # ETUBN1234              (^ETUBN\d{4})|(^etubn\d{4})








import tkinter.messagebox as msgbox


# 메시지 출력 
def info():
    msgbox.showinfo("알림", "정상적으로 설변 BOM 생성 처리 되었습니다.")
    root.destroy()  # 알람 메시지 띄우고 프로그램 완전히 종료 처리

def info_bom_open():
    msgbox.showinfo("알림", "입력 상자에 입력하기 전에 BOM 부터 불러와 주세요.")

def info_nothing():
    msgbox.showinfo("알림", "변경 품번에는 아무것도 입력되지 않았습니다. 품번을 입력 해 주세요.")

def info_no_nothing():
    msgbox.showinfo("알림", "변경 수량이 입력되지 않았습니다. 변경되는 수량을 숫자로 입력 해 주세요.")    

def info_no_match_line():
    msgbox.showinfo("알림", "변경 개수 품번과 변경 개수의 입력 숫자가 매칭되지 않습니다. 두 입력창을 확인해 주세요.")

def info_change_part_nothing():
    msgbox.showinfo("알림", "변경하고자 하는 품번이 입력되지 않았습니다.")

def warn():
    msgbox.showwarning("경고", "동일한 품번이 중복 입력되었습니다. 중복 품번을 모두 제거합니다.")

def overlap_del_change_warn():
    msgbox.showwarning("경고", "삭제하려는 품번과 수량 변경하는 품번이 동일하게 입력되었습니다. 이 경우 변경되는 수량과 개수가 다른 품번들은 유지됩니다.")    # 이 부분 정리 필요 

def error():
    msgbox.showerror("에러", "품번 형식 (xxxxxx-xxxxx + 영어, LxxxxXXXX 등) 이나 숫자가 정확히 기입되었는지 확인 해 주세요.")
