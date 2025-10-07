from flask import Flask, request, jsonify
from rapidfuzz import process
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    mainQ = data.get("mainQ", "")
    gender = data.get("gender", "")
    questions = data.get("questions", [])
    userInput = data.get("userInput", "")

    dataFromUserInput = questions + [mainQ, gender] + userInput.split(' ')

    keywordsFromUser = set()
    print("main",mainQ)

    keywords = {
        # 🔹 النوع والطابع
        "رجالي", "للرجال", "رجاليه", "رجولي", "حريمي", "نسائي", "للنساء", "أنثوي", "بناتي", "جذاب",
        "مثير", "شيك", "رايق", "كلاسيك", "فخم", "راقي", "ملكي", "عملي", "شبابي", "رومانسي", "نظيف", "ناعم","ورد"

        # 🔹 القوة والثبات
        "قوي", "جامد", "عنيف", "فواح", "ثابت", "بيثبت", "هادي", "خفيف", "ناعم", "تقيل",
        "مش فواح", "مش ثابت", "ريحته بتهدى", "خفيفه", "تقيله", "معتدل", "متوازن",

        # 🔹 الرائحة والمكونات
        "ليمون", "حمضي", "حمضيات", "موالح", "برتقال", "يوسفي", "تفاح", "خوخ", "أناناس", "مانجو", "فراولة",
        "كريمي", "فانيليا", "فاكهة", "سكّري", "حلو", "حلاوة", "زهري", "ورد", "فل", "ياسمين", "لافندر",
        "مسك", "مسكي", "عنبر", "عود", "عودي", "خشب", "خشبي", "جلدي", "جلد", "تبغ", "قهوة", "كاكاو",
        "توابل", "بهارات", "حار", "دافي", "بارد", "منعش", "نظيف", "صابون", "مائي", "بحري", "ملحي",
        "أخضر", "عشبي", "ترابي", "زهور", "زهر", "باتشولي", "طبيعي", "بلاستيك", "مخدر", "نكهي",

        # 🔹 الوقت والموسم
        "صباحي", "نهاري", "مسائي", "ليلي", "صيفي", "شتوي", "ربيعي", "خريفي", "دافي", "منعش",
        "حر", "برد", "جو بارد", "جو حر", "مناسب للصيف", "مناسب للشتا",

        # 🔹 المناسبة والاستخدام
        "يومي", "للاستخدام اليومي", "خروج", "مشاوير", "شغل", "دوام", "مناسبات", "حفلات", "سهرات",
        "فرح", "خروجة", "سفر", "عطري رسمي", "عطري كاجوال", "عطري صباحي", "سهره", "مكتب",

        # 🔹 الانطباع والذوق
        "بيجنن", "تحفة", "حلو", "جميل", "عادي", "مش حلو", "مش مميز", "غريب", "غامض",
        "فاخر", "راقي", "مميز", "مبهر", "مريح", "مزعج", "نفس", "بيخنق", "خفيف عالقلب",
        "يخطف", "ينفع هدية", "مناسب للهدايا",

        # 🔹 الدرجات والرائحة العامة
        "حلوة", "نفاذ", "ناعم", "هادئ", "قوي", "طاغي", "متوسط", "مش نفاذ", "خفيف", "تركيز عالي", "تركيز متوسط",

        # 🔹 نوع العطر
        "بارفان", "اودي بارفان", "اودي تواليت", "كولونيا", "عطر", "سبراي", "زيت", "ميني", "او دي بيرفيوم",
        "او دي تواليت",

        # 🔹 مشاعر وانطباعات إضافية
        "بيفكرني", "بيفكر", "افتكرت", "ذكريات", "ريلاكس", "مريح للأعصاب", "هادي الأعصاب", "مبهج", "مفرح",
        "بيهدي", "بيفتح النفس", "ينور", "مفيش زيه", "كده كده جامد", "بيدفي", "بيبرد", "بيملى المكان"
    }
    synonyms = {
        "رجالي": ["رجولي", "ذكوري", "رجال"],
        "حريمي": ["أنثوي", "نسائي", "بناتي"],
        "زهري": ["ورد", "زهور", "فل", "ورود","ياسمين"],
        "خشبي": ["عود", "صندل", "خشب"],
        "سكّري": ["حلو", "كراميل", "عسلي", "سويت"],
        "فواح": ["ثابت", "مليان", "مشبع", "يبين"],
        "شتوي": ["دافئ", "مريح", "حسي"],
        "فاكهة": ["تفاح", "مانجا", "خوخ", "مشمش", "أناناس"],
        "قوي": ["جامد", "حاد", "نفاذ"],
        "خفيف": ["ناعم", "رايق", "سهل"]
    }

    match2,score, _ = process.extractOne(mainQ, keywords)
    if score > 70:
        mainQ=match2
    print(mainQ ,"   dddddd")
    for word in dataFromUserInput:
        match, score, _ = process.extractOne(word, keywords)
        if score > 70:
            keywordsFromUser.add(match)

    extractedKeywords = set()
    for word in keywordsFromUser:
        extractedKeywords.add(word)
        for main_word, syns in synonyms.items():
            if word in syns:
                extractedKeywords.add(main_word)

    print(f"keyWords after fuzz {keywordsFromUser}")

    ggg = extractedKeywords
    recommendations = []
    import json

    # 1️⃣ افتح الملف واقرأه
    file_path = r"perfume_full.json"
    with open(file_path, "r", encoding="utf-8") as f:
        perfume_json = json.load(f)

    # 2️⃣ حول القوائم إلى set عشان عمليات التقاطع (&) تعمل
    perfume = {k: set(v) for k, v in perfume_json.items()}

    # 4️⃣ حساب التوصيات
    for i in perfume:
        score = len(perfume[i] & ggg) / len(ggg)
        if score >= .2 and mainQ in perfume[i] and gender in perfume[i]:
            recommendations.append({"name": i, "score": round(score * 100, 2)})

    if not recommendations:
        for i in perfume:
            score = len(perfume[i] & ggg) / len(ggg)
            if score >= .2 and gender in perfume[i]:
                recommendations.append({"name": i, "score": round(score * 100, 2)})

    if not recommendations:
        return jsonify({"message": "اعطني تفاصيل اكتر"})

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    print(f"keyWords after fuzz2 {ggg}")
    return jsonify({
        "user_keywords": list(ggg),
        "recommendations": recommendations
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
