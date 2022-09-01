from collections import Counter
from os import getpid, system
from psutil import Process
from re import search
from sys import platform
from time import localtime, strftime, time


def StartEnd(tpl) -> tuple:
    result = ()
    for item in tpl:
        try:
            start, end = map(int, item.split())
        except ValueError:
            start = end = int(item)
        result += (range(start, end+1),)
    return result


def CheckDuplicate(arr, s):
    if len(arr) != len(set(arr)):
        counter = Counter(arr)
        for key in counter:
            if counter[key] > 1:
                print('Serial {} xuất hiện {} lần ở <{}>'.format(
                    key, counter[key], s))
            else:
                break
        print()


print('CHƯƠNG TRÌNH CHECK SERIAL')
with open('input.txt', 'w', encoding='utf-8') as inp:
    inp.write('--- Đầu kỳ ---\n\n\n')
    inp.write('--- Nhập ---\n\n\n')
    inp.write('--- Xuất ---\n\n\n')
    inp.write('--- So sánh ---\n')

# Tự động mở file <input.txt> cho người dùng nhập
# Sau khi lưu file và đóng file, chương trình sẽ chạy tiếp
if platform == 'linux':
    system('gedit input.txt')
elif platform == 'win32':
    system('notepad input.txt')
elif platform == 'darwin':
    system('textedit input.txt')

# Ghi nhận thời gian bắt đầu thực thi
execTime = time()

# Lấy tất cả dòng trong file <input.txt> trừ dòng trống
with open('input.txt', encoding='utf-8') as inp:
    data = tuple([x.replace('\n', '') for x in inp.readlines() if x != '\n'])

dauky = data[1:data.index('--- Nhập ---')]
nhap = data[data.index('--- Nhập ---')+1:data.index('--- Xuất ---')]
xuat = data[data.index('--- Xuất ---')+1:data.index('--- So sánh ---')]
sosanh = data[data.index('--- So sánh ---')+1:]

# Ghép nối tất cả các serial lại và kiểm tra có xuất hiện chữ cái không,
# - nếu có, đó là các serial có chữ cái
# - nếu không, đó là các serial số và chạy hàm <StartEnd>
data = ''.join(x for x in dauky + nhap + xuat + sosanh)
if not search('[A-Za-z]', data):
    dauky = StartEnd(dauky)
    nhap = StartEnd(nhap)
    xuat = StartEnd(xuat)
    sosanh = StartEnd(sosanh)

# Kiểm tra xem có các serial trùng lặp trong cùng một phần không
CheckDuplicate(dauky, 'Đầu kỳ')
CheckDuplicate(nhap, 'Nhập')
CheckDuplicate(xuat, 'Xuất')
CheckDuplicate(sosanh, 'So sánh')

# Đưa ra lời nhắc nếu có sự bất thường trong đầu vào
if set(nhap) & set(dauky) != set():
    print('[!]  Có serial vừa có trong <đầu kỳ> vừa có trong <nhập>')
    for item in sorted(set(nhap) & set(dauky)):
        print(item)
    print()

if set(xuat) - (set(dauky) | set(nhap)) != set():
    print('[!]  Có serial có trong <xuất>\
nhưng không có trong <đầu kỳ> và <nhập>')
    for item in sorted(set(xuat) - (set(dauky) | set(nhap))):
        print(item)
    print()

# Cuối kỳ = Đầu kỳ + Nhập - Xuất
# "Thiếu" là những serial có trong <Cuối kỳ> nhưng không có trong <So sánh>
# "Thừa" là những serial có trong <So sánh> nhưng không có trong <Cuối kỳ>
cuoiky = (set(dauky) | set(nhap)) - set(xuat)
thieu = sorted(set(cuoiky) - set(sosanh))
thua = sorted(set(sosanh) - set(cuoiky))
print('[Kết quả]: Thiếu {}, Thừa {}'.format(len(thieu), len(thua)))

# Ghi kết quả ra file <output.txt>
with open('output.txt', 'w', encoding='utf-8') as out:
    print('[Hiện tại]:', strftime("%d/%m/%Y %H:%M:%S", localtime()), file=out)
    out.write('--- Thiếu ---\n')
    for item in thieu:
        print(item, file=out)
    out.write('\n--- Thừa ---\n')
    for item in thua:
        print(item, file=out)

# Lấy thời gian thực thi
execTime = time() - execTime      # Thời gian tính theo giây (s)
ONE_SECOND = 1
MILISECONDS_PER_SECOND = 1000     # 1 s = 1000 ms
if execTime >= ONE_SECOND:
    execTime = '{:.5f} s'.format(execTime)
else:
    execTime = '{:.5f} ms'.format(execTime * MILISECONDS_PER_SECOND)
print('[Thời gian thực thi]:', execTime)

# Lấy khoảng bộ nhớ đã sử dụng
execMemory = Process(getpid()).memory_info().rss   # Bộ nhớ tính theo byte (B)
BYTES_PER_GIGABYTE = 1073741824   # 1 GB = 1024^3 B = 1073741824 B
BYTES_PER_MEGABYTE = 1048576      # 1 MB = 1024^2 B = 1048576 B
BYTES_PER_KILOBYTE = 1024         # 1 KB = 1024^1 B = 1024 B
if execMemory >= BYTES_PER_GIGABYTE:
    execMemory = '{:.5f} GB'.format(execMemory / BYTES_PER_GIGABYTE)
elif execMemory >= BYTES_PER_MEGABYTE:
    execMemory = '{:.5f} MB'.format(execMemory / BYTES_PER_MEGABYTE)
else:
    execMemory = '{:.5f} KB'.format(execMemory / BYTES_PER_KILOBYTE)
print('[Bộ nhớ sử dụng]:', execMemory)

# Tự động mở file <output.txt>
print('Đóng file <output.txt> => chương trình tự động thoát.')
if platform == 'linux':
    system('gedit output.txt')
elif platform == 'win32':
    system('notepad output.txt')
elif platform == 'darwin':
    system('textedit output.txt')
