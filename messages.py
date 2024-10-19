from langdetect import detect as detect_langdetect, detect_langs as detect_langs_langdetect

RULES = """📜 Խմբի անդամների վարքագծի կանոններ 📜

1. 🙏 Հարգանք: Հարգեք միմյանց տեսակետները և անհատականությունը:
2. 🚫 Անձնական վիրավորանքներ չկան: Արգելվում է անձնական հարձակումները, վիրավորանքները և անպատշաճ լեզուն։
3. 📸 Լուսանկարով նույնականացում: Նոր անդամները պարտադիր պետք է ներկայացնեն իրենց իրական լուսանկարը:
4. 🛑 Կարգավորվող հաղորդագրություններ: Խմբում թույլ չեն տրվում գռեհիկ կամ ոչ պատշաճ բառեր:
5. 💡 Խորհուրդներ: Խմբի անդամները կարող են տալ ու ստանալ օգտակար խորհուրդներ՝ առանց վիրավորելու:
6. 🔒 Գաղտնիություն: Պահպանեք խմբի անդամների գաղտնիությունը, ոչ մի դեպքում չբացահայտեք անձնական տեղեկություններ առանց թույլտվության:
7. 🆘 Օգնություն: Եթե ունեք հարց կամ խնդիր, դիմեք խմբի ադմինիստրատորին:
8. ⚖️ Կոնստրուկտիվության պարտադրանք: Քննադատությունը պետք է լինի կառուցողական և նպատակաուղղված:
9. 🚫 Խնդրանքներ: Խնդրում ենք չգրել սպամ և գովազդներ:
10. 🤝 Համերաշխություն։ Աջակցեք միմյանց, խթանեք թիմային աշխատասիրությունն ու գործընկերային հարաբերությունները:

📌 Կանոններին հետևելը խթանում է անհատական և թիմային աշխատանքի արդյունավետությունը։
"""

NO_FACE_DETECTED = "Բոտը չկարողացավ հայտնաբերել դեմքը 😔"
NO_PROFILE_PHOTO_MSG = "Լուսանկար չկա 📷"
NO_SECOND_PHOTO_MSG = "Բացակայում է երկրորդ լուսանկարը 📸"
NO_LAST_NANE_MSG = "Բացակայում է ազգանունը ❌"

LAST_NAME = "Ազգանուն 📝"
PROFILE_PHOTO_MSG = "Լուսանկար դեմքով չկա 📷😊"
PROFILE_PHOTO2_MSG = "Երկրորդ նախագիծ լուսանկար դեմքով 📸😊"
BLOCK_MSG = " Այս օգտատերը արգելափակել է անհայտ աղբյուրներից հաղորդագրությունների ընդունումը։ ⛔"


async def sendMsgToAdmins(chat_id, context, msg) -> None:
    administrators = await context.bot.get_chat_administrators(chat_id)
    for admin in administrators:
        if admin.user.is_bot:
            continue
        await context.bot.send_message(admin.user.id, msg)

async def sendPhotoToAdmins(chat_id, context, photo) -> None:
    administrators = await context.bot.get_chat_administrators(chat_id)
    for admin in administrators:
        if admin.user.is_bot:
            continue
        await context.bot.send_photo(admin.user.id, photo)

async def welcome_message(first_name, last_name):
    message = f"🎉 Բարի գալուստ {first_name} {last_name} դեպի Fundamental Crypto Academy! 🇦🇲\n🌟 Մաղթում ենք Ձեզ մեծ հաջողություններ ձեր ուսումնական ճանապարհին! 🎓📚"
    return message

async def ValidationErrorToAdmins(member, groupName, msg):
    user_id = member.id
    first_name = member.first_name
    last_name = member.last_name

    return (
        f"👋 Նոր օգտատեր միացավ, բայց հեռացվեց\n\n"
        f"📛 Պատճառ: {msg}\n"
        f"🙍‍♂️ Օգտատեր: {first_name} {last_name}\n"
        f"🆔 Օգտատիրոջ ID: {user_id}\n"
        f"💬 Խմբի անվանում: {groupName}"
    )

async def ValidationErrorToUser(msg):
    return (
        "🚫 Մուտքի հարցումը մերժվեց\n\n"
        "⚠️ Ցավոք, վավերացման սխալ է տեղի ունեցել։\n"
        f"Խնդրում ենք ավելացնել ձեր {msg}՝ խնդրանքը ավարտին հասցնելու համար։ 📝\n\n"
        "Շնորհակալություն ձեր ըմբռնման համար! 🙏"
    )

