#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_business_lessons.py — создаёт data/business/lesson01..15.json.
Урок 1 заполнен из материалов учебника + рабочей тетради.
Уроки 2-15 — заглушки с заголовками модулей и уроков.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BIZ = ROOT / "data" / "business"
BIZ.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# УРОК 1 — полный контент
# ═══════════════════════════════════════════════════════════

LESSON_01 = {
  "module": 1,
  "lesson": 1,
  "module_title": {
    "zh": "接待客商",
    "ru": "Приём клиентов",
    "en": "Receiving Business Guests",
    "tk": "", "uz": "", "tg": "", "id": ""
  },
  "title": {
    "zh": "我已经给两位订好酒店了",
    "pinyin": "Wǒ yǐjīng gěi liǎng wèi dìng hǎo jiǔdiàn le",
    "ru": "Я уже забронировал вам отель",
    "en": "I've already booked the hotel for you two",
    "tk": "", "uz": "", "tg": "", "id": ""
  },
  "goals": {
    "zh": ["能完成接机、酒店入住等商务活动。",
           "能使用航班信息查询、酒店预订等常用软件。",
           "能在出入中国海关时正确申报所带物品。"],
    "ru": ["Осуществлять приём в аэропорту, регистрацию в отеле и т.п.",
           "Пользоваться приложениями для проверки рейсов и бронирования отелей.",
           "Правильно декларировать物品 при прохождении китайской таможни."],
    "en": ["Handle business activities like airport pickup and hotel check-in.",
           "Use flight-tracking and hotel-booking apps.",
           "Correctly declare belongings at Chinese customs."]
  },
  "warmup": {
    "question": {
      "zh": "根据预习时的准备，说一说：",
      "ru": "Обсудите, опираясь на подготовку:",
      "en": "Discuss based on your preparation:"
    },
    "items": [
      {"zh": "出差时可能会用到哪些APP？",
       "ru": "Какие приложения могут понадобиться в командировке?",
       "en": "Which apps might you use on a business trip?"},
      {"zh": "办理酒店入住的过程是怎样的？",
       "ru": "Как проходит регистрация в отеле?",
       "en": "What is the process of hotel check-in?"},
      {"zh": "出入境时哪些物品需要向中国海关申报？",
       "ru": "Какие物品 нужно декларировать на таможне Китая?",
       "en": "Which items must be declared at Chinese customs?"}
    ]
  },
  "dialogs": [
    {
      "scene": {
        "zh": "在机场", "ru": "В аэропорту", "en": "At the airport",
        "tk": "", "uz": "", "tg": "", "id": ""
      },
      "audio": "textbook_1.mp3",
      "lines": [
        {"speaker": "孟安诺", "zh": "欢迎来到深圳！",
         "pinyin": "Huānyíng lái dào Shēnzhèn!",
         "ru": "Добро пожаловать в Шэньчжэнь!",
         "en": "Welcome to Shenzhen!",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "谢谢。实在抱歉，天气不好，航班延误了。另外，过海关时，我们托运的行李中有些东西需要申报，让您久等了。",
         "pinyin": "Xièxie. Shízài bàoqiàn, tiānqì bù hǎo, hángbān yánwù le. Lìngwài, guò hǎiguān shí, wǒmen tuōyùn de xíngli zhōng yǒu xiē dōngxi xūyào shēnbào, ràng nín jiǔděng le.",
         "ru": "Спасибо. Прошу прощения — погода плохая, рейс задержали. К тому же на таможне пришлось декларировать часть багажа, извините, что заставили ждать.",
         "en": "Thank you. Sorry — bad weather, our flight was delayed. Also, at customs we had to declare some items in our checked luggage, sorry to keep you waiting.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "没事儿，我在“飞常准”上看到延误信息了，正好利用这个时间回了几封邮件。",
         "pinyin": "Méi shìr, wǒ zài “Fēichángzhǔn” shàng kàn dào yánwù xìnxī le, zhènghǎo lìyòng zhège shíjiān huí le jǐ fēng yóujiàn.",
         "ru": "Ничего страшного — я видел информацию о задержке в «Фэйчанчжунь», как раз использовал это время, чтобы ответить на несколько писем.",
         "en": "No worries — I saw the delay on “Feichangzhun” and used the time to reply to a few emails.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "“非常准”？",
         "pinyin": "“Fēichángzhǔn”?",
         "ru": "«Фэйчанчжунь»?",
         "en": "“Feichangzhun”?",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "对，这个软件能实时显示航班信息，也能预订机票，出差用特别方便。",
         "pinyin": "Duì, zhège ruǎnjiàn néng shíshí xiǎnshì hángbān xìnxī, yě néng yùdìng jīpiào, chūchāi yòng tèbié fāngbiàn.",
         "ru": "Да, это приложение в реальном времени показывает информацию о рейсах и позволяет бронировать билеты — очень удобно в командировке.",
         "en": "Yes, this app displays real-time flight info and lets you book tickets — very handy for business trips.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "哦，是飞机的“飞”啊，我以为是非常的“非”呢，那我也下载一个。对了，您汉语说得太地道了。",
         "pinyin": "Ò, shì fēijī de “fēi” a, wǒ yǐwéi shì fēicháng de “fēi” ne, nà wǒ yě xiàzài yī gè. Duì le, nín Hànyǔ shuō de tài dìdao le.",
         "ru": "А, это «飞» от «самолёта», а я думала — «非» от «очень». Тогда я тоже скачаю. Кстати, вы говорите по-китайски очень аутентично.",
         "en": "Oh, it's “fēi” from “airplane” — I thought it was “fēi” from “very”. I'll download it too. By the way, your Chinese is so authentic.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "您的汉语也不错啊，我在电话里还以为您是中国人呢！",
         "pinyin": "Nín de Hànyǔ yě búcuò a, wǒ zài diànhuà lǐ hái yǐwéi nín shì Zhōngguórén ne!",
         "ru": "Ваш китайский тоже отличный — по телефону я даже подумал, что вы китаянка!",
         "en": "Your Chinese is great too — on the phone I even thought you were Chinese!",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "哪里哪里。我来介绍一下，这位是我们采购部总经理Jason，这位是讯达公司的孟安诺。",
         "pinyin": "Nǎli nǎli. Wǒ lái jièshào yīxià, zhè wèi shì wǒmen cǎigòu bù zǒngjīnglǐ Jason, zhè wèi shì Xùndá gōngsī de Mèng Ānnuò.",
         "ru": "Что вы, что вы. Позвольте представить: это генеральный менеджер нашего отдела закупок Jason, а это Мэн Аньно из компании «Сюньда».",
         "en": "You flatter me. Let me introduce: this is Jason, general manager of our procurement department, and this is Meng Annuo from Xunda.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "您好！孟先生。",
         "pinyin": "Nín hǎo! Mèng xiānsheng.",
         "ru": "Здравствуйте, господин Мэн!",
         "en": "Hello, Mr. Meng!",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "您好，Jason先生。我叫了个专车，在地下停车场，咱们坐直梯下去吧。我已经给两位订好酒店了，咱们先去办理入住。",
         "pinyin": "Nín hǎo, Jason xiānsheng. Wǒ jiào le ge zhuānchē, zài dìxià tíngchēchǎng, zánmen zuò zhítī xiàqù ba. Wǒ yǐjīng gěi liǎng wèi dìng hǎo jiǔdiàn le, zánmen xiān qù bǎnlǐ rùzhù.",
         "ru": "Здравствуйте, господин Jason. Я вызвал такси-премиум, оно на подземной парковке — давайте спустимся на лифте. Я уже забронировал отель, сначала заселимся.",
         "en": "Hello, Mr. Jason. I called a premium car — it's in the underground parking. Let's take the elevator down. I've already booked your hotel, let's check in first.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "Jason", "zh": "好的！", "pinyin": "Hǎo de!",
         "ru": "Хорошо!", "en": "OK!", "tk": "", "uz": "", "tg": "", "id": ""}
      ]
    },
    {
      "scene": {
        "zh": "在酒店前台", "ru": "На ресепшн отеля", "en": "At the hotel front desk",
        "tk": "", "uz": "", "tg": "", "id": ""
      },
      "audio": "textbook_1.mp3",
      "lines": [
        {"speaker": "服务员", "zh": "先生您好！请问您有预订吗？",
         "pinyin": "Xiānsheng nín hǎo! Qǐngwèn nín yǒu yùdìng ma?",
         "ru": "Здравствуйте! У вас есть бронь?",
         "en": "Hello sir! Do you have a reservation?",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "孟安诺", "zh": "有，两间高级大床房，23号到26号。",
         "pinyin": "Yǒu, liǎng jiān gāojí dàchuángfáng, èrshísān hào dào èrshíliù hào.",
         "ru": "Да, два улучшенных номера с большой кроватью, с 23 по 26.",
         "en": "Yes, two deluxe king rooms, from the 23rd to the 26th.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "服务员", "zh": "好的，请出示一下证件。",
         "pinyin": "Hǎo de, qǐng chūshì yīxià zhèngjiàn.",
         "ru": "Хорошо, покажите документы, пожалуйста.",
         "en": "OK, please show your ID.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "这是我们的护照。",
         "pinyin": "Zhè shì wǒmen de hùzhào.",
         "ru": "Вот наши паспорта.",
         "en": "Here are our passports.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "服务员", "zh": "系统里显示您的房费总额是1800元。",
         "pinyin": "Xìtǒng lǐ xiǎnshì nín de fángfèi zǒng'é shì yīqiān bābǎi yuán.",
         "ru": "В системе отображается, что общая сумма за номер — 1800 юаней.",
         "en": "The system shows your total room charge is 1,800 yuan.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "给你信用卡。",
         "pinyin": "Gěi nǐ xìnyòngkǎ.",
         "ru": "Вот кредитная карта.",
         "en": "Here's my credit card.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "服务员", "zh": "先冻结您2000元的预授权作为押金，结算时房费会从预授权中扣除。",
         "pinyin": "Xiān dòngjié nín liǎngqiān yuán de yùshòuquán zuòwéi yājīn, jiésuàn shí fángfèi huì cóng yùshòuquán zhōng kòuchú.",
         "ru": "Сначала заморозим 2000 юаней (предавторизация) как депозит; при расчёте стоимость номера будет вычтена из предавторизации.",
         "en": "First, we'll freeze a pre-authorization of 2,000 yuan as a deposit; the room rate will be deducted at settlement.",
         "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "安娜", "zh": "好的。", "pinyin": "Hǎo de.",
         "ru": "Хорошо.", "en": "OK.", "tk": "", "uz": "", "tg": "", "id": ""},
        {"speaker": "服务员", "zh": "给您房卡，退房时间是中午12点之前。早餐时间从7点到10点，在二楼自助餐厅。",
         "pinyin": "Gěi nín fángkǎ, tuìfáng shíjiān shì zhōngwǔ shí'èr diǎn zhīqián. Zǎocān shíjiān cóng qī diǎn dào shí diǎn, zài èr lóu zìzhù cāntīng.",
         "ru": "Вот ваши ключи. Выписка — до 12:00. Завтрак с 7:00 до 10:00, на втором этаже, шведский стол.",
         "en": "Here are your room keys. Check-out is before 12:00. Breakfast is from 7 to 10 on the 2nd floor, buffet.",
         "tk": "", "uz": "", "tg": "", "id": ""}
      ]
    }
  ],
  "vocabulary": [
    {"hanzi": "延误", "pinyin": "yánwù", "pos": "v.",
     "meaning": {"ru": "задерживаться (о рейсе)", "en": "to delay"},
     "simple": {"ru": "«延误» — значит опоздать по сравнению с установленным временем.",
                "en": "“延误” means being later than the set time."},
     "examples": [
       {"zh": "前往喀什的CA1477次航班计划13:20起飞，因为大雪，现在预计要21:00才能起飞，延误了大约8个小时。",
        "ru": "Рейс CA1477 в Кашгар должен был вылететь в 13:20, но из-за снегопада вылет теперь ожидается в 21:00 — задержка около 8 часов.",
        "en": "Flight CA1477 to Kashgar was scheduled for 13:20, but due to heavy snow it's now expected to take off at 21:00 — a delay of about 8 hours."}
     ],
     "question": {"ru": "По каким причинам обычно задерживают самолёты?",
                  "en": "What usually causes flight delays?"}},

    {"hanzi": "海关", "pinyin": "hǎiguān", "pos": "n.",
     "meaning": {"ru": "таможня", "en": "customs"},
     "simple": {"ru": "«海关» — государственный орган, который проверяет товары и物品 на границе, взимает пошлины.",
                "en": "“海关” is the state body that checks goods at the border and collects duties."},
     "examples": [
       {"zh": "出国旅行或留学前，最好先上网查一查，什么东西不能过海关。",
        "ru": "Перед поездкой или учёбой за границей лучше проверить в интернете, что нельзя провозить через таможню.",
        "en": "Before traveling or studying abroad, it's best to check online what you can't bring through customs."}
     ],
     "question": {"ru": "Что нельзя провозить через китайскую таможню?",
                  "en": "What cannot go through Chinese customs?"}},

    {"hanzi": "托运", "pinyin": "tuōyùn", "pos": "v.",
     "meaning": {"ru": "сдать в багаж", "en": "to consign (luggage)"},
     "simple": {"ru": "«托运» — сдать вещи транспортной компании. В аэропорту обычно сдаём крупный багаж, чтобы не нести его в салон.",
                "en": "“托运” means handing things to a transport company. At the airport we check in large luggage so we don't have to carry it on board."},
     "examples": [
       {"zh": "我们的行李很多，需要提前到机场办理托运。",
        "ru": "У нас много багажа, нужно приехать в аэропорт заранее и сдать его.",
        "en": "We have a lot of luggage and need to arrive at the airport early to check it in."}
     ],
     "question": {"ru": "Что обычно сдают в багаж при перелёте?",
                  "en": "What do you usually check in when flying?"}},

    {"hanzi": "申报", "pinyin": "shēnbào", "pos": "v.",
     "meaning": {"ru": "декларировать", "en": "to declare"},
     "simple": {"ru": "«申报» — письменно сообщить в соответствующие органы. На таможне вы заполняете декларацию на物品, требующие说明.",
                "en": "“申报” means reporting in writing. At customs, you fill in a declaration form for items that need to be specified."},
     "examples": [
       {"zh": "中国海关规定，如果带的香烟超过400支，需要向海关申报。",
        "ru": "Китайская таможня требует декларировать более 400 сигарет.",
        "en": "Chinese customs requires declaring more than 400 cigarettes."}
     ],
     "question": {"ru": "Какие物品 нужно декларировать при въезде в вашу страну?",
                  "en": "Which items must be declared when entering your country?"}},

    {"hanzi": "实时", "pinyin": "shíshí", "pos": "adv.",
     "meaning": {"ru": "в реальном времени", "en": "real-time"},
     "simple": {"ru": "«实时» — синхронно с происходящим.",
                "en": "“实时” means synchronously with what's happening."},
     "examples": [
       {"zh": "“实时公交”APP可以让乘客实时查到要坐的公交车开到哪儿了。",
        "ru": "Приложение «实时公交» позволяет пассажиру в реальном времени видеть, где сейчас нужный автобус.",
        "en": "The “Real-time Bus” app lets passengers see in real time where their bus is."}
     ],
     "question": {"ru": "Какой сейчас实时 курс вашей валюты к юаню?",
                  "en": "What is your currency's real-time rate to the yuan?"}},

    {"hanzi": "显示", "pinyin": "xiǎnshì", "pos": "v.",
     "meaning": {"ru": "отображать, показывать", "en": "to display, show"},
     "simple": {"ru": "«显示» — давать увидеть (обычно данные: температура, пульс, расстояние, время).",
                "en": "“显示” means showing (data: temperature, heart rate, distance, time)."},
     "examples": [
       {"zh": "体温计能显示出人的体温，宝宝现在的体温是36.5℃。",
        "ru": "Термометр показывает температуру тела; у малыша сейчас 36,5 °C.",
        "en": "The thermometer shows body temperature — the baby's is 36.5°C."}
     ],
     "question": {"ru": "Что появляется на экране, когда телефон почти разряжен?",
                  "en": "What appears on the screen when the phone is almost dead?"}},

    {"hanzi": "预订", "pinyin": "yùdìng", "pos": "v.",
     "meaning": {"ru": "бронировать, заказывать заранее", "en": "to book, reserve"},
     "simple": {"ru": "«预订» — заказать заранее.",
                "en": "“预订” means to order in advance."},
     "examples": [
       {"zh": "安娜8月3日要去上海出差，她7月15日就在网上预订了一家酒店的房间。",
        "ru": "Анна едет в командировку в Шанхай 3 августа — ещё 15 июля она забронировала отель онлайн.",
        "en": "Anna goes to Shanghai on business on Aug 3; on Jul 15 she already booked a hotel online."}
     ],
     "question": {"ru": "Каким приложением вы обычно бронируете отели и билеты?",
                  "en": "Which app do you usually use to book hotels and tickets?"}},

    {"hanzi": "采购", "pinyin": "cǎigòu", "pos": "v.",
     "meaning": {"ru": "закупать", "en": "to purchase"},
     "simple": {"ru": "«采购» — выбирать и покупать в соответствии с потребностями.",
                "en": "“采购” means to select and buy based on needs."},
     "examples": [
       {"zh": "公司采购了100台新电脑，总价80万。",
        "ru": "Компания закупила 100 новых компьютеров на общую сумму 800 000.",
        "en": "The company purchased 100 new computers for 800,000 yuan total."}
     ],
     "question": {"ru": "Чем отличаются 采购部, 采购员, 采购经理, 采购部部长?",
                  "en": "How do 采购部, 采购员, 采购经理, 采购部部长 differ?"}},

    {"hanzi": "专车", "pinyin": "zhuānchē", "pos": "n.",
     "meaning": {"ru": "такси-премиум (заказное авто)", "en": "premium car service"},
     "simple": {"ru": "«专车» — машина, обслуживающая конкретного человека или заказ.",
                "en": "“专车” is a car serving a specific person or order."},
     "examples": [
       {"zh": "从公司打车到机场，可以选择出租车、专车或商务车，专车的服务比一般的出租车好一些，价格也贵一些，商务车最贵。",
        "ru": "От офиса до аэропорта можно взять такси, премиум-авто или бизнес-вэн: сервис премиум-авто лучше обычного такси, и дороже, а бизнес-вэн — самый дорогой.",
        "en": "From office to airport you can take a taxi, premium car, or business van: premium is nicer and pricier than a regular taxi; business van is most expensive."}
     ],
     "question": {"ru": "Какой транспорт вы выбираете и почему?",
                  "en": "Which transport do you choose and why?"}},

    {"hanzi": "出示", "pinyin": "chūshì", "pos": "v.",
     "meaning": {"ru": "предъявлять", "en": "to show, produce"},
     "simple": {"ru": "«出示» — достать и показать документ (удостоверение, паспорт).",
                "en": "“出示” means to take out and show a document (ID, passport)."},
     "examples": [
       {"zh": "正式考试时，在教室门口需要向工作人员出示身份证或护照，以及准考证。",
        "ru": "На официальном экзамене у входа нужно предъявить сотруднику паспорт или удостоверение и пропуск.",
        "en": "At an official exam, you must show staff your ID/passport and exam pass at the door."}
     ],
     "question": {"ru": "В каких ситуациях нужно предъявлять удостоверение?",
                  "en": "In which situations must you show ID?"}},

    {"hanzi": "证件", "pinyin": "zhèngjiàn", "pos": "n.",
     "meaning": {"ru": "документ, удостоверение", "en": "credentials, ID"},
     "simple": {"ru": "«证件» — документ, удостоверяющий личность или статус: паспорт, ID, студенческий, диплом и т.д.",
                "en": "“证件” is a document proving identity or status: passport, ID, student card, diploma, etc."},
     "examples": [
       {"zh": "实在抱歉，如果没有证件，我无法确认您的身份，不能让您进去。",
        "ru": "Прошу прощения, без документа я не могу подтвердить вашу личность и не могу вас пропустить.",
        "en": "I'm sorry, without ID I cannot confirm your identity and cannot let you in."}
     ],
     "question": {"ru": "Какие важные документы есть в вашей стране?",
                  "en": "Which important documents exist in your country?"}},

    {"hanzi": "总额", "pinyin": "zǒng'é", "pos": "n.",
     "meaning": {"ru": "общая сумма", "en": "total amount"},
     "simple": {"ru": "«总额» — общее количество.",
                "en": "“总额” is the total amount."},
     "examples": [
       {"zh": "小王每个月工资8000元，一年的工资总额是96000元。",
        "ru": "У Сяо Вана зарплата 8000 юаней в месяц, за год — 96 000 юаней.",
        "en": "Xiao Wang earns 8,000 per month; annual total is 96,000 yuan."}
     ],
     "question": {"ru": "Какой был общий объём внешней торговли Китая в 2022 году?",
                  "en": "What was China's total foreign trade in 2022?"}},

    {"hanzi": "冻结", "pinyin": "dòngjié", "pos": "v.",
     "meaning": {"ru": "заморозить (счёт)", "en": "to freeze (account)"},
     "simple": {"ru": "«冻结» — деньги на карте есть, но банк временно не даёт ими пользоваться.",
                "en": "“冻结” means the money is on the card but the bank temporarily blocks its use."},
     "examples": [
       {"zh": "我的银行卡被冻结了，不能取钱了。",
        "ru": "Мою банковскую карту заблокировали — снять деньги нельзя.",
        "en": "My bank card was frozen — I can't withdraw money."}
     ],
     "question": {"ru": "В каких случаях банк замораживает счёт?",
                  "en": "When does a bank freeze an account?"}},

    {"hanzi": "预授权", "pinyin": "yùshòuquán", "pos": "n.",
     "meaning": {"ru": "предавторизация", "en": "pre-authorization"},
     "simple": {"ru": "«预授权» — при оплате в отеле/прокате карта замораживает примерную сумму до окончательного расчёта.",
                "en": "“预授权” is when a hotel/rental freezes an estimated sum on your card until final settlement."},
     "examples": [
       {"zh": "先生您好，您的房费总额是1800元，我们先冻结您2000元的预授权。",
        "ru": "Здравствуйте, общая стоимость номера — 1800 юаней, мы сначала заморозим предавторизацию 2000 юаней.",
        "en": "Hello, your total room charge is 1,800 yuan; first we'll freeze a 2,000-yuan pre-authorization."}
     ],
     "question": {"ru": "Когда обычно используют предавторизацию?",
                  "en": "When is pre-authorization usually used?"}},

    {"hanzi": "押金", "pinyin": "yājīn", "pos": "n.",
     "meaning": {"ru": "залог, депозит", "en": "deposit"},
     "simple": {"ru": "«押金» — дополнительная сумма за аренду/проживание; возвращают при выезде, если ничего не потеряно/сломано.",
                "en": "“押金” is an extra amount for rent/hotel; returned on check-out if nothing is lost or broken."},
     "examples": [
       {"zh": "随着科技发展和消费习惯的变化，很多酒店已经不收押金，只收房费了。",
        "ru": "С развитием технологий и изменением потребительских привычек многие отели уже не берут депозит, только плату за номер.",
        "en": "With tech and habits changing, many hotels no longer charge a deposit — only room fees."}
     ],
     "question": {"ru": "Где кроме отелей нужен депозит?",
                  "en": "Where else besides hotels is a deposit required?"}},

    {"hanzi": "结算", "pinyin": "jiésuàn", "pos": "v.",
     "meaning": {"ru": "производить расчёт", "en": "to settle an account"},
     "simple": {"ru": "«结算» — подсчитать общую сумму.",
                "en": "“结算” means to calculate the total amount."},
     "examples": [
       {"zh": "整个项目结束后，总公司会跟您结算全部费用。",
        "ru": "По завершении всего проекта головной офис рассчитается с вами по всем расходам.",
        "en": "After the whole project, HQ will settle all expenses with you."}
     ],
     "question": {"ru": "Когда обычно проводят расчёт?",
                  "en": "When is settlement usually done?"}},

    {"hanzi": "扣除", "pinyin": "kòuchú", "pos": "v.",
     "meaning": {"ru": "вычитать", "en": "to deduct"},
     "simple": {"ru": "«扣除» — вычесть из общей суммы.",
                "en": "“扣除” means to subtract from the total."},
     "examples": [
       {"zh": "结算时，房费会从预授权中扣除。",
        "ru": "При расчёте стоимость номера вычтут из предавторизации.",
        "en": "At settlement, the room rate is deducted from the pre-authorization."},
       {"zh": "小王每月税前工资8800元，扣除保险和税以后，实际工资收入是7500元。",
        "ru": "До вычетов Сяо Ван получает 8800; после вычета страховки и налога на руки — 7500.",
        "en": "Xiao Wang's pre-tax salary is 8,800; after insurance and tax — 7,500 net."}
     ],
     "question": {"ru": "Что вычитают из зарплаты в вашей стране?",
                  "en": "What is deducted from salaries in your country?"}}
  ],
  "expressions": [
    {"zh": "您汉语说得太地道了。",
     "pinyin": "Nín Hànyǔ shuō de tài dìdao le.",
     "ru": "Вы говорите по-китайски очень аутентично.",
     "en": "Your Chinese is so authentic.",
     "note": {"ru": "Используется для похвалы чужого китайского. «地道» = настоящий, чистый, стандартный.",
              "en": "Used to praise someone's Chinese. “地道” = genuine, pure, standard."}},
    {"zh": "我在电话里还以为您是中国人呢！",
     "pinyin": "Wǒ zài diànhuà lǐ hái yǐwéi nín shì Zhōngguórén ne!",
     "ru": "По телефону я даже подумал, что вы китаянка!",
     "en": "On the phone I even thought you were Chinese!",
     "note": {"ru": "Ещё варианты: «您这汉语说得和中国人完全没两样啊», «您是外国人吗？怎么汉语说得这么好».",
              "en": "Other variants: “您这汉语说得和中国人完全没两样啊”, “您是外国人吗？怎么汉语说得这么好”."}},
    {"zh": "请出示一下证件。",
     "pinyin": "Qǐng chūshì yīxià zhèngjiàn.",
     "ru": "Покажите документы, пожалуйста.",
     "en": "Please show your ID.",
     "note": {"ru": "Фраза на ресепшн, в библиотеке, на экзамене — когда нужно подтвердить личность.",
              "en": "Used at front desks, libraries, exams — whenever identity must be confirmed."}},
    {"zh": "先冻结您2000元的预授权作为押金，结算时房费会从预授权中扣除。",
     "pinyin": "Xiān dòngjié nín liǎngqiān yuán de yùshòuquán zuòwéi yājīn, jiésuàn shí fángfèi huì cóng yùshòuquán zhōng kòuchú.",
     "ru": "Сначала заморозим 2000 юаней как депозит; при расчёте стоимость номера вычтут из предавторизации.",
     "en": "We'll first freeze a 2,000-yuan pre-authorization as a deposit; at settlement the room rate will be deducted.",
     "note": {"ru": "Часто говорит администратор отеля при заселении.",
              "en": "A common phrase hotel receptionists say at check-in."}}
  ],
  "grammar": [
    {"pattern": "在…上",
     "explanation": {"ru": "Указывает на источник/место: «в (на) чём-то».",
                     "en": "Marks the source/place: “on / in something”."},
     "examples": [
       {"zh": "我在“飞常准”上看到延误信息了。",
        "ru": "Я увидел информацию о задержке в «Фэйчанчжунь».",
        "en": "I saw the delay info on “Feichangzhun”."}
     ]},
    {"pattern": "正好 + 利用 + 时间 + 动词",
     "explanation": {"ru": "«Как раз использовать время, чтобы…»",
                     "en": "“Just use the time to…”"},
     "examples": [
       {"zh": "正好利用这个时间回了几封邮件。",
        "ru": "Как раз использовал это время, чтобы ответить на несколько писем.",
        "en": "I used the time to reply to a few emails."}
     ]},
    {"pattern": "以为…呢",
     "explanation": {"ru": "«(ошибочно) думал, что…» — с оттенком удивления.",
                     "en": "“(Mistakenly) thought…” — with surprise."},
     "examples": [
       {"zh": "我在电话里还以为您是中国人呢！",
        "ru": "По телефону я даже думал, что вы китаянка!",
        "en": "On the phone I even thought you were Chinese!"}
     ]},
    {"pattern": "给…订好",
     "explanation": {"ru": "«Уже забронировать кому-то» (результат).",
                     "en": "“Already booked for someone” (result)."},
     "examples": [
       {"zh": "我已经给两位订好酒店了。",
        "ru": "Я уже забронировал вам отель.",
        "en": "I've already booked the hotel for you two."}
     ]},
    {"pattern": "先…，…时…会…",
     "explanation": {"ru": "Схема процесса: «сначала…, при… будет…».",
                     "en": "A process scheme: “first…, at… will…”."},
     "examples": [
       {"zh": "先冻结您2000元的预授权作为押金，结算时房费会从预授权中扣除。",
        "ru": "Сначала заморозим 2000 юаней, при расчёте сумма спишется.",
        "en": "First freeze 2,000 yuan; at settlement it will be deducted."}
     ]}
  ],
  "exercises": {
    "comprehension": [
      {"q": {"zh": "安娜的航班为什么延误了？", "ru": "Почему у Анны задержали рейс?", "en": "Why was Anna's flight delayed?"},
       "a": {"zh": "因为天气不好。", "ru": "Из-за плохой погоды.", "en": "Because of bad weather."}},
      {"q": {"zh": "过海关时，安娜和Jason做什么了？", "ru": "Что делали Анна и Jason на таможне?", "en": "What did Anna and Jason do at customs?"},
       "a": {"zh": "有些托运的行李需要申报。", "ru": "Декларировали часть багажа.", "en": "Declared some checked luggage."}},
      {"q": {"zh": "孟安诺是怎么回应安娜的道歉的？", "ru": "Как Мэн Аньно ответил на извинения?", "en": "How did Meng Annuo respond to Anna's apology?"},
       "a": {"zh": "他说没事儿，自己利用时间回了邮件。", "ru": "Сказал, что ничего, он использовал время, чтобы ответить на письма.", "en": "He said no worries, he used the time to reply to emails."}},
      {"q": {"zh": "“飞常准”是什么？这种起名方式有什么特点？",
             "ru": "Что такое «Фэйчанчжунь»? В чём особенность названия?",
             "en": "What is “Feichangzhun”? What's special about its name?"},
       "a": {"zh": "是一个实时显示航班信息的APP。名字借用“非常准”的谐音，用“飞机”的“飞”代替“非常”的“非”。",
             "ru": "Приложение реального времени для информации о рейсах. Название — игра слов: «非常准» (очень точно), но «非» заменено на «飞» (самолёт).",
             "en": "A real-time flight info app. Its name puns on “非常准” (very accurate) but replaces “非” with “飞” (airplane)."}},
      {"q": {"zh": "安娜和孟安诺是怎么夸奖对方中文好的？",
             "ru": "Как Анна и Мэн Аньно похвалили китайский друг друга?",
             "en": "How did Anna and Meng Annuo compliment each other's Chinese?"},
       "a": {"zh": "安娜说孟安诺说得地道；孟安诺说以为安娜是中国人。",
             "ru": "Анна сказала, что Мэн говорит аутентично; Мэн — что думал, будто Анна китаянка.",
             "en": "Anna said Meng speaks authentically; Meng said he thought Anna was Chinese."}},
      {"q": {"zh": "孟安诺预订了什么房间？", "ru": "Какие номера забронировал Мэн?", "en": "What rooms did Meng book?"},
       "a": {"zh": "两间高级大床房，23号到26号。", "ru": "Два улучшенных номера с большой кроватью, 23–26.", "en": "Two deluxe king rooms, 23rd–26th."}},
      {"q": {"zh": "服务员会怎样为Jason他们结算房费？",
             "ru": "Как администратор рассчитается с Jason?",
             "en": "How will the receptionist settle with Jason?"},
       "a": {"zh": "先从信用卡预授权中扣除房费。",
             "ru": "Сначала спишет стоимость номера из предавторизации карты.",
             "en": "First, deduct from the credit card pre-authorization."}}
    ],
    "true_false": [
      {"q": {"zh": "Jason和安娜的航班延误是因为天气不好。", "ru": "Рейс Jason и Анны задержали из-за погоды.", "en": "Their flight was delayed due to weather."}, "answer": True},
      {"q": {"zh": "孟安诺在机场等了很久，不太高兴。", "ru": "Мэн Аньно долго ждал и был недоволен.", "en": "Meng waited long and was unhappy."}, "answer": False},
      {"q": {"zh": "“飞常准”只能显示航班信息，不能订机票。", "ru": "«Фэйчанчжунь» показывает только информацию о рейсах, билеты не бронирует.", "en": "“Feichangzhun” only shows flight info, cannot book tickets."}, "answer": False},
      {"q": {"zh": "Jason的职位是采购员。", "ru": "Jason — сотрудник отдела закупок (не менеджер).", "en": "Jason's position is procurement clerk."}, "answer": False},
      {"q": {"zh": "安娜向服务员出示了护照。", "ru": "Анна показала администратору паспорт.", "en": "Anna showed the receptionist her passport."}, "answer": True},
      {"q": {"zh": "安娜用现金交了押金。", "ru": "Анна заплатила депозит наличными.", "en": "Anna paid the deposit in cash."}, "answer": False}
    ],
    "multiple_choice": [
      {"q": {"zh": "如果要去旅行，最好提前（　）酒店和机票。", "ru": "В поездке лучше заранее ___ отель и билеты.", "en": "For a trip, it's best to ___ hotel and tickets in advance."},
       "options": ["订购", "预定", "申报", "预订"], "answer": 3},
      {"q": {"zh": "我觉得这个打车软件很方便，你也（　）一个吧。", "ru": "Мне нравится это такси-приложение — ты тоже ___ его.", "en": "I like this taxi app — you should ___ it too."},
       "options": ["上传", "下载", "复制", "冻结"], "answer": 1},
      {"q": {"zh": "一个外国人能把汉语说得这么（　），真了不起啊！", "ru": "Иностранец говорит по-китайски так ___ — потрясающе!", "en": "A foreigner speaks Chinese so ___ — amazing!"},
       "options": ["地道", "真实", "实在", "真正"], "answer": 0},
      {"q": {"zh": "如果身份证丢失，请您尽快去派出所（　）申报补领新证的有关手续。", "ru": "Если потеряли удостоверение, срочно в полицию ___ процедуру восстановления.", "en": "If you lose your ID, go to the police station to ___ re-issuance procedures."},
       "options": ["办理", "管理", "办公", "结算"], "answer": 0},
      {"q": {"zh": "（　）是指信用卡或借记卡的持卡人在宾馆、酒店或出租公司等消费时，消费与结算不在同一时间完成，特约单位通过POS机预先向发卡机构索要授权的行为。", "ru": "___ — когда оплата и расчёт не совпадают; POS запрашивает у банка предварительное разрешение.", "en": "___ — when payment and settlement differ; the POS asks the bank for pre-approval."},
       "options": ["预订", "预约", "预留", "预授权"], "answer": 3},
      {"q": {"zh": "如果信用卡丢失，可以主动要求银行临时（　）信用卡。", "ru": "Если карта потеряна, можно попросить банк временно ___ её.", "en": "If the card is lost, you can ask the bank to temporarily ___ it."},
       "options": ["扣除", "结算", "冻结", "冷冻"], "answer": 2},
      {"q": {"zh": "如果你的支付宝信用分在600分以上，骑共享单车时就不需要交（　）了。", "ru": "Если твой Alipay-скор выше 600, при аренде велосипеда не нужен ___.", "en": "If your Alipay score is 600+, you don't need a ___ for shared bikes."},
       "options": ["基金", "总额", "押金", "余额"], "answer": 2},
      {"q": {"zh": "北斗卫星导航系统是中国自行研发的全球第三个成熟的卫星导航系统，它可以为全球用户提供（　）精准定位和导航服务。", "ru": "Beidou — третья成熟 глобальная навигационная система, даёт ___ точное позиционирование.", "en": "BeiDou provides ___ precise positioning globally."},
       "options": ["按时", "实时", "地道", "超前"], "answer": 1}
    ],
    "fill_blank": {
      "title": {"zh": "安娜的日记", "ru": "Дневник Анны", "en": "Anna's diary"},
      "text": {
        "zh": "2022年7月23日 雷雨\n今天我们来到深圳，天气不好，航班（　）了。过海关的时候，我们带的一些物品需要（　），耽误了很长时间，到达出口的时候，讯达公司的孟安诺已经在等我们了。他等了很久，我以为他会很无聊，没想到他早就在“飞常准”上看到航班信息了，他（　）利用等我们的时间（　）了几封邮件，什么工作都没耽误。",
        "ru": "23 июля 2022, гроза.\nСегодня мы приехали в Шэньчжэнь — погода плохая, рейс (　). На таможне часть物品 нужно было (　), потратили много времени. Когда дошли до выхода, Мэн Аньно из «Сюньда» уже ждал. Ждал долго — я думала, ему скучно, но он давно увидел информацию о рейсе в «Фэйчанчжунь» и (　) использовал время ожидания, чтобы (　) несколько писем — работа не пострадала.",
        "en": "July 23, 2022, thunderstorm.\nToday we arrived in Shenzhen — bad weather, our flight was (　). At customs some items had to be (　), it took a long time. When we reached the exit, Meng Annuo from Xunda was already waiting. He'd waited a long time — I thought he'd be bored, but he'd already seen the flight info on “Feichangzhun” and (　) used the waiting time to (　) a few emails — nothing was delayed."
      },
      "answers": [
        {"zh": "延误", "ru": "задержали", "en": "delayed"},
        {"zh": "申报", "ru": "декларировать", "en": "declare"},
        {"zh": "正好", "ru": "как раз", "en": "just"},
        {"zh": "回", "ru": "ответил", "en": "replied to"}
      ]
    }
  },
  "audio": {
    "textbook_1": "textbook_1.mp3",
    "vocab": "vocab.mp3"
  }
}


