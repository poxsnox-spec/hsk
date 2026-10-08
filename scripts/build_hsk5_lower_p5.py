# -*- coding: utf-8 -*-
"""Уроки 28-30 (Unit 10 — 关注经济)."""
from build_hsk5_lower import _vocab, _t, save


# ============================================================
# LESSON 28 — 最受欢迎的毕业生
# ============================================================
def lesson28():
    vocab = [
        _vocab("届", "jiè", "m.", "выпуск; счётное слово для выпусков", "session, year, class"),
        _vocab("本科", "běnkē", "n.", "бакалавриат", "undergraduate education"),
        _vocab("面对", "miànduì", "v.", "сталкиваться, перед лицом", "to face, to confront"),
        _vocab("乐观", "lèguān", "adj.", "оптимистичный", "optimistic"),
        _vocab("就业", "jiùyè", "v.", "трудоустройство", "to find employment"),
        _vocab("实话", "shíhuà", "n.", "правда", "truth, true words"),
        _vocab("优势", "yōushì", "n.", "преимущество", "superiority, advantage"),
        _vocab("简历", "jiǎnlì", "n.", "резюме", "resume, CV"),
        _vocab("现场", "xiànchǎng", "n.", "место, площадка", "site, spot"),
        _vocab("职位", "zhíwèi", "n.", "должность", "position, post"),
        _vocab("体验", "tǐyàn", "v.", "испытать, ощутить", "to feel and experience"),
        _vocab("从此", "cóngcǐ", "adv.", "с тех пор", "from then on, since then"),
        _vocab("范围", "fànwéi", "n.", "рамки, сфера", "scope, range"),
        _vocab("初（级）中（学）", "chū(jí)zhōng(xué)", "n.", "неполная средняя школа", "junior high school"),
        _vocab("顾问", "gùwèn", "n.", "консультант", "consultant, adviser"),
        _vocab("参考", "cānkǎo", "v.", "справляться, использовать как справочник", "to consult, to refer to"),
        _vocab("成长", "chéngzhǎng", "v.", "расти, взрослеть", "to grow up"),
        _vocab("制作", "zhìzuò", "v.", "изготовлять, производить", "to make, to produce"),
        _vocab("才艺", "cǎiyì", "n.", "талант и умения", "talent and skill"),
        _vocab("假设", "jiǎshè", "v.", "предположить, допустить", "to suppose, to assume"),
        _vocab("乘", "chéng", "v.", "ехать (на транспорте)", "to ride, to travel by"),
        _vocab("反应", "fǎnyìng", "v.", "реагировать", "to respond, to react"),
        _vocab("到达", "dàodá", "v.", "прибыть, достичь", "to reach, to arrive"),
        _vocab("老板", "lǎobǎn", "n.", "начальник, босс", "boss, employer"),
        _vocab("陆续", "lùxù", "adv.", "один за другим", "one after another, in succession"),
        _vocab("提问", "tíwèn", "v.", "задавать вопрос", "to ask a question"),
        _vocab("堆", "duī", "m.", "куча", "heap, pack, pile"),
        _vocab("情侣", "qínglǚ", "n.", "влюблённая пара", "couple, lovers"),
        _vocab("制订", "zhìdìng", "v.", "разрабатывать, составлять", "to make, to draw up"),
        _vocab("休闲", "xiūxián", "v.", "отдыхать, досуг", "to have leisure, to relax"),
        _vocab("具体", "jùtǐ", "adj.", "конкретный", "specific, detailed"),
        _vocab("专注", "zhuānzhù", "adj.", "сосредоточенный", "concentrated, engrossed"),
        _vocab("显然", "xiǎnrán", "adj.", "очевидный", "obvious, evident"),
        _vocab("成立", "chénglì", "v.", "учреждать, создавать", "to establish, to set up"),
        _vocab("部门", "bùmén", "n.", "отдел", "department, section"),
        _vocab("执着", "zhízhuó", "adj.", "настойчивый, упорный", "persistent, persevering"),
        _vocab("光明", "guāngmíng", "adj.", "светлый", "bright, promising"),
        _vocab("前途", "qiántú", "n.", "будущее, перспектива", "future, prospect"),
        _vocab("行业", "hángyè", "n.", "отрасль", "trade, profession, industry"),
        _vocab("缺乏", "quēfá", "v.", "не хватать, испытывать недостаток", "to lack, to be short of"),
    ]

    grammar = [
        {
            "word": "从此", "pos": "adv.",
            "explanation": {
                "ru": "«从此» — наречие, «с этого времени», «с тех пор». Обозначает отправную точку в прошлом.",
                "en": "«从此» is an adverb meaning 'from this time on', 'since then'. Marks a starting point in the past.",
            },
            "formula": {"ru": "从此 + глагольная фраза / предложение",
                        "en": "从此 + verb phrase / clause"},
            "examples": [
                {"zh": "因为小学六年级的时候，他迷上了公交车，从此，就一直关注公交线路。",
                 "ru": "В шестом классе он увлёкся автобусами, и с тех пор постоянно следил за маршрутами.",
                 "en": "He became obsessed with buses in sixth grade, and from then on he kept following bus routes."},
                {"zh": "李白听了老婆婆的话，很受感动。从此他刻苦用功，最后成了一位伟大的诗人。",
                 "ru": "Вдохновлённый словами старушки, Ли Бо с тех пор усердно учился и стал великим поэтом.",
                 "en": "Inspired by the old woman's words, Li Bai studied hard from then on and became a great poet."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "他十年前来到中国，__。", "answer": "从此就在这里生活了。"},
                {"type": "fill_blank", "question": "医生说他体重过重，__。", "answer": "从此他开始每天运动。"},
            ],
        },
        {
            "word": "假设", "pos": "v./n.",
            "explanation": {
                "ru": "«假设» — глагол: «предположим, что…»; существительное: предположение, гипотеза.",
                "en": "«假设» — verb: 'to suppose'; noun: hypothesis, supposition.",
            },
            "formula": {"ru": "假设 + предложение",
                        "en": "假设 + clause"},
            "examples": [
                {"zh": "假设我要从国贸到鼓楼大街，该怎么乘车？",
                 "ru": "Предположим, мне нужно от Гомао до улицы Гулоу — как доехать?",
                 "en": "Suppose I want to go from Guomao to Gulou Street — how should I take the bus?"},
                {"zh": "这是一种大胆的假设，但不一定是科学的。",
                 "ru": "Это смелая гипотеза, но не обязательно научная.",
                 "en": "This is a bold hypothesis, but not necessarily scientific."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "__他说的是真话，我们应该怎么办？", "answer": "假设"},
            ],
        },
        {
            "word": "堆", "pos": "m./v./n.",
            "explanation": {
                "ru": "«堆» — счётное слово для куч; глагол «сваливать в кучу»; существительное «куча».",
                "en": "«堆» — measure word for piles; verb 'to pile up'; noun 'heap'.",
            },
            "formula": {"ru": "一大堆 + сущ.; 堆 + 在/到 + место",
                        "en": "一大堆 + noun; 堆 + 在/到 + place"},
            "examples": [
                {"zh": "他准确无误地按顺序报了一大堆公交车、地铁站的名字。",
                 "ru": "Он безошибочно перечислил кучу названий автобусных и метро-станций.",
                 "en": "He accurately listed a pile of bus and subway station names in order."},
                {"zh": "这些零件怎么都堆在这儿啊？",
                 "ru": "Почему эти детали свалены здесь?",
                 "en": "Why are these parts all piled up here?"},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "下雪了，孩子们在院子里__。", "answer": "堆雪人。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "反应", "word_b": "反映",
            "common": {"ru": "同音，都既可做动词又可做名词。",
                       "en": "Homophones; both can be verbs and nouns."},
            "differences": [
                {"ru": "«反应» — реакция на внешний стимул; «反映» — сообщать наверх или отражать сущность.",
                 "en": "«反应» — respond to stimuli; «反映» — report opinions upward or reflect the essence."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "职业、求职", "ru": "Профессии и поиск работы", "en": "Professions and job hunting"},
        "words": [
            {"hanzi": "模特", "pinyin": "mótè", "meaning": {"zh": "", "ru": "модель", "en": "model"}},
            {"hanzi": "会计", "pinyin": "kuàijì", "meaning": {"zh": "", "ru": "бухгалтер", "en": "accountant"}},
            {"hanzi": "秘书", "pinyin": "mìshū", "meaning": {"zh": "", "ru": "секретарь", "en": "secretary"}},
            {"hanzi": "农民", "pinyin": "nóngmín", "meaning": {"zh": "", "ru": "крестьянин", "en": "farmer"}},
            {"hanzi": "工程师", "pinyin": "gōngchéngshī", "meaning": {"zh": "", "ru": "инженер", "en": "engineer"}},
            {"hanzi": "员工", "pinyin": "yuángōng", "meaning": {"zh": "", "ru": "сотрудник", "en": "employee"}},
            {"hanzi": "人事", "pinyin": "rénshì", "meaning": {"zh": "", "ru": "кадры, отдел кадров", "en": "personnel"}},
            {"hanzi": "报到", "pinyin": "bàodào", "meaning": {"zh": "", "ru": "явиться, зарегистрироваться", "en": "to report for duty"}},
            {"hanzi": "失业", "pinyin": "shīyè", "meaning": {"zh": "", "ru": "потерять работу", "en": "unemployment"}},
            {"hanzi": "待遇", "pinyin": "dàiyù", "meaning": {"zh": "", "ru": "условия, зарплата", "en": "treatment, pay"}},
            {"hanzi": "兼职", "pinyin": "jiānzhí", "meaning": {"zh": "", "ru": "подработка", "en": "part-time job"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_28_1.mp3",
             "prompt": {"zh": "他为什么压力很大？", "ru": "Почему у него большой стресс?", "en": "Why is he stressed?"},
             "options": ["乐观", "就业形势不乐观", "专业不好", "工资太低"], "answer": 1},
            {"type": "mc", "audio": "workbook_28_1.mp3",
             "prompt": {"zh": "他得到了什么工作？", "ru": "Какую работу он получил?", "en": "What job did he get?"},
             "options": ["导游", "旅游体验师", "司机", "主持人"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "老总为什么给他那么高的工资？", "ru": "Почему босс дал ему такую высокую зарплату?", "en": "Why did the boss pay him so much?"},
             "options": ["他很幸运", "专业、执着、优秀的人才是无价的", "公司很有钱", "他认识老板"], "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["是", "的", "在", "她的反应", "正常范围内"],
             "answer": "她的反应是在正常范围内的。"},
            {"type": "make_sentence", "words": ["到达了", "代表们", "会场", "陆续", "已经"],
             "answer": "代表们已经陆续到达了会场。"},
            {"type": "short_essay", "words": ["前途", "行业", "体验", "缺乏", "显然"], "min_length": 80},
        ],
    }

    return {
        "title": _t("最受欢迎的毕业生", "Самый популярный выпускник", "", "The most popular graduate", ""),
        "audio_files": {
            "textbook_1": "textbook_28_1.mp3",
            "vocab": "vocab_28.mp3",
            "workbook_28_1": "workbook_28_1.mp3",
            "workbook_28_2": "workbook_28_2.mp3",
        },
        "warmup": {
            "question": _t(
                "如果你是一家公司的老板，需要招聘一名旅游体验师，你对这个职位有什么要求？你会对应聘者提出哪些问题？",
                "Если бы вы были директором компании и вам нужно было нанять туристического эксперта, какие требования вы бы предъявили? Какие вопросы задали бы соискателю?",
                "",
                "If you were a boss hiring a travel experience officer, what requirements would you have? What questions would you ask?",
                ""),
            "answers": [],
        },
        "text_zh": (
            "他叫刘辰，是一个年仅23岁的应届本科毕业生，再过一个月就要毕业了。面对并不乐观的就业形势，他压力很大：“说实话，我觉得自己实在没什么优势。”\n"
            "就在他为工作发愁时，机会来了。天津卫视的《非你莫属》节目组看了他的简历，接受了他的申请，他可以到节目现场去求职。来到现场，他发现，果然有一家公司有适合他的职位——旅游体验师。因为小学六年级的时候，他迷上了公交车，从此，就一直关注公交线路，北京市范围内所有的公交线路他都了如指掌。从上初中起，他就是同学们的出行顾问，无论谁想去哪里，他都能很快地回答出最方便的路线，提供给同学们参考。在他的成长过程中，公交就是他最好的伙伴。\n"
            "节目制作时，电视台问他有什么才艺，他便说：“我是个公交迷，对北京市的公交、地铁线路都有一些研究。”主持人现场考他：“假设我要从国贸到鼓楼大街，该怎么乘车？”他反应得非常快，马上回答说：“在国贸坐1路车，到天安门东，换乘82路，就可以到达。”他的回答让台上的12位老板都兴奋了起来，他们开始陆续向他提问。他有问必答，不但准确无误地按顺序报了一大堆公交车、地铁站的名字，而且还给一对情侣制订了北京休闲一日游的具体方案。\n"
            "他对公交的这种专注显然为他的求职打开了大门。老总们向他发出了热情的邀请，给他非常好的职位和待遇，甚至要专门为他成立有关的部门，只为留住这个人才。最终，他选择了一家他感兴趣的单位。\n"
            "主持人问这家公司的老总：“你给的工资是不是太高了？”这个老总回答：“专业的、执着的、优秀的人才是无价的，这样的人一定会有光明的前途。”是的，无论在哪个行业，最缺乏的永远都是专注的人。专注的人永远不缺机会！"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Лю Чэнь — 23-летний выпускник бакалавриата. Несмотря на сложный рынок труда, благодаря глубокому увлечению автобусными маршрутами Пекина он получил работу мечты — туристического эксперта. Его история показывает: сосредоточенность и уникальные знания всегда востребованы.",
            "tk": "",
            "en": "Liu Chen, a 23-year-old undergraduate facing a tough job market, turned his obsession with Beijing's bus routes into a dream job as a travel experience officer. His story shows that focus and unique knowledge are always in demand.",
            "uz": "",
            "tg": "",
            "id": "",
            "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "话题讨论：找工作。1. 你喜欢“分配工作”还是“双向选择”？为什么？2. 一般的用人单位对员工可能有什么样的要求？3. 你认为自己有什么优势？",
                "Обсуждение: поиск работы. 1. Что вы предпочитаете: распределение или свободный выбор? 2. Какие требования обычно предъявляют работодатели? 3. В чём ваше преимущество?",
                "",
                "Discussion: job hunting. 1. Do you prefer job assignment or two-way selection? 2. What requirements do employers usually have? 3. What are your advantages?",
                ""),
        },
        "workbook": workbook,
    }


# ============================================================
# LESSON 29 — 培养对手
# ============================================================
def lesson29():
    vocab = [
        _vocab("培养", "péiyǎng", "v.", "воспитывать, выращивать, тренировать", "to foster, to train"),
        _vocab("对手", "duìshǒu", "n.", "соперник, конкурент", "opponent, rival"),
        _vocab("公寓", "gōngyù", "n.", "квартира, апартаменты", "apartment, flat"),
        _vocab("文具", "wénjù", "n.", "канцтовары", "stationery"),
        _vocab("电池", "diànchí", "n.", "батарейка", "battery, cell"),
        _vocab("日用品", "rìyòngpǐn", "n.", "товары повседневного спроса", "daily necessities"),
        _vocab("利润", "lìrùn", "n.", "прибыль", "profit"),
        _vocab("诚信", "chéngxìn", "adj.", "честный, добросовестный", "honest, in good faith"),
        _vocab("媒体", "méitǐ", "n.", "СМИ", "media"),
        _vocab("对象", "duìxiàng", "n.", "объект; партнёр", "target, object"),
        _vocab("营业", "yíngyè", "v.", "вести торговлю, работать", "to do business, to operate"),
        _vocab("额", "é", "n.", "сумма, объём", "amount, volume"),
        _vocab("不如", "bùrú", "v.", "уступать, быть хуже", "to be not as good as"),
        _vocab("干脆", "gāncuì", "adv.", "просто, напрямик", "simply, just"),
        _vocab("挤", "jǐ", "v.", "вытеснять, сжимать", "to squeeze out"),
        _vocab("垮", "kuǎ", "v.", "развалиться", "to collapse"),
        _vocab("垄断", "lǒngduàn", "v.", "монополизировать", "to monopolize"),
        _vocab("倒闭", "dǎobì", "v.", "обанкротиться", "to go bankrupt"),
        _vocab("热心", "rèxīn", "adj.", "отзывчивый, горячий", "enthusiastic, earnest"),
        _vocab("资金", "zījīn", "n.", "капитал, средства", "capital, fund"),
        _vocab("傻", "shǎ", "adj.", "глупый", "stupid, foolish"),
        _vocab("倒霉", "dǎoméi", "adj.", "невезучий", "having bad luck"),
        _vocab("生态", "shēngtài", "n.", "экология", "ecology"),
        _vocab("商业", "shāngyè", "n.", "бизнес, коммерция", "business, commerce"),
        _vocab("领域", "lǐngyù", "n.", "сфера, область", "field, domain"),
        _vocab("适当", "shìdàng", "adj.", "подходящий, надлежащий", "proper, adequate"),
        _vocab("促使", "cùshǐ", "v.", "побуждать, способствовать", "to urge, to spur"),
        _vocab("生长", "shēngzhǎng", "v.", "расти", "to grow"),
        _vocab("妨碍", "fáng'ài", "v.", "мешать, препятствовать", "to hinder"),
        _vocab("促进", "cùjìn", "v.", "продвигать, ускорять", "to promote"),
        _vocab("利益", "lìyì", "n.", "интерес, выгода", "benefit, interest"),
        _vocab("合理", "hélǐ", "adj.", "разумный, рациональный", "reasonable"),
        _vocab("万一", "wànyī", "conj.", "если вдруг, в случае", "in case"),
        _vocab("维持", "wéichí", "v.", "поддерживать, сохранять", "to keep, to maintain"),
        _vocab("饱和", "bǎohé", "v.", "насыщенный", "to be saturated"),
        _vocab("不见得", "bùjiàndé", "adv.", "не обязательно, вряд ли", "not necessarily"),
    ]

    grammar = [
        {
            "word": "不如", "pos": "v.",
            "explanation": {
                "ru": "«不如» — глагол: «уступать, быть хуже, чем…».",
                "en": "«不如» — verb: 'to be not as good as, inferior to'.",
            },
            "formula": {"ru": "A 不如 B (+ прилагательное / фраза)",
                        "en": "A 不如 B (+ adjective/phrase)"},
            "examples": [
                {"zh": "三家的营业额加起来还不如他一家高。",
                 "ru": "Суммарный оборот трёх магазинов был ниже, чем у одного его магазина.",
                 "en": "The combined turnover of the three stores was still lower than his one store."},
                {"zh": "求人不如求己。",
                 "ru": "Лучше полагаться на себя, чем просить других.",
                 "en": "It is better to rely on yourself than to ask others."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "与上学期相比，这学期的成绩__。",
                 "answer": "不如上学期。"},
            ],
        },
        {
            "word": "干脆", "pos": "adj./adv.",
            "explanation": {
                "ru": "«干脆» — прилагательное: «прямой, решительный»; наречие: «просто, напрямик».",
                "en": "«干脆» — adjective: 'straightforward, decisive'; adverb: 'simply, just'.",
            },
            "formula": {"ru": "干脆 + глагольная фраза; 他这人很干脆",
                        "en": "干脆 + verb phrase; he is very straightforward"},
            "examples": [
                {"zh": "许多亲朋好友便建议他干脆把另三家书店挤垮。",
                 "ru": "Многие друзья советовали ему просто разорить три других книжных магазина.",
                 "en": "Many friends suggested he simply crush the other three bookstores."},
                {"zh": "我求他帮忙，他答应得很干脆。",
                 "ru": "Я попросил его о помощи — он согласился без колебаний.",
                 "en": "I asked him for help, and he agreed without hesitation."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "这件事你已经考虑了一个月了，__。",
                 "answer": "干脆就这么定了吧。"},
            ],
        },
        {
            "word": "万一", "pos": "conj./n.",
            "explanation": {
                "ru": "«万一» — союз: «если вдруг» (о нежелательном); существительное: маловероятный случай.",
                "en": "«万一» — conjunction: 'in case' (of sth undesirable); noun: unlikely accident.",
            },
            "formula": {"ru": "万一 + предложение; 以防万一; 不怕一万，就怕万一",
                        "en": "万一 + clause; 以防万一; 不怕一万，就怕万一"},
            "examples": [
                {"zh": "万一他们自己跑到其他图书市场去“货比三家”，那我的生意就完了。",
                 "ru": "Если вдруг они пойдут сравнивать цены на другой книжный рынок, мой бизнес пропадёт.",
                 "en": "If by any chance they go to other book markets to compare prices, my business will be ruined."},
                {"zh": "不怕一万，就怕万一。",
                 "ru": "Бережёного Бог бережёт.",
                 "en": "Better safe than sorry."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "我们还是早点出发吧，__。",
                 "answer": "万一路上堵车呢。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "挤", "word_b": "拥挤",
            "common": {"ru": "Оба могут быть глаголом и прилагательным; как прил. означают «тесный».",
                       "en": "Both can be verbs and adjectives; as adjectives they mean 'crowded'."},
            "differences": [
                {"ru": "«挤»: проталкиваться, выдавливать, вытеснять; «拥挤»: быть скученным, тесным; может быть подлежащим/дополнением.",
                 "en": "«挤»: to squeeze through, squeeze out, push out; «拥挤»: to be crowded together; can be subject or object."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "经济1", "ru": "Экономика 1", "en": "Economy 1"},
        "words": [
            {"hanzi": "发票", "pinyin": "fāpiào", "meaning": {"zh": "", "ru": "счёт-фактура, чек", "en": "invoice"}},
            {"hanzi": "收据", "pinyin": "shōujù", "meaning": {"zh": "", "ru": "квитанция", "en": "receipt"}},
            {"hanzi": "支票", "pinyin": "zhīpiào", "meaning": {"zh": "", "ru": "чек", "en": "check"}},
            {"hanzi": "税", "pinyin": "shuì", "meaning": {"zh": "", "ru": "налог", "en": "tax"}},
            {"hanzi": "市场", "pinyin": "shìchǎng", "meaning": {"zh": "", "ru": "рынок", "en": "market"}},
            {"hanzi": "执照", "pinyin": "zhízhào", "meaning": {"zh": "", "ru": "лицензия, патент", "en": "license"}},
            {"hanzi": "柜台", "pinyin": "guìtái", "meaning": {"zh": "", "ru": "прилавок", "en": "counter"}},
            {"hanzi": "商品", "pinyin": "shāngpǐn", "meaning": {"zh": "", "ru": "товар", "en": "goods"}},
            {"hanzi": "优惠", "pinyin": "yōuhuì", "meaning": {"zh": "", "ru": "льготный, скидка", "en": "preferential, discount"}},
            {"hanzi": "讨价还价", "pinyin": "tǎojià-huánjià", "meaning": {"zh": "", "ru": "торговаться", "en": "to bargain"}},
            {"hanzi": "兑换", "pinyin": "duìhuàn", "meaning": {"zh": "", "ru": "обменивать", "en": "to exchange"}},
            {"hanzi": "投资", "pinyin": "tóuzī", "meaning": {"zh": "", "ru": "инвестировать", "en": "to invest"}},
            {"hanzi": "分配", "pinyin": "fēnpèi", "meaning": {"zh": "", "ru": "распределять", "en": "to distribute"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_29_1.mp3",
             "prompt": {"zh": "他为什么帮助竞争对手？", "ru": "Почему он помогает конкурентам?", "en": "Why does he help rivals?"},
             "options": ["他怕他们", "他要保持平衡", "他比他们有钱", "他不会竞争"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "作者认为对手对他有什么影响？", "ru": "Как автор считает, конкуренты влияют на него?", "en": "How does the author think rivals affect him?"},
             "options": ["妨碍他", "促进他", "威胁他", "让他破产"], "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["对", "你不应该", "她的", "拒绝", "合理要求"],
             "answer": "你不应该拒绝她的合理要求。"},
            {"type": "make_sentence", "words": ["我们的", "对手", "不见得", "会妨碍", "发展"],
             "answer": "我们的对手不见得会妨碍发展。"},
            {"type": "short_essay", "words": ["对手", "倒霉", "热心", "促进", "不如"], "min_length": 80},
        ],
    }

    return {
        "title": _t("培养对手", "Воспитывать соперника", "", "Training your rivals", ""),
        "audio_files": {
            "textbook_1": "textbook_29_1.mp3",
            "vocab": "vocab_29.mp3",
            "workbook_29_1": "workbook_29_1.mp3",
            "workbook_29_2": "workbook_29_2.mp3",
        },
        "warmup": {
            "question": _t(
                "请从本课的生词中找出与商业有关的词语，写在下面的横线上，并说说它们分别是什么意思。",
                "Найдите в новых словах слова, связанные с бизнесом, и объясните их значения.",
                "",
                "Find business-related words in this lesson's vocabulary and explain their meanings.",
                ""),
            "answers": ["利润", "诚信", "媒体", "营业", "垄断", "倒闭", "资金", "商业"],
        },
        "text_zh": (
            "建伟在大学的一座公寓楼里开了一家书店，顺便卖点儿文具、电池、小日用品等。一年多来，虽然每件商品的利润都并不高，但他诚信经营，薄利多销，使书店生意越来越红火，甚至成为了媒体的采访对象。这个大学里另外还有三家书店，由于受到了建伟书店的影响，这三家书店的经营空间越来越小，三家的营业额加起来还不如他一家高。建伟成了这里的“书店老大”。\n"
            "这时，许多亲朋好友便建议他干脆把另三家书店挤垮，垄断这个市场。可建伟不但没有去挤垮对手，反而还经常帮助三家书店搞一些营销活动，对于一家快要倒闭的书店，他还主动热心地借给其资金，想办法让他继续经营下去。\n"
            "有人问他：“你怎么这么傻？就让他们倒霉，不好吗？！”\n"
            "建伟说，我是在保持这一地区图书市场的“生态平衡”。商业领域其实和自然界一样，自然界中的生物，适当有一些“敌人”，会促使它们生长得更好；同样的，对手并不会妨碍我的发展，反而会促进经营，让我获得更多利益。一个原因是这样能创造让客户有所比较和优中选优的购物环境，通过比较，学生们才知道我的书店服务好、品种优、价格合理。如果只有我一家书店了，学生们没有了比较，价格定得再低也会认为我的书价高，万一他们自己跑到其他图书市场去“货比三家”，那我的生意就完了。还有一个很重要的原因，就是维持这种书店饱和的“生态”，避免更多、更强的对手来“插足”。我把其他三家都挤垮了，不见得是件好事，因为别人一看这么大的地方只有我一家书店，新的书店可能就会出现，弄不好来一个比我更强的对手。所以，为了保持目前这种经营的“生态平衡”，我要继续把对手培养好。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Цзяньвэй открыл книжный магазин в университетском общежитии. Он не стал разорять конкурентов, а наоборот помогал им, чтобы сохранить «экологический баланс» рынка и избежать появления более сильных соперников.",
            "tk": "",
            "en": "Jianwei opened a bookstore in a university apartment building. Instead of crushing his rivals, he helped them to maintain the market's 'ecological balance' and avoid stronger competitors.",
            "uz": "",
            "tg": "",
            "id": "",
            "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "话题讨论：适者生存。1. 课文中建伟面对不如自己的竞争对手和亲友的建议，他是怎么做的？2. 你同意他的做法吗？3. 如果你是建伟，你会怎么做？",
                "Обсуждение: выживает сильнейший. 1. Как Цзяньвэй поступил с конкурентами? 2. Вы согласны с ним? 3. Что бы вы сделали на его месте?",
                "",
                "Discussion: survival of the fittest. 1. What did Jianwei do? 2. Do you agree? 3. What would you do?",
                ""),
        },
        "workbook": workbook,
    }


# ============================================================
# LESSON 30 — 竞争让市场更高效
# ============================================================
def lesson30():
    vocab = [
        _vocab("沙丁鱼", "shādīngyú", "n.", "сардина", "sardine"),
        _vocab("运输", "yùnshū", "v.", "перевозить, транспортировать", "to transport, to convey"),
        _vocab("岸", "àn", "n.", "берег", "bank, shore"),
        _vocab("商品", "shāngpǐn", "n.", "товар", "goods, commodity"),
        _vocab("延长", "yáncháng", "v.", "продлевать, удлинять", "to prolong, to lengthen"),
        _vocab("存活", "cúnhuó", "v.", "выживать, существовать", "to survive, to exist"),
        _vocab("改善", "gǎishàn", "v.", "улучшать", "to improve"),
        _vocab("无意", "wúyì", "adv.", "непреднамеренно, случайно", "accidentally, inadvertently"),
        _vocab("巧妙", "qiǎomiào", "adj.", "остроумный, искусный", "ingenious, clever"),
        _vocab("实用", "shíyòng", "adj.", "практичный", "practical"),
        _vocab("天敌", "tiāndí", "n.", "естественный враг", "natural enemy"),
        _vocab("鲇鱼", "niányú", "n.", "сом", "catfish"),
        _vocab("设备", "shèbèi", "n.", "оборудование, устройство", "equipment, device"),
        _vocab("和平", "hépíng", "adj.", "мирный", "peaceful"),
        _vocab("构成", "gòuchéng", "v.", "составлять, образовывать", "to compose, to form"),
        _vocab("逃避", "táobì", "v.", "избегать, уклоняться", "to escape, to evade"),
        _vocab("不断", "búduàn", "adv.", "непрерывно, постоянно", "continuously"),
        _vocab("旺盛", "wàngshèng", "adj.", "бурный, цветущий", "exuberant, vibrant"),
        _vocab("比例", "bǐlì", "n.", "пропорция, доля", "proportion, scale"),
        _vocab("感想", "gǎnxiǎng", "n.", "впечатления, мысли", "impressions, thoughts"),
        _vocab("体会", "tǐhuì", "n.", "понимание, ощущение", "feeling, understanding"),
        _vocab("概念", "gàiniàn", "n.", "понятие, концепция", "concept, notion"),
        _vocab("刺激", "cìjī", "v.", "стимулировать, раздражать", "to stimulate, to excite"),
        _vocab("活力", "huólì", "n.", "жизненная сила, энергия", "vigor, vitality"),
        _vocab("落后", "luòhòu", "v.", "отставать", "to fall behind"),
        _vocab("本质", "běnzhì", "n.", "сущность, природа", "essence, nature"),
        _vocab("员工", "yuángōng", "n.", "сотрудник, персонал", "staff, employee"),
        _vocab("危机", "wēijī", "n.", "кризис", "crisis"),
        _vocab("有利", "yǒulì", "adj.", "благоприятный, выгодный", "beneficial, advantageous"),
        _vocab("挖掘", "wājué", "v.", "копать, раскрывать", "to dig, to unearth"),
        _vocab("潜力", "qiánlì", "n.", "потенциал", "potential"),
        _vocab("决赛", "juésài", "n.", "финал", "final, final match"),
        _vocab("接近", "jiējìn", "v.", "приближаться, быть близким", "to approach, to be close to"),
        _vocab("佳", "jiā", "adj.", "хороший, отличный", "good, fine"),
        _vocab("的确", "díquè", "adv.", "действительно, в самом деле", "indeed, really"),
    ]

    grammar = [
        {
            "word": "无意", "pos": "v./adv.",
            "explanation": {
                "ru": "«无意» — глагол: «не желать, не планировать»; наречие: «нечаянно, случайно», часто «无意中……».",
                "en": "«无意» — verb: 'to not intend'; adverb: 'accidentally', often '无意中……'.",
            },
            "formula": {"ru": "无意 + глагол; 无意中 + глагол",
                        "en": "无意 + verb; 无意中 + verb"},
            "examples": [
                {"zh": "后来一位渔民无意中发现了一种巧妙而实用的方法。",
                 "ru": "Позже один рыбак случайно обнаружил остроумный и практичный способ.",
                 "en": "Later a fisherman accidentally discovered a clever and practical method."},
                {"zh": "我无意打扰您，不过我可以跟您谈一会儿吗？",
                 "ru": "Я не хочу вас беспокоить, но можно с вами немного поговорить?",
                 "en": "I don't mean to disturb you, but may I talk with you for a moment?"},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "真对不起！踩到您的脚了，__。",
                 "answer": "我不是无意的。"},
            ],
        },
        {
            "word": "有利", "pos": "adj.",
            "explanation": {
                "ru": "«有利» — прилагательное: «полезный, благоприятный». Часто используется «有利于».",
                "en": "«有利» — adjective: 'beneficial, helpful'. Often used as «有利于».",
            },
            "formula": {"ru": "有利于 + сущ./глагольная фраза; 对……有利",
                        "en": "有利于 + noun/verb phrase; 对……有利"},
            "examples": [
                {"zh": "适度的压力有利于我们保持良好的状态。",
                 "ru": "Умеренное давление помогает нам сохранять хорошее состояние.",
                 "en": "Moderate pressure helps us maintain a good state."},
                {"zh": "笑能促进心肺活动，对睡眠也是有利的。",
                 "ru": "Смех улучшает работу сердца и лёгких и полезен для сна.",
                 "en": "Laughter promotes heart and lung activity and is also beneficial for sleep."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "与电子阅读相比，纸质阅读更__保护眼睛。",
                 "answer": "有利于"},
            ],
        },
        {
            "word": "的确", "pos": "adv.",
            "explanation": {
                "ru": "«的确» — наречие: «действительно, в самом деле». Может удваиваться.",
                "en": "«的确» — adverb: 'indeed, really'. Can be reduplicated.",
            },
            "formula": {"ru": "的确 + прилагательное / глагольная фраза",
                        "en": "的确 + adjective/verb phrase"},
            "examples": [
                {"zh": "“鲇鱼效应”的确对挖掘员工潜力、提高企业活力具有积极的意义。",
                 "ru": "«Эффект сома» действительно играет положительную роль в раскрытии потенциала сотрудников.",
                 "en": "The 'catfish effect' indeed has positive significance for tapping employee potential."},
                {"zh": "他的确是我所教过的学生中最聪明的。",
                 "ru": "Он действительно самый умный из моих учеников.",
                 "en": "He is indeed the smartest student I have ever taught."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "丽丽的歌声优美动人，听她唱歌__。",
                 "answer": "的确是一种享受。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "接近", "word_b": "靠近",
            "common": {"ru": "Оба глаголы, означают «быть близко или приближаться»; иногда взаимозаменяемы.",
                       "en": "Both verbs mean 'to be close or move closer'; sometimes interchangeable."},
            "differences": [
                {"ru": "«接近»: сочетается с конкретными и абстрактными объектами, временем, числом; «靠近»: обычно не со временем/числом/абстрактным.",
                 "en": "«接近»: with concrete/abstract things, time, number; «靠近»: generally not with time, number, or abstract things."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "经济2", "ru": "Экономика 2", "en": "Economy 2"},
        "words": [
            {"hanzi": "出口", "pinyin": "chūkǒu", "meaning": {"zh": "", "ru": "экспорт", "en": "export"}},
            {"hanzi": "进口", "pinyin": "jìnkǒu", "meaning": {"zh": "", "ru": "импорт", "en": "import"}},
            {"hanzi": "贸易", "pinyin": "màoyì", "meaning": {"zh": "", "ru": "торговля", "en": "trade"}},
            {"hanzi": "谈判", "pinyin": "tánpàn", "meaning": {"zh": "", "ru": "переговоры", "en": "negotiation"}},
            {"hanzi": "合同", "pinyin": "hétong", "meaning": {"zh": "", "ru": "контракт", "en": "contract"}},
            {"hanzi": "中介", "pinyin": "zhōngjiè", "meaning": {"zh": "", "ru": "посредник", "en": "intermediary"}},
            {"hanzi": "破产", "pinyin": "pòchǎn", "meaning": {"zh": "", "ru": "обанкротиться", "en": "bankruptcy"}},
            {"hanzi": "资金", "pinyin": "zījīn", "meaning": {"zh": "", "ru": "капитал, средства", "en": "capital, fund"}},
            {"hanzi": "利润", "pinyin": "lìrùn", "meaning": {"zh": "", "ru": "прибыль", "en": "profit"}},
            {"hanzi": "股票", "pinyin": "gǔpiào", "meaning": {"zh": "", "ru": "акции", "en": "stock"}},
            {"hanzi": "账户", "pinyin": "zhànghù", "meaning": {"zh": "", "ru": "счёт (банковский)", "en": "account"}},
            {"hanzi": "利息", "pinyin": "lìxī", "meaning": {"zh": "", "ru": "проценты", "en": "interest"}},
            {"hanzi": "贷款", "pinyin": "dàikuǎn", "meaning": {"zh": "", "ru": "кредит, ссуда", "en": "loan"}},
            {"hanzi": "汇率", "pinyin": "huìlǜ", "meaning": {"zh": "", "ru": "валютный курс", "en": "exchange rate"}},
            {"hanzi": "押金", "pinyin": "yājīn", "meaning": {"zh": "", "ru": "залог, депозит", "en": "deposit"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_30_1.mp3",
             "prompt": {"zh": "为什么要让沙丁鱼活着？", "ru": "Почему сардины нужно перевозить живыми?", "en": "Why must sardines be transported alive?"},
             "options": ["为了好玩", "为了卖更高的价钱", "为了放生", "为了养殖"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "“鲇鱼效应”是什么意思？", "ru": "Что означает «эффект сома»?", "en": "What does the 'catfish effect' mean?"},
             "options": [" рыбный бизнес", "стимул для развития", "морская история", "экономический закон"],
             "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["无意中", "这些话", "事实", "他的", "接近了"],
             "answer": "他的话无意中接近了事实。"},
            {"type": "make_sentence", "words": ["活跃起来", "采取", "刺激企业", "必须", "措施"],
             "answer": "必须采取措施刺激企业活跃起来。"},
            {"type": "short_essay", "words": ["决赛", "感想", "刺激", "延长", "落后"], "min_length": 80},
        ],
    }

    return {
        "title": _t("竞争让市场更高效", "Конкуренция делает рынок эффективнее", "", "Competition makes the market more efficient", ""),
        "audio_files": {
            "textbook_1": "textbook_30_1.mp3",
            "vocab": "vocab_30.mp3",
            "workbook_30_1": "workbook_30_1.mp3",
            "workbook_30_2": "workbook_30_2.mp3",
        },
        "warmup": {
            "question": _t(
                "请试着找出本课和你知道的跟“竞争”有关的词语，写在下面的横线上，并说说你选这些词的道理。",
                "Найдите слова, связанные с конкуренцией, и объясните свой выбор.",
                "",
                "Find words related to competition and explain your choices.",
                ""),
            "answers": ["刺激", "活力", "潜力", "危机感", "落后", "决赛"],
        },
        "text_zh": (
            "西班牙人特别喜欢吃沙丁鱼。但沙丁鱼对离开大海后的环境极不适应，运输就成了问题。鱼上岸后，过不了多久就会死去。而死掉的沙丁鱼口感很差，作为商品销售，价格就会便宜很多。如果上岸时沙丁鱼还活着，鱼卖价可以涨很多倍。\n"
            "为了延长沙丁鱼的存活期，减少经济损失，渔民们想了很多办法，但情况仍然没有得到太大的改善。后来一位渔民无意中发现了一种巧妙而实用的方法：把几条沙丁鱼的天敌鲇鱼放进装鱼的设备中。因为鲇鱼是食肉鱼，无法和沙丁鱼和平共处，它会四处游动寻找小鱼吃，对沙丁鱼构成威胁。为了逃避天敌，沙丁鱼自然会不断地加速游动，从而保持了旺盛的生命力，存活的比例大大提高。\n"
            "看到这里，你有什么感想和体会呢？其实，这在经济学上被称为“鲇鱼效应”。“鲇鱼效应”对于市场经济以及现代企业管理都有着重要的启发作用。这个概念的核心是：一个市场如果能采取一种措施，刺激企业活跃起来，就能使企业获得足够的活力，在市场中积极参与竞争而不至于落后，同时这样反过来又能促使市场更为高效。\n"
            "从本质上说，“鲇鱼效应”使得企业和员工产生一种危机感，其实就是一种压力效应。很多研究发现，适度的压力有利于我们保持良好的状态，更加有助于挖掘我们的潜力，从而提高个人的工作效率。比如运动员每到参加比赛，尤其是决赛时，一定要将自己调整到接近最佳状态，让自己感到适度的压力，如果他不紧张、没压力感，则不利于出成绩。因此，“鲇鱼效应”的确对挖掘员工潜力、提高企业活力具有积极的意义。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Испанцы любят сардины, но их трудно перевозить живыми. Однажды рыбак добавил в ёмкость с сардинами их естественного врага — сома, и сардины, спасаясь, стали активнее, что повысило их выживаемость. Это явление назвали «эффектом сома» — оно применимо и к рыночной экономике.",
            "tk": "",
            "en": "Spaniards love sardines, but transporting them alive is difficult. A fisherman put catfish, their natural enemy, into the tank; the sardines became more active and survived better. This is the 'catfish effect', which also applies to market economics.",
            "uz": "",
            "tg": "",
            "id": "",
            "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "话题讨论：你喜欢竞争吗？1. 请列举一些生活中的实例，说明竞争给我们带来的好处。2. 你有过在竞争中失败的经历吗？说说它对你有何影响。3. 如果竞争是不可避免的，你认为应该如何面对？",
                "Обсуждение: любите ли вы конкуренцию? 1. Приведите примеры её пользы. 2. Был ли у вас опыт поражения? 3. Как следует относиться к конкуренции?",
                "",
                "Discussion: Do you like competition? 1. Give examples of its benefits. 2. Have you failed in competition? 3. How should we face competition?",
                ""),
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(10, 28, lesson28())
    save(10, 29, lesson29())
    save(10, 30, lesson30())
    print("Done.")