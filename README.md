# 🗑️ Garbage Classification Project 🚀

Dự án này sử dụng **Deep Learning** để phân loại rác thải từ hình ảnh, giúp nâng cao nhận thức về tái chế và xử lý rác.

---

## **📢 Tính năng**

✅ Phân loại rác thành các nhóm như **nhựa, giấy, thủy tinh, kim loại, hữu cơ**  
✅ Sử dụng mô hình **Deep Learning** với TensorFlow/Keras  
✅ Giao diện đơn giản, dễ sử dụng với **PyQt6**  
✅ Tích hợp với **MySQL** để lưu trữ dữ liệu

---

## **📥 Cài đặt**

### **1️⃣ Clone Repository**

```bash
git clone https://github.com/minhluquang/Garbage-Classification.git
cd Garbage-Classification

```
### **2️⃣ Cài đặt thư viện**

```bash
pip install -r requirements.txt
```

### **3️⃣ Tạo thư mục models/ và thêm mô hình**
Sau khi đã tạo thư mục models cũng như thêm model vào vào thư mục.
Chúng ta cần vào **views/classify.py** để thay đổi tên model muốn chạy.
```
model_path = os.path.join(os.path.dirname(__file__), "../models/resnet50.h5")
```
Ngoài ra, cần phải vào **views/classify.py** ở **function: handle_predict** để thay đổi size hình ảnh cũng như className phù hợp với các cài đặt trong đoạn code train model.

### **📂 Cấu trúc thư mục**
```
Garbage-Classification/
│── models/                     # Chứa các mô hình Deep Learning (.h5)
│   ├── resnet50.h5             # Mô hình ResNet50 đã huấn luyện (ví dụ)
│   ├── ...                     # Các mô hình khác (nếu có)
│
│── assets/                      # Chứa các tài nguyên tĩnh
│   ├── images/                  # Hình ảnh dùng trong ứng dụng
│
│── config/                      # Chứa các file cấu hình
│   ├── db_config.py             # Cấu hình kết nối cơ sở dữ liệu
│
│── ui/                          # Chứa các file giao diện PyQt
│   ├── classify.ui              # Giao diện phân loại rác
│   ├── login.ui                 # Giao diện đăng nhập
│   ├── signup.ui                # Giao diện đăng ký tài khoản
│
│── views/                       # Chứa các file xử lý logic
│   ├── classify.py              # Xử lý phân loại rác từ hình ảnh
│   ├── login.py                 # Xử lý đăng nhập
│   ├── signup.py                # Xử lý đăng ký tài khoản
│
│── main.py                      # Chương trình chính để chạy ứng dụng
│── python-db.sql                 # File chứa câu lệnh SQL tạo database
│── requirements.txt              # Danh sách thư viện cần cài đặt
│── README.md                     # Hướng dẫn sử dụng
│── .gitignore                    # File liệt kê các tệp không cần push lên Git
```
