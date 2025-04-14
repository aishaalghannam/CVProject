import pdfplumber
import re

# الكلمات المفتاحية للمؤهل
degree_keywords = [
    "بكالوريوس", "ماجستير", "دكتوراه", "Bachelor", "Master", "PhD", 
    "Associate's degree", "Diploma"
]

# الكلمات المفتاحية للتخصص
major_keywords = [
    "علوم حاسب", "محاسبة", "إدارة أعمال", "هندسة", "Computer Science", "Accounting", 
    "Business Administration", "Finance", "Marketing", "Electrical Engineering", "Civil Engineering", 
    "Software Engineering", "Mechanical Engineering", "Mathematics", "Physics", "Data Science"
]

# الكلمات المفتاحية للمهارات
skills_keywords = [
    "Python", "SQL", "Excel", "Power BI", "Tableau", "Git", "Machine Learning", 
    "Deep Learning", "AI", "Java", "JavaScript", "HTML", "CSS", "C++", "R", "React", "Node.js", 
    "Project Management", "Agile", "Docker", "Kubernetes", "Azure", "AWS", "Big Data", "Tableau"
]

# الكلمات المفتاحية للغات
language_keywords = [
    "اللغة الإنجليزية", "English", "Fluent", "جيد", "ممتاز", "Native", 
    "Arabic", "French", "Spanish", "German", "Italian", "Russian"
]

# الكلمات المفتاحية للشهادات
certificates_keywords = [
    "PMP", "Udemy", "Coursera", "شهادة", "دورة", "Certificate", "Google Analytics", "AWS Certified", 
    "Scrum Master", "Microsoft Certified", "Data Science Certificate", "IELTS", "TOEFL", "Cisco Certified", 
    "Project Management Professional", "Certified Information Systems Security Professional (CISSP)"
]

# الكلمات المفتاحية للوظائف
job_titles = [
    "مهندس", "محاسب", "مدير", "مبرمج", "محلل نظم", "Software Engineer", "Accountant", 
    "Manager", "Data Scientist", "Business Analyst", "System Architect", "Project Manager", "HR Specialist", 
    "Graphic Designer", "UI/UX Designer", "Sales Manager", "Product Manager"
]

# دالة لتحليل السيرة الذاتية
def parse_cv(filepath):
    # قراءة النص من ملف PDF
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # استخراج الوظيفة
    job_title = next((word for word in job_titles if word.lower() in text.lower()), "")

    # استخراج اسم الجامعة
    university = next((line.strip() for line in text.split("\n") if "جامعة" in line or "University" in line), "")

    # استخراج المؤهل
    degree = next((word for word in degree_keywords if word.lower() in text.lower()), "")

    # استخراج التخصص
    major = next((word for word in major_keywords if word.lower() in text.lower()), "")
    
    # استخراج سنوات الخبرة
    match = re.search(r"خبرة\s*(\d+)\s*(سنة|سنوات)?", text)
    experience = f"{match.group(1)} سنوات" if match else ""

    # استخراج المهارات
    skills = [kw for kw in skills_keywords if kw.lower() in text.lower()]

    # استخراج اللغة
    language = next((word for word in language_keywords if word.lower() in text.lower()), "")

    # استخراج الشهادات
    certificates = [c for c in certificates_keywords if c.lower() in text.lower()]

    # إرجاع البيانات كقاموس
    return {
        "الجامعة": university,
        "المؤهل": degree,
        "التخصص": major,
        "سنوات الخبرة": experience,
        "المهارات": ", ".join(skills),
        "اللغة": language,
        "الوظيفة السابقة": job_title,
        "الشهادات": ", ".join(certificates)
    }