cross_words_en = {
    "Damn", "Hell", "Stupid", "Idiot", "Fool", "Bastard", "Crap", "Moron", "Dumb", "Shut up",
    "Jerk", "Loser", "Scum", "Freak", "Lame", "Pathetic", "Sucks", "Piss off", "Douche", "Asshole",
    "Bitch", "Fuck", "Shit", "Whore", "Slut", "Prick", "Dick", "Pussy", "Cunt", "Ass",
    "Jackass", "Retard", "Sissy", "Scumbag", "Wanker", "Bullshit", "Damn it", "Pissed", "Craphead", "Motherfucker",
    "Son of a bitch", "Douchebag", "Bastards", "Fucker", "Fuckface", "Cock", "Cockhead", "Shithead", "Twat", "Arse",
    "Bugger", "Tosser", "Knobhead", "Pillock", "Knob", "Git", "Muppet", "Shag", "Tosspot", "Piss",
    "Bollocks", "Wanker", "Bellend", "Prat", "Chav", "Slag", "Wazzock", "Arsehole", "Bint", "Skank",
    "Wench", "Ponce", "Tart", "Bastard", "Pikey", "Knobend", "Nobhead", "Cocksucker", "Shite", "Twunt",
    "Bugger off", "Sod off", "Nobber", "Fanny", "Boff", "Minger", "Pikey", "Slapper", "Tart", "Troglodyte"
}

cross_words_ru = {
    "Чёрт", "Ад", "Глупый", "Идиот", "Дурак", "Ублюдок", "Дерьмо", "Дебил", "Тупой", "Заткнись",
    "Придурок", "Лох", "Мразь", "Чучело", "Слабак", "Жалкий", "Отстой", "Отвали", "Долбоёб", "Мудак",
    "Сука", "Хуй", "Блядь", "Шлюха", "Проститутка", "Урод", "Член", "Пизда", "Анус", "Жопа",
    "Кретин", "Сопляк", "Тварь", "Баран", "Пидорас", "Дерьмоед", "Говнюк", "Мудачок", "Херовина", "Дрянь",
    "Сволочь", "Мудаки", "Ублюдки", "Пидарасы", "Еблан", "Хуйло", "Говноед", "Уебан", "Тупица", "Арс",
    "Бугор", "Тупняк", "Гондон", "Пошёл ты", "Чмо", "Дебилы", "Долбоёбы", "Пидарасы", "Хуесос", "Чмошник",
    "Твари", "Ублюдочная", "Говнюшки", "Пиздюк", "Тупорылый", "Мудачки", "Херня", "Сраный", "Ебанутый", "Говно",
    "Уёбок", "Козлина", "Пидор", "Сука", "Хуярить", "Дрочить", "Пиздеть", "Заебал", "Ебать", "Пидарасина",
    "Пидарашка", "Заебись", "Пиздец", "Мудачня", "Ебланство", "Блядь", "Пиздатый", "Ебанутый", "Мудак", "Говнюк",
    "Пидарок", "Хуйло", "Пиздёж", "Ёбнуться", "Мудила", "Пидараска", "Членосос", "Говноед", "Уёбище", "Тупиздюк"
}

cross_words_am = {
    "Անիծված", "Ապուշ", "Անկելք", "Իդիոտ", "Անասուն", "Կեղտոտ", "Հիմար", "Խելագար", "Բթամիտ", "Լռիր",
    "Անպիտան", "Խղճուկ", "Տհաս", "Տականք", "Անտեր", "Գյոռ", "Բոզ", "Շոռբա", "Պոռնիկ", "Պոռնիկություն",
    "Հոգեկան", "Անդիմադրելի", "Թշնամական", "Հակահայրենասիրական", "Տխմար", "Տկլոր", "Աղետ", "Նեռ", "Գող",
    "Խոզ", "Թափթփուկ", "Սրիկա", "Անբարոյական", "Սրիկաներ", "Հրեշներ", "Սատկածներ", "Գողեր", "Արծաթաքաղներ",
    "Տնաքանդ", "Անասուններ", "Բոզեր", "Սրիկաներ", "Անպիտաններ", "Հիմարներ", "Թափթփուկներ", "Թշնամիներ",
    "Անբարոյականներ", "Հոգեկաններ", "Կեղծավորություն", "Դատարկամիտություն", "Գետնատարած", "Անհոգի", "Սրբապիղծներ",
    "Բոզի", "Տականքի", "Գյորգյոռ", "Գոմիկ", "Թուրք", "Բոզավատ", "Շնացող", "Բոզատես", "Շներ", "Խոզեր",
    "Գոմեշ", "Տավար", "Պախան", "Ճիճու", "Գոմեր"
}

language_map = {
    'en': cross_words_en,
    'ru': cross_words_ru,
    'hy': cross_words_am
}

def detect_language(text):
    unicode_ranges = {
        'en': ('\u0041', '\u005A', '\u0061', '\u007A'),
        'ru': ('\u0400', '\u04FF'),  
        'hy': ('\u0530', '\u058F')   
    }
    
    def char_in_range(char, unicode_range):
        return unicode_range[0] <= char <= unicode_range[1]
    
    language_scores = {lang: 0 for lang in unicode_ranges}
    
    for char in text:
        for lang, ranges in unicode_ranges.items():
            if any(char_in_range(char, (ranges[i], ranges[i+1])) for i in range(0, len(ranges), 2)):
                language_scores[lang] += 1
                
    detected_language = max(language_scores, key=language_scores.get)
    return detected_language

async def contains_cross_words(text):
    language_code = detect_language(text)
    text_lower = text.lower()
    cross_words = language_map[language_code]

    for word in cross_words:
        if word.lower() in text_lower:
            return True
    return False
