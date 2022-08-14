"""
Thuật toán gọi hàm của chương trình:
    main()
        - QuickReset()
        - Common()
            + Process()
        - DigitsSerials()
            + StartAndEnd()
            + Common()
        - CharSetSerials()
            + Common()
"""

from csv import reader
from collections import Counter
from os import remove
from time import time


def QuickReset():
    '''
    Hàm này dùng để reset Folder chương trình về
    trạng thái ban đầu, chưa nhập dữ liệu.
    '''
    # Thực hiện việc xoá dữ liệu cũ người dùng nhập trong file input.csv
    try:
        f = open('input.csv', 'w', encoding='utf-8-sig')
        f.write('Đầu kỳ,,,Nhập,,,Xuất,,,So sánh' + '\n')
        # Cho hai dòng write như này cho đẹp, PEP-8 mà :)
        f.write('Bắt đầu,Kết thúc,,Bắt đầu,Kết thúc,,')
        f.write('Bắt đầu,Kết thúc,,Bắt đầu,Kết thúc')
        f.close()
    except PermissionError:
        print('Hãy đóng file <input.csv> trước khi chạy chương trình.')
    
    # Xoá file output.csv và log.txt, nếu file không tồn tại thì bỏ qua,
    # nếu gặp lỗi PermissionError thì yêu cầu đóng file trước.
    try:
        remove('output.csv')
    except FileNotFoundError:
        pass
    except PermissionError:
        print('Hãy đóng file <output.csv> trước khi chạy chương trình.')

    try:
        remove('log.txt')
    except FileNotFoundError:
        pass
    except PermissionError:
        print('Hãy đóng file <log.txt> trước khi chạy chương trình')


def Process(arr, s):
    '''
    Hàm kiểm tra xem mảng có phần tử trùng nhau hay không,
    nếu trùng thì trả ra những phần tử bị trùng nhau.
    '''
    if len(arr) != len(set(arr)):
        # cnt là một dict có các key là các phần tử,
        # các value là số lần xuất hiện của các phần tử trong arr.
        cnt = Counter(arr)
        # Nếu key có value > 1 (tức là phần tử bị trùng lặp),
        # thì in phần tử đó ra,
        # đồng thời thông báo số lần trùng lặp của phần tử.
        for key in cnt:
            if cnt[key] > 1:
                print('Element {} appears {} times\
                    in <{}>'.format(key, cnt[key], s), file=log)
        print(file=log)  # Để một dòng trống cho thoáng :)
    return set(arr)


def Common():
    '''
    Hàm này là phần chung của hàm DigitsSerials() và hàm CharSetSerials()
    '''
    # global dauky, nhap, xuat, sosanh
    # global set_dauky, set_nhap, set_xuat, set_sosanh
    set_dauky = Process(dauky, 'Đầu kỳ (BC36 n-1)')
    set_nhap = Process(nhap, 'Nhập')
    set_xuat = Process(xuat, 'Xuất')
    set_sosanh = Process(sosanh, 'So sánh (BC36 n)')

    # Phần cảnh báo
    # In ra những phần tử thuộc cảnh báo
    if set_nhap - set_dauky != set_nhap:
        print('[!]  Có serial vừa có trong <đầu kỳ>\
            vừa có trong <nhập>', file=log)
        for item in sorted(list(set_nhap & set_dauky)):
            print(item, file=log)
        print(file=log)  # Để một dòng trống cho thoáng :)

    if set_xuat - set_dauky != set():
        print('[!]  Có serial có trong <xuất>\
            nhưng không có trong <đầu kỳ>', file=log)
        for item in sorted(list(set_xuat-set_dauky)):
            print(item, file=log)
        print(file=log)  # Để một dòng trống cho thoáng :)

    kq = (set_dauky | set_nhap) - set_xuat
    thieu = sorted(list(set(kq) - set_sosanh))
    thua = sorted(list(set_sosanh - set(kq)))

    cnt_thieu = 0
    cnt_thua = 0
    out = open('output.csv', 'w', encoding='utf-8-sig')
    print('Thiếu,Thừa', file=out)

    for i in range(min(len(thieu), len(thua))):
        print('{},{}'.format(thieu[i], thua[i]), file=out)
        cnt_thieu += 1
        cnt_thua += 1

    if len(thieu) < len(thua):
        for k in range(i+1, len(thua)):
            print(',{}'.format(thua[k]), file=out)
            cnt_thua += 1

    elif len(thieu) > len(thua):
        for k in range(i+1, len(thieu)):
            print('{}'.format(thieu[k]), file=out)
            cnt_thieu += 1

    print('[Result]: Thiếu {}, Thừa {}'.format(cnt_thieu, cnt_thua), file=log)
    inp.close()
    out.close()