# ═══════════════════════════════════════════════════════════
# Заголовки уроков 2-15
# ═══════════════════════════════════════════════════════════

LESSONS_INDEX = [
    (1,  1, "接待客商", "Приём клиентов",       "我已经给两位订好酒店了", "Я уже забронировал вам отель"),
    (1,  2, "接待客商", "Приём клиентов",       "请您确认一下日程安排",   "Подтвердите расписание"),
    (1,  3, "接待客商", "Приём клиентов",       "很荣幸为二位接风洗尘",   "Для меня честь устроить вам приём"),
    (2,  4, "考察与订购", "Осмотр и заказ",      "这是我们公司的产品体验区", "Наш демонстрационный зал продукции"),
    (2,  5, "考察与订购", "Осмотр и заказ",      "这家工厂的规模可真不小", "Этот завод действительно крупный"),
    (2,  6, "考察与订购", "Осмотр и заказ",      "我接受这个报价",         "Я принимаю это предложение"),
    (3,  7, "新产品推广与销售", "Продвижение и продажи", "我们的广告最好新旧结合", "Рекламе нужно сочетать старое и новое"),
    (3,  8, "新产品推广与销售", "Продвижение и продажи", "选对了代言人就能事半功倍", "С правильным амбассадором — вдвое эффективнее"),
    (3,  9, "新产品推广与销售", "Продвижение и продажи", "这个活动力度确实不小",   "Акция действительно мощная"),
    (4, 10, "参加展销会", "Участие в выставке", "在官网平台申请品牌展位",       "Заявка на бренд-стенд на сайте"),
    (4, 11, "参加展销会", "Участие в выставке", "我边介绍边给您演示",           "Расскажу и покажу одновременно"),
    (4, 12, "参加展销会", "Участие в выставке", "我们非常看重和中国公司的合作", "Мы ценим сотрудничество с компаниями Китая"),
    (5, 13, "应聘与入职", "Собеседование и адаптация", "欢迎你参加今天的面试", "Добро пожаловать на собеседование"),
    (5, 14, "应聘与入职", "Собеседование и адаптация", "我一定会加倍努力的",   "Я буду стараться вдвойне"),
    (5, 15, "应聘与入职", "Собеседование и адаптация", "我把你拉到部门微信群", "Добавлю тебя в WeChat-группу отдела"),
]


