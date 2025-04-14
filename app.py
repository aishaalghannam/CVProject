import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from cv_parser import parse_cv  # استيراد الدالة لتحليل السيرة الذاتية

app = Flask(__name__)

UPLOAD_FOLDER = 'CVs'  
ALLOWED_EXTENSIONS = {'pdf'}  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# التحقق من امتداد الملف
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# دالة لحذف السيرة الذاتية من ملف Excel بناءً على اسم الملف
def delete_cv_from_excel(cv_filename):
    excel_file = "نتائج_السير_الذاتية.xlsx"

    # التحقق إذا كان الملف موجودًا
    if os.path.exists(excel_file):
        # قراءة البيانات من ملف Excel
        df = pd.read_excel(excel_file)

        # حذف السيرة الذاتية بناءً على اسم الملف
        df = df[df["اسم الملف"] != cv_filename]

        # إعادة حفظ الملف بعد الحذف
        df.to_excel(excel_file, index=False)
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "لا يوجد ملف مرفق", 400
        
        file = request.files['file']
        
        if file.filename == '':
            return "لم يتم اختيار ملف", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # نحلل السيرة الذاتية باستخدام دالة parse_cv
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            parsed_data = parse_cv(filepath)
            parsed_data['اسم الملف'] = filename  # إضافة اسم الملف للبيانات

            # ملف Excel حيث سيتم تخزين النتائج
            excel_file = "نتائج_السير_الذاتية.xlsx"

            # إذا كان الملف موجودًا، نقوم بقراءته وإضافة البيانات الجديدة إليه
            if os.path.exists(excel_file):
                df = pd.read_excel(excel_file)  # قراءة البيانات الحالية من الملف
                # إضافة البيانات الجديدة إلى DataFrame الحالي
                df = pd.concat([df, pd.DataFrame([parsed_data])], ignore_index=True)
            else:
                # إذا لم يكن الملف موجودًا، ننشئ ملف جديد
                df = pd.DataFrame([parsed_data])

            # حفظ التحديثات في الملف
            df.to_excel(excel_file, index=False)

            return redirect(url_for('success', name=filename))

    return render_template('index.html')

# صفحة نجاح بعد رفع السيرة الذاتية
@app.route('/success')
def success():
    return "تم رفع السيرة الذاتية بنجاح!"

# صفحة لحذف السيرة الذاتية
@app.route('/delete/<filename>', methods=['GET'])
def delete_cv(filename):
    if delete_cv_from_excel(filename):
        return f"تم حذف السيرة الذاتية {filename} بنجاح!"
    else:
        return "لم يتم العثور على السيرة الذاتية في الملف."

if __name__ == '__main__':
    app.run(debug=True)