def StartAndEnd(a_bdkt, a):
    # từng item trong mảng a_bdkt có dạng [start, end]
    # start và end có kiểu là str
    for item in a_bdkt:
        start, end = item
        if end == '':  # Nếu không có giá trị kt thì bd = kt
            end = start
        # Thêm các số từ bd tới kt vào mảng a
        a.extend(range(int(start), int(end) + 1))
    return a


def DigitsSerials():
    global inp, dauky, nhap, xuat, sosanh
    # Khởi tạo mảng cần thiết
    dauky = []
    nhap = []
    xuat = []
    sosanh = []
    inp = open('input.csv', encoding='utf-8-sig')
    # Bỏ hai dòng đầu không đưa vào xử lý
    inp.readline()
    inp.readline()
    r = reader(inp)  # Lấy phần dữ liệu còn lại đưa vào xử lý
    arr = [row for row in r]

    # Xử lý mảng arr thành 4 mảng như dưới
    dauky_bdkt = [item[:2] for item in arr if item[0] != '']
    nhap_bdkt = [item[3:5] for item in arr if item[3] != '']
    xuat_bdkt = [item[6:8] for item in arr if item[6] != '']
    sosanh_bdkt = [item[9:] for item in arr if item[9] != '']

    StartAndEnd(dauky_bdkt, dauky)
    StartAndEnd(nhap_bdkt, nhap)
    StartAndEnd(xuat_bdkt, xuat)
    StartAndEnd(sosanh_bdkt, sosanh)

    Common()


def CharSetSerials():
    global inp, dauky, nhap, xuat, sosanh
    inp = open('input.csv', encoding='utf-8-sig')
    # Bỏ hai dòng đầu không đưa vào xử lý
    inp.readline()
    inp.readline()
    r = reader(inp)  # Lấy phần dữ liệu còn lại đưa vào xử lý
    arr = [row for row in r]

    # Xử lý mảng arr thành 4 mảng như dưới
    dauky = [item[0] for item in arr if item[0] != '']
    nhap = [item[3] for item in arr if item[3] != '']
    xuat = [item[6] for item in arr if item[6] != '']
    sosanh = [item[9] for item in arr if item[9] != '']

    Common()


def main():
    global log
    print('--- CHƯƠNG TRÌNH CHECK SERIAL ---')
    print('Mời bạn chọn chức năng:')
    print('   0. Quick reset')
    print('   1. Digit serials')
    print('   2. Characterset serials')

    while True:
        choice = input('>> Lựa chọn của bạn (0|1|2): ')
        if choice == '0':
            QuickReset()
            print('Done!')
        elif choice == '1':
            log = open('log.txt', 'w', encoding='utf-8-sig')
            t = time()
            DigitsSerials()
            print('[Execution time]:', time()-t, 's', end='', file=log)
            log.close()
            break
        elif choice == '2':
            log = open('log.txt', 'w', encoding='utf-8-sig')
            t = time()
            CharSetSerials()
            print('[Execution time]:', time()-t, 's', end='', file=log)
            log.close()
            break
        elif choice == '':
            break
        else:
            print('Bạn nhập không đúng, vui lòng nhập lại!')


main()