def make_stub(module, lesson, module_ru, module_zh, title_ru, title_zh):
    return {
      "module": module,
      "lesson": lesson,
      "module_title": {"zh": module_zh, "ru": module_ru, "en": "", "tk": "", "uz": "", "tg": "", "id": ""},
      "title": {"zh": title_zh, "ru": title_ru, "en": "", "tk": "", "uz": "", "tg": "", "id": ""},
      "status": "stub",
      "goals": {}, "warmup": {}, "dialogs": [], "vocabulary": [],
      "expressions": [], "grammar": [], "exercises": {}, "audio": {}
    }


def main():
    # Урок 1
    p1 = BIZ / "lesson01.json"
    p1.write_text(json.dumps(LESSON_01, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {p1.relative_to(ROOT)}  ({p1.stat().st_size} байт)")

    # Уроки 2-15 — заглушки
    for (module, lesson, mod_zh, mod_ru, t_zh, t_ru) in LESSONS_INDEX:
        if lesson == 1:
            continue
        stub = make_stub(module, lesson, mod_ru, mod_zh, t_ru, t_zh)
        p = BIZ / f"lesson{lesson:02d}.json"
        p.write_text(json.dumps(stub, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"OK: {p.relative_to(ROOT)} (заглушка)")

    print()
    print(f"Итого: {len(LESSONS_INDEX)} уроков в data/business/")
    print("Урок 1 — полный. Остальные — заглушки.")


if __name__ == "__main__":
    main()