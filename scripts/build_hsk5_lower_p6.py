# -*- coding: utf-8 -*-
"""Уроки 31-33 (Unit 11 — 观察社会)."""
from build_hsk5_lower import _vocab, _t, save


def lesson31():
    vocab = [
        _vocab("门槛", "ménkǎn", "n.", "порог", "threshold"),
        _vocab("报社", "bàoshè", "n.", "редакция газеты", "newspaper office"),
        _vocab("编辑", "biānjí", "n.", "редактор", "editor"),
        _vocab("嗯", "ng", "int.", "м-м (междометие)", "used to indicate positive response"),
        _vocab("轻易", "qīngyì", "adj.", "легко, запросто", "easy, effortless"),
        _vocab("处理", "chǔlǐ", "v.", "обрабатывать, улаживать", "to handle, to deal with"),
        _vocab("社区", "shèqū", "n.", "микрорайон, сообщество", "community"),
        _vocab("劝", "quàn", "v.", "убеждать, уговаривать", "to try to persuade"),
        _vocab("圆", "yuán", "adj.", "круглый", "round, circular"),
        _vocab("标志", "biāozhì", "n.", "знак, символ", "sign, mark"),
        _vocab("出示", "chūshì", "v.", "предъявлять, показывать", "to show, to produce"),
        _vocab("赞成", "zànchéng", "v.", "одобрять, поддерживать", "to agree with, to approve of"),
        _vocab("请愿书", "qǐngyuànshū", "n.", "петиция", "petition"),
        _vocab("恋爱", "liàn'ài", "n.", "любовь, влюблённость", "romantic love"),
        _vocab("迫切", "pòqiè", "adj.", "настоятельный, срочный", "urgent, pressing"),
        _vocab("犹豫", "yóuyù", "adj.", "колеблющийся", "hesitant"),
        _vocab("冷淡", "lěngdàn", "adj.", "холодный, равнодушный", "cold, indifferent"),
        _vocab("无所谓", "wúsuǒwèi", "v.", "безразлично, не важно", "to not care, to not mind"),
        _vocab("值班", "zhíbān", "v.", "дежурить", "to be on duty"),
        _vocab("报告", "bàogào", "n.", "доклад, отчёт", "report"),
        _vocab("八成", "bāchéng", "adv.", "скорее всего, вероятно", "most probably"),
        _vocab("模糊", "móhu", "adj.", "размытый, нечёткий", "blurred, vague"),
        _vocab("狡猾", "jiǎohuá", "adj.", "хитрый, лукавый", "crafty, cunning"),
        _vocab("了不起", "liǎobùqǐ", "adj.", "выдающийся, потрясающий", "great, amazing"),
        _vocab("身段", "shēnduàn", "n.", "осанка, позиция", "posture, manner"),
        _vocab("缩短", "suōduǎn", "v.", "сокращать, укорачивать", "to shorten"),
        _vocab("看不起", "kànbuqǐ", "v.", "смотреть свысока, презирать", "to look down upon"),
        _vocab("谦虚", "qiānxū", "adj.", "скромный", "modest"),
        _vocab("实践", "shíjiàn", "v.", "практиковать, применять", "to put into practice"),
    ]

    grammar = [
        {
            "word": "嗯", "pos": "int.",
            "explanation": {"ru": "«嗯» — междометие. Употребляется как согласие, удивление или вопрос, в зависимости от тона.",
                            "en": "«嗯» is an interjection. Depending on the tone, it means agreement, surprise, or a question."},
            "formula": {"ru": "嗯 + 小句", "en": "嗯 + clause"},
            "examples": [
                {"zh": "嗯，如果您心情好，我就说件事；心情不好就改天再说。",
                 "ru": "М-м, если у вас хорошее настроение — я кое-что скажу; если плохое — поговорим в другой раз.",
                 "en": "Mm, if you're in a good mood, I'll say something; if not, we'll talk another day."},
                {"zh": "嗯？不是28号，难道是我记错了？",
                 "ru": "М-м? Не 28-е — может, я ошибся?",
                 "en": "Hm? Not the 28th — did I remember wrong?"},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "__我记住了，明天给你发邮件。", "answer": "嗯"},
            ],
        },
        {
            "word": "轻易", "pos": "adj./adv.",
            "explanation": {"ru": "«轻易» — прилагательное: «легко, без усилий»; наречие: «необдуманно, поспешно». Часто в отрицании «轻易不...» = «редко».",
                            "en": "«轻易» — adj.: 'easy, effortless'; adv.: 'rashly'. In the negative «轻易不...» = 'rarely'."},
            "formula": {"ru": "轻易 + 动词", "en": "轻易 + verb"},
            "examples": [
                {"zh": "领导有了兴趣，假，就这样轻易地请好了。",
                 "ru": "Начальник заинтересовался — и отгул так легко был получен.",
                 "en": "The boss got interested — and the leave was granted just like that."},
                {"zh": "他这个人的特点，是从不轻易决定，也不轻易转变。",
                 "ru": "Его черта — никогда не решать поспешно и не менять мнение легко.",
                 "en": "His trait is never deciding rashly or changing easily."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "爸，天这么热，你们怎么不开空调啊？——我们__开空调。",
                 "answer": "轻易不"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "轻易", "word_b": "容易",
            "common": {"ru": "Как прилагательные оба означают, что что-то делается без усилий.",
                       "en": "As adjectives both mean doing something without effort."},
            "differences": [
                {"ru": "«轻易» делает акцент на лёгкости действия, обычно в роли обстоятельства; «容易» — на простоте содержания, может быть сказуемым.",
                 "en": "«轻易» focuses on ease of action, usually adverbial; «容易» — on simplicity, can be a predicate."},
                {"ru": "«容易» также означает «вероятно, легко может случиться» — «容易发脾气». «轻易» так не используется.",
                 "en": "«容易» also means 'likely to happen' — 容易发脾气. «轻易» cannot be used this way."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "行为1", "ru": "Поведение 1", "en": "Behavior 1"},
        "words": [
            {"hanzi": "插", "pinyin": "chā", "meaning": {"zh": "", "ru": "вставлять", "en": "to insert"}},
            {"hanzi": "捶", "pinyin": "chuí", "meaning": {"zh": "", "ru": "стучать кулаком", "en": "to pound"}},
            {"hanzi": "瞪", "pinyin": "dèng", "meaning": {"zh": "", "ru": "уставиться, сверлить взглядом", "en": "to stare"}},
            {"hanzi": "抚摸", "pinyin": "fǔmō", "meaning": {"zh": "", "ru": "гладить, ласкать", "en": "to stroke"}},
            {"hanzi": "搂", "pinyin": "lǒu", "meaning": {"zh": "", "ru": "обнимать, обхватывать", "en": "to hug"}},
            {"hanzi": "爬", "pinyin": "pá", "meaning": {"zh": "", "ru": "ползти, взбираться", "en": "to crawl, to climb"}},
            {"hanzi": "抛", "pinyin": "pāo", "meaning": {"zh": "", "ru": "бросать, подкидывать", "en": "to throw"}},
            {"hanzi": "扔", "pinyin": "rēng", "meaning": {"zh": "", "ru": "швырять", "en": "to throw away"}},
            {"hanzi": "踢", "pinyin": "tī", "meaning": {"zh": "", "ru": "пинать, бить ногой", "en": "to kick"}},
            {"hanzi": "握", "pinyin": "wò", "meaning": {"zh": "", "ru": "сжимать (в руке)", "en": "to grasp"}},
            {"hanzi": "握", "pinyin": "wò", "meaning": {"zh": "", "ru": "сжимать", "en": "to hold"}},
            {"hanzi": "砸", "pinyin": "zá", "meaning": {"zh": "", "ru": "разбивать, обрушивать", "en": "to smash"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_31_1.mp3",
             "prompt": {"zh": "女的是什么意思？", "ru": "Что имеет в виду женщина?", "en": "What does the woman mean?"},
             "options": ["很关心", "无所谓", "坚决反对", "有点儿犹豫"], "answer": 3},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "「登门槛效应」是什么意思？", "ru": "Что такое «эффект ноги в двери»?", "en": "What is the foot-in-the-door effect?"},
             "options": ["要先拒绝", "先小后大", "先大后小", "拒绝到底"], "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["能", "一点儿", "老师", "谦虚", "希望我"],
             "answer": "老师希望我能谦虚一点儿。"},
            {"type": "make_sentence", "words": ["请", "填写", "并出示", "这张表格", "您的护照"],
             "answer": "请填写这张表格并出示您的护照。"},
            {"type": "short_essay", "words": ["态度", "冷淡", "赞成", "无所谓", "犹豫"], "min_length": 80},
        ],
    }

    return {
        "title": _t("登门槛效应", "Эффект «ноги в двери»", "", "Foot-in-the-door effect", ""),
        "audio_files": {
            "textbook_1": "textbook_31_1.mp3",
            "vocab": "vocab_31.mp3",
            "workbook_31_1": "workbook_31_1.mp3",
        },
        "warmup": {
            "question": _t(
                "如果你想请别人帮你做件事情，又担心对方不愿意，你一般会考虑哪些问题？你会以何种方式向对方提出请求呢？",
                "Если вы хотите попросить кого-то о помощи и боитесь отказа — о чём вы обычно думаете? Как вы формулируете просьбу?",
                "",
                "If you want to ask someone for help but worry they'll refuse — what do you usually consider? How do you phrase your request?",
                ""),
            "answers": ["接受"],
        },
        "text_zh": (
            "一个朋友在报社当编辑。一天他去请假，他先问领导：“您今天心情好吗？”领导说：“怎么了？”朋友答：“嗯，如果您心情好，我就说件事；心情不好就改天再说。”领导有了兴趣，假，就这样轻易地请好了。\n"
            "不得不说，这位朋友很会利用“登门槛效应”来处理问题。\n"
            "心理学家曾做过“登门槛技术”的现场实验。他们派人到两个社区，劝人们在屋前立一块“小心驾驶”的圆形标志。在第一个社区，研究人员直接向人们提出要求，结果很多人表示拒绝，接受率仅为17%。在第二个社区，研究人员把同样的事情分成两个步骤：先向大家出示一份赞成安全驾驶的请愿书，请求他们在上面签字，几周后再提出立牌要求，这次接受者竟然达到了55%。第一个步骤的签字是很容易的，几乎所有人都照做了，大家可能都没意识到，这个小小的“登门槛行为”对接下来的决定产生了重要影响。\n"
            "日常生活中也是这样。当你想要求某人做某件较大的事情，又担心对方不愿意做时，可以先向他/她提出做一件同类型的、比较容易的事。比如你想与一个女孩谈恋爱，如果一开始就迫切地提出要跟她约会，女孩可能会犹豫，甚至表现得很冷淡；如果你说“饭总是要吃的吧，一起吃饭吧”，她答应了，那接下来是去看电影还是泡酒吧都无所谓了。你想让同事帮你值班或写报告什么的，直接说八成儿会被拒绝，把事情模糊化，“能不能帮个小忙”，“不会占用你很多时间”，台阶一铺，事情就容易多了……\n"
            "你可能会说，这些小动作会让人觉得你很狡猾。但是不得不承认，有了这些小动作的帮助，别人的确更愿意接受你的请求。有时候，当你自认为了不起时，别人通常觉得你这人不过如此；可是当你放低身段时，会缩短与人的距离，别人并不会看不起你，反而会觉得你为人谦虚。实践证明，第二种人得到的总是比第一种人更多。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "У одного моего друга — редактора в газете — был случай с отгулом. Он сначала спросил у начальника про настроение, потом сказал, что если оно хорошее — он кое-что скажет. Начальник заинтересовался, и отгул получил легко. Это — «эффект ноги в двери»: сначала маленькая просьба, потом большая. Психологи ставили эксперименты: если сначала попросить подписать петицию, а потом разрешить поставить знак «Внимание! Дорога!» — процент согласившихся резко растёт. В быту так же: девушке проще согласиться пойти поесть, а потом уже и в кино; коллеге проще «маленькую просьбу» выполнить, чем сразу большой отчёт. Эти маленькие хитрости кажутся лукавыми, но они реально помогают — и когда человек «спускается с высоты», с ним приятнее иметь дело.",
            "tk": "",
            "en": "A friend of mine, an editor at a newspaper, had a story about asking for leave. He first asked his boss about his mood — and if the mood was good, he'd say something. The boss got interested, and the leave was easily granted. This is the “foot-in-the-door effect”: start with a small request, then go bigger. Psychologists have done field experiments: if you first ask people to sign a petition, and later to allow a sign 'Drive Carefully!' — the acceptance rate jumps dramatically. In daily life too: it's easier for a girl to say yes to a meal than to a date, and for a colleague to do 'a small favour' than a big report. These little tricks may seem crafty, but they work — and when you step down from your pedestal, people are more willing to help.",
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
                "话题讨论：交往之道——接受与拒绝。1. 你觉得帮助别人对你会有影响吗？2. 介绍你拒绝别人的一次经历，那是什么事？3. 在与人交往中，你处理“接受与拒绝”的原则是什么？",
                "Обсуждение: как принимать и отказывать. 1. Помощь другим влияет на вас? 2. Расскажите случай, когда вы отказали. 3. Какие у вас принципы в этом?",
                "",
                "Discussion: accepting and refusing. 1. Does helping others affect you? 2. Tell about a time you refused. 3. What are your principles?",
                ""),
        },
        "workbook": workbook,
    }


def lesson32():
    vocab = [
        _vocab("消失", "xiāoshī", "v.", "исчезать", "to disappear, to vanish"),
        _vocab("洪水", "hóngshuǐ", "n.", "наводнение", "flood"),
        _vocab("地震", "dìzhèn", "n.", "землетрясение", "earthquake"),
        _vocab("破坏", "pòhuài", "v.", "разрушать, ломать", "to destroy, to damage"),
        _vocab("砍", "kǎn", "v.", "рубить, срубать", "to cut, to chop, to fell"),
        _vocab("生存", "shēngcún", "v.", "существовать, выживать", "to live, to subsist"),
        _vocab("沙漠", "shāmò", "n.", "пустыня", "desert"),
        _vocab("公布", "gōngbù", "v.", "объявлять, публиковать", "to announce, to make public"),
        _vocab("数据", "shùjù", "n.", "данные", "data"),
        _vocab("真实", "zhēnshí", "adj.", "реальный, истинный", "real, actual"),
        _vocab("夸张", "kuāzhāng", "adj.", "преувеличенный", "exaggerated"),
        _vocab("资源", "zīyuán", "n.", "ресурсы", "resource"),
        _vocab("车祸", "chēhuò", "n.", "автокатастрофа", "traffic accident"),
        _vocab("不安", "bù'ān", "adj.", "тревожный, беспокойный", "upset, disturbed"),
        _vocab("工业", "gōngyè", "n.", "промышленность", "industry"),
        _vocab("农业", "nóngyè", "n.", "сельское хозяйство", "agriculture"),
        _vocab("生产", "shēngchǎn", "v.", "производить", "to produce, to manufacture"),
        _vocab("大型", "dàxíng", "adj.", "крупномасштабный", "large-scale"),
        _vocab("工厂", "gōngchǎng", "n.", "фабрика, завод", "factory"),
        _vocab("废", "fèi", "adj.", "отработанный, ненужный", "waste, useless"),
        _vocab("燃烧", "ránshāo", "v.", "гореть, сжигать", "to burn, to combust"),
        _vocab("煤炭", "méitàn", "n.", "уголь", "coal"),
        _vocab("密切", "mìqiè", "adj.", "тесный, близкий", "close, intimate"),
        _vocab("尾气", "wěiqì", "n.", "выхлопные газы", "exhaust gas"),
        _vocab("幸运", "xìngyùn", "adj.", "удачливый, счастливый", "lucky, fortunate"),
        _vocab("敏感", "mǐngǎn", "adj.", "чувствительный, восприимчивый", "sensitive, susceptible"),
        _vocab("自觉", "zìjué", "adj.", "сознательный", "conscious, on one's own initiative"),
        _vocab("设施", "shèshī", "n.", "оборудование, инфраструктура", "installation, facilities"),
        _vocab("能源", "néngyuán", "n.", "энергоресурсы", "energy resource"),
        _vocab("逐步", "zhúbù", "adv.", "постепенно, шаг за шагом", "gradually, step by step"),
        _vocab("尽量", "jǐnliàng", "adv.", "по возможности, стараться", "to the best of one's abilities"),
        _vocab("私人", "sīrén", "n.", "частное лицо; личный", "private"),
        _vocab("尊敬", "zūnjìng", "v.", "уважать", "to respect, to esteem"),
        _vocab("鼓舞", "gǔwǔ", "v.", "воодушевлять", "to encourage, to inspire"),
        _vocab("消极", "xiāojí", "adj.", "пассивный, негативный", "passive, inactive"),
        _vocab("幻想", "huànxiǎng", "n.", "иллюзия, фантазия", "fantasy, illusion"),
        _vocab("贡献", "gòngxiàn", "n.", "вклад", "contribution"),
        _vocab("命运", "mìngyùn", "n.", "судьба", "fate, destiny"),
        _vocab("掌握", "zhǎngwò", "v.", "владеть, управлять", "to take charge of, to control"),
    ]

    grammar = [
        {
            "word": "密切", "pos": "adj./v.",
            "explanation": {"ru": "«密切» — прилагательное: «тесно связанный, близкий»; также «внимательный, тщательный»; глагол: «сближать, делать теснее».",
                            "en": "«密切» — adj.: 'closely related, close'; also 'attentive'; verb: 'to bring closer'."},
            "formula": {"ru": "和/与……密切相关；密切地 + 动词", "en": "和/与...密切相关；密切地 + verb"},
            "examples": [
                {"zh": "还有一部分污染和我们的日常生活密切相关，汽车尾气就是其中之一。",
                 "ru": "Часть загрязнения тесно связана с нашей повседневной жизнью — выхлопные газы тому пример.",
                 "en": "Part of the pollution is closely tied to daily life — car exhaust is one example."},
                {"zh": "刘医生密切地观察着李妈妈病情的发展。",
                 "ru": "Доктор Лю внимательно следил за развитием болезни мамы Ли.",
                 "en": "Dr. Liu closely monitored the development of Mama Li's illness."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "这种病传染性很强，__。", "answer": "要密切注意。"},
            ],
        },
        {
            "word": "尽量", "pos": "adv.",
            "explanation": {"ru": "«尽量» — наречие: «стараться изо всех сил, по возможности».",
                            "en": "«尽量» — adverb: 'to the best of one's ability, as much as possible'."},
            "formula": {"ru": "尽量 + 动词", "en": "尽量 + verb"},
            "examples": [
                {"zh": "同时，尽量多骑自行车，多选择公共交通，少使用私家车。",
                 "ru": "И стараться больше ездить на велосипеде, пользоваться общественным транспортом, меньше — личным автомобилем.",
                 "en": "Also try to cycle more, use public transport more, and use private cars less."},
                {"zh": "老年人要尽量少吃油炸食品。",
                 "ru": "Пожилым людям следует по возможности избегать жареной еды.",
                 "en": "Elderly people should eat as little fried food as possible."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "明天单位有个活动，可能不能按时下班，__。",
                 "answer": "我会尽量早点回来。"},
            ],
        },
        {
            "word": "逐步", "pos": "adv.",
            "explanation": {"ru": "«逐步» — наречие: «шаг за шагом, постепенно». Обычно о действиях человека, не о природных явлениях.",
                            "en": "«逐步» — adverb: 'step by step, gradually'. Usually about human actions, not natural phenomena."},
            "formula": {"ru": "逐步 + 动词", "en": "逐步 + verb"},
            "examples": [
                {"zh": "调整能源消费结构，逐步向可再生能源转变。",
                 "ru": "Скорректировать структуру энергопотребления и постепенно перейти к возобновляемым источникам.",
                 "en": "Adjust the energy consumption structure and gradually shift to renewables."},
                {"zh": "现在受灾群众已逐步恢复了正常的生产生活。",
                 "ru": "Сейчас пострадавшие постепенно восстановили нормальную жизнь и производство.",
                 "en": "The affected people have gradually resumed normal life and work."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "随着人们生活水平的不断提高，绿色食品__。",
                 "answer": "逐步走进了普通家庭。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "鼓励", "word_b": "鼓舞",
            "common": {"ru": "Оба глагола значат «воодушевлять, укреплять веру».",
                       "en": "Both verbs mean 'to encourage, to boost one's spirits'."},
            "differences": [
                {"ru": "«鼓励» — нейтральное, может использоваться и в негативном контексте; субъект — обычно человек или организация, конструкция «鼓励某人做某事».",
                 "en": "«鼓励» — neutral, can be used negatively; subject is usually a person or organization; pattern «鼓励某人做某事»."},
                {"ru": "«鼓舞» — о воодушевлении от какого-то события; подлежащее — обычно абстрактное (победа, успех).",
                 "en": "«鼓舞» — inspiration from an event; subject is usually abstract (a victory, success)."},
                {"ru": "«鼓舞» также может быть прилагательным: «令人鼓舞».",
                 "en": "«鼓舞» can also be an adjective: 令人鼓舞."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "资源", "ru": "Ресурсы", "en": "Resources"},
        "words": [
            {"hanzi": "金属", "pinyin": "jīnshǔ", "meaning": {"zh": "", "ru": "металл", "en": "metal"}},
            {"hanzi": "黄金", "pinyin": "huángjīn", "meaning": {"zh": "", "ru": "золото", "en": "gold"}},
            {"hanzi": "银", "pinyin": "yín", "meaning": {"zh": "", "ru": "серебро", "en": "silver"}},
            {"hanzi": "钢铁", "pinyin": "gāngtiě", "meaning": {"zh": "", "ru": "сталь", "en": "steel"}},
            {"hanzi": "煤炭", "pinyin": "méitàn", "meaning": {"zh": "", "ru": "уголь", "en": "coal"}},
            {"hanzi": "能源", "pinyin": "néngyuán", "meaning": {"zh": "", "ru": "энергоресурсы", "en": "energy resource"}},
            {"hanzi": "原料", "pinyin": "yuánliào", "meaning": {"zh": "", "ru": "сырьё", "en": "raw material"}},
            {"hanzi": "资源", "pinyin": "zīyuán", "meaning": {"zh": "", "ru": "ресурсы", "en": "resources"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_32_1.mp3",
             "prompt": {"zh": "环境污染有什么危害？", "ru": "Какой вред наносит загрязнение?", "en": "What harm does pollution do?"},
             "options": ["危害动植物和人类", "只是视觉问题", "与人类无关", "只影响城市"], "answer": 0},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "作者对环保的态度是什么？", "ru": "Какова позиция автора об охране окружающей среды?", "en": "What is the author's attitude to environmental protection?"},
             "options": ["悲观", "无所谓", "积极", "愤怒"], "answer": 2},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["爱护环境", "父母", "要", "教育他", "从小就"],
             "answer": "父母要从小就教育他爱护环境。"},
            {"type": "make_sentence", "words": ["这样", "逐步", "良好的习惯", "形成一些", "才能"],
             "answer": "这样才能逐步形成一些良好的习惯。"},
            {"type": "short_essay", "words": ["环保", "掌握", "自觉", "破坏", "贡献"], "min_length": 80},
        ],
    }

    return {
        "title": _t("身边的环保", "Экология вокруг нас", "", "Protecting the environment around us", ""),
        "audio_files": {
            "textbook_1": "textbook_32_1.mp3",
            "vocab": "vocab_32.mp3",
            "workbook_32_1": "workbook_32_1.mp3",
        },
        "warmup": {
            "question": _t(
                "结合图片，请你举例说明人类对环境的破坏造成了哪些恶劣的影响。当我们谈论环境遭到污染和破坏时，常常提到哪些词语？",
                "По картинке: приведите примеры того, какой вред наносит человек природе. Какие слова мы часто используем, когда говорим о загрязнении?",
                "",
                "Look at the picture and give examples of the damage humans do to the environment. What words do we often use when talking about pollution?",
                ""),
            "answers": ["破坏"],
        },
        "text_zh": (
            "如果你觉得地球上的一点儿小污染没什么关系，那你可就大错特错了！环境污染会危害动物、植物以及人类自身。\n"
            "有些生活在过去的动物，你今天再也看不到了，植物也面临着同样的危险。动植物的消失，部分原因是由于自然界的变化，比如洪水、地震等改变了它们生活的环境，但更大的原因则是人类对自然的破坏——有些地区的森林已经几乎被人砍光了，很多河流被污染，不再适合鱼类生存，有的地区原本是草原，如今已变为沙漠……从国际环保组织公布的数据可知，地球上一半以上的动植物正在消失，这是真实的情况，一点儿也不夸张。人类自身也饱受污染的危害。有些地区地表水已污染，地下水又被过量使用，水资源短缺问题就连科学家们也不知道该如何解决，目前世界上有17%的人无法享用干净的饮用水，而每年死于与空气污染有关的疾病的人比死于车祸的还要多。这些数据确实令人不安。\n"
            "一部分环境污染是由工业农业生产活动造成的，例如，大型工厂生产过程中，有的会产生大量废水；有的要大量燃烧煤炭，从而产生大量废气和废物。还有一部分污染和我们的日常生活密切相关，汽车尾气就是其中之一。此外，垃圾也会对环境造成严重的损害。\n"
            "幸运的是，越来越多的人敏感地认识到了环境问题的严重，并自觉地投入到了保护地球的行动中。生产中，增加环保设施，减少污染物排放，调整能源消费结构，逐步向可再生能源转变；而在日常生活中，改变生活习惯，尽量减少生活垃圾，做到垃圾分类。同时，尽量多骑自行车，多选择公共交通，少使用私家车。这些为此付出努力的人们令人尊敬，取得的成绩也令人鼓舞。\n"
            "地球是人类共同的家园，我们应该把它看作一个属于自己的大房间。房间脏了，消极的逃避和不符合实际的幻想都不能解决问题，为保持它的卫生每一个人都应付出行动，做出贡献。人类的命运由我们自己掌握，改变要靠我们自己。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Если вам кажется, что немного загрязнения — это не страшно, вы сильно ошибаетесь. Загрязнение вредит животным, растениям и самому человеку. Многие виды исчезают, леса вырубаются, реки загрязнены, степи превращаются в пустыни. По данным экологов, больше половины видов флоры и фауны на планете исчезают — это не преувеличение. 17% людей на Земле не имеют доступа к чистой питьевой воде, а от болезней, связанных с загрязнением воздуха, умирает больше людей, чем в ДТП. Часть загрязнений — от промышленности и сельского хозяйства, часть — от повседневной жизни: выхлопные газы, мусор. Но есть и хорошая новость: всё больше людей ответственно относятся к экологии, внедряют экологические технологии, сортируют мусор, выбирают велосипед и общественный транспорт. Земля — наш общий дом, и судьба её в наших руках.",
            "tk": "",
            "en": "If you think a little pollution on Earth is no big deal — you're badly mistaken. Pollution harms animals, plants, and humans. Many species have already gone extinct; forests are being cut down, rivers polluted, grasslands turning into deserts. According to international environmental organizations, over half of the planet's species are disappearing — this is real, not exaggerated. 17% of the world's population has no access to clean drinking water, and more people die each year from air-pollution-related diseases than from car accidents. Some pollution comes from industry and agriculture, some from daily life — car exhaust, garbage. The good news: more and more people are aware and taking action — adding eco-friendly facilities, sorting waste, cycling, using public transport. The Earth is our shared home, and its fate is in our hands.",
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
                "话题讨论：环保。1. 说说你每天从身边观察到的不环保的行为。2. 结合自己的经历，谈谈你对环保的认识。3. 请介绍几件生活中我们可以做到的环保实事。",
                "Обсуждение: охрана окружающей среды. 1. Какие неэкологичные действия вы наблюдаете? 2. Ваше понимание экологии. 3. Что реально можно сделать в быту?",
                "",
                "Discussion: environmental protection. 1. What non-eco behaviours do you observe? 2. Your understanding of eco issues. 3. What can we realistically do?",
                ""),
        },
        "workbook": workbook,
    }


def lesson33():
    vocab = [
        _vocab("缓解", "huǎnjiě", "v.", "ослаблять, облегчать", "to alleviate, to ease up"),
        _vocab("招儿", "zhāor", "n.", "приём, способ", "trick, move, method"),
        _vocab("繁荣", "fánróng", "adj.", "процветающий", "prosperous, thriving"),
        _vocab("体现", "tǐxiàn", "v.", "отражать, воплощать", "to manifest, to reflect"),
        _vocab("拥挤", "yōngjǐ", "adj.", "переполненный, тесный", "crowded, congested"),
        _vocab("家常", "jiācháng", "n.", "повседневная жизнь семьи", "daily life of a family"),
        _vocab("面积", "miànjī", "n.", "площадь", "area, space"),
        _vocab("宽", "kuān", "adj.", "широкий", "wide, broad"),
        _vocab("主观", "zhǔguān", "adj.", "субъективный", "subjective"),
        _vocab("扩大", "kuòdà", "v.", "расширять", "to enlarge, to expand"),
        _vocab("根治", "gēnzhì", "v.", "лечить радикально, искоренять", "to cure once and for all"),
        _vocab("不妨", "bùfáng", "adv.", "почему бы и не, не мешает", "might as well"),
        _vocab("展开", "zhǎnkāi", "v.", "разворачивать, развёртывать", "to launch, to carry out"),
        _vocab("归纳", "guīnà", "v.", "обобщать, подытоживать", "to infer, to sum up"),
        _vocab("虚心", "xūxīn", "adj.", "открытый, готовый учиться", "open-minded, modest"),
        _vocab("咨询", "zīxún", "v.", "консультироваться", "to consult"),
        _vocab("中旬", "zhōngxún", "n.", "середина месяца", "middle ten days of a month"),
        _vocab("照常", "zhàocháng", "adv.", "как обычно, как всегда", "as usual"),
        _vocab("健身", "jiànshēn", "v.", "поддерживать форму, тренироваться", "to keep fit, to work out"),
        _vocab("图", "tú", "v.", "ради, стремиться", "to covet, to be after"),
        _vocab("受伤", "shòushāng", "v.", "получить травму", "to be hurt, to be injured"),
        _vocab("保险", "bǎoxiǎn", "n.", "страховка", "insurance"),
        _vocab("赔偿", "péicháng", "v.", "компенсировать, возмещать", "to compensate"),
        _vocab("政府", "zhèngfǔ", "n.", "правительство", "government"),
        _vocab("批准", "pīzhǔn", "v.", "утверждать, ратифицировать", "to ratify, to approve"),
        _vocab("改革", "gǎigé", "v.", "реформировать", "to reform"),
        _vocab("取消", "qǔxiāo", "v.", "отменять", "to cancel, to call off"),
        _vocab("行人", "xíngrén", "n.", "пешеход", "pedestrian"),
        _vocab("广场", "guǎngchǎng", "n.", "площадь", "square, plaza"),
        _vocab("商务", "shāngwù", "n.", "бизнес, деловые дела", "business affairs"),
        _vocab("大厦", "dàshà", "n.", "большое здание", "large building, mansion"),
        _vocab("自愿", "zìyuàn", "v.", "добровольно", "to volunteer"),
        _vocab("难怪", "nánguài", "v./adv.", "неудивительно; вот почему", "to be understandable; no wonder"),
        _vocab("与其", "yǔqí", "conj.", "чем..., лучше", "rather than"),
        _vocab("汽油", "qìyóu", "n.", "бензин", "gasoline"),
        _vocab("明确", "míngquè", "adj.", "чёткий, ясный", "clear and definite"),
        _vocab("期待", "qīdài", "v.", "ожидать, надеяться", "to look forward to"),
        _vocab("解放", "jiěfàng", "v.", "освобождать", "to liberate, to free"),
    ]

    grammar = [
        {
            "word": "照常", "pos": "v./adv.",
            "explanation": {"ru": "«照常» — глагол: «идти как обычно»; наречие: «как всегда, без изменений».",
                            "en": "«照常» — verb: 'to go on as usual'; adverb: 'as usual, without change'."},
            "formula": {"ru": "照常 + 动词；一切照常", "en": "照常 + verb; 一切照常"},
            "examples": [
                {"zh": "九月中旬的一天早晨，詹森照常提前出门赶在早高峰之前去交通部。",
                 "ru": "Однажды утром в середине сентября Йенсен, как обычно, вышел пораньше, чтобы доехать до министерства до часа пик.",
                 "en": "One mid-September morning, Jensen left early as usual to beat the rush hour to the ministry."},
                {"zh": "虽然战争临近，但这里的日常生活，一切照常。",
                 "ru": "Хотя война приближалась, повседневная жизнь здесь шла как обычно.",
                 "en": "Though war was approaching, daily life here went on as usual."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "王医生，手术后__吗？",
                 "answer": "一般来说，手术后三个月就可以参加一般的运动了"},
            ],
        },
        {
            "word": "难怪", "pos": "v./adv.",
            "explanation": {"ru": "«难怪» — глагол: «нечего удивляться, понять и простить»; наречие: «вот почему, неудивительно».",
                            "en": "«难怪» — verb: 'to be understandable'; adverb: 'no wonder, that's why'."},
            "formula": {"ru": "难怪 + 小句；这也难怪", "en": "难怪 + clause; 这也难怪"},
            "examples": [
                {"zh": "这也难怪，与其堵在路上浪费时间和汽油，污染环境，倒不如改乘公交出行。",
                 "ru": "И неудивительно: чем стоять в пробке, терять время и бензин и загрязнять среду — лучше пересесть на общественный транспорт.",
                 "en": "No wonder — rather than waste time and petrol in traffic and pollute the environment, it's better to take public transport."},
                {"zh": "你的抽屉真乱，难怪总是找不到东西。",
                 "ru": "У тебя в ящике такой беспорядок — неудивительно, что ничего не находишь.",
                 "en": "Your drawer is so messy — no wonder you can never find anything."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "李岩和我是小学同学，我们认识快20年了。——__。",
                 "answer": "难怪你们这么熟。"},
            ],
        },
        {
            "word": "与其", "pos": "conj.",
            "explanation": {"ru": "«与其» — союз, вводит отвергаемый вариант; в паре с «不如», «宁可»: «чем..., лучше...».",
                            "en": "«与其» — conjunction, introduces the rejected option; pairs with «不如», «宁可»: 'rather than..., better to...'."},
            "formula": {"ru": "与其 + A，不如 + B", "en": "与其 + A，不如 + B"},
            "examples": [
                {"zh": "与其说是采访，不如说是向他学习。",
                 "ru": "Это не столько интервью, сколько учёба у него.",
                 "en": "It's less an interview than learning from him."},
                {"zh": "与其找个不认真的小时工，我宁可自己打扫。",
                 "ru": "Чем брать нерадивого уборщика, я лучше сам уберу.",
                 "en": "Rather than hire a careless cleaner, I'd rather do it myself."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "那些赶时髦的消费者，__。",
                 "answer": "与其说是买东西，不如说是买牌子"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "表现", "word_b": "体现",
            "common": {"ru": "Оба глагола означают «проявлять, показывать».",
                       "en": "Both verbs mean 'to show, to manifest'."},
            "differences": [
                {"ru": "«表现» — о стиле, эмоциях, отношении конкретного человека; может быть существительным «поведение».",
                 "en": "«表现» — about a person's style, emotion, attitude; can be a noun meaning 'behaviour'."},
                {"ru": "«体现» — о том, как явление, идея или сущность отражаются в чём-то конкретном.",
                 "en": "«体现» — about how a phenomenon, idea, or essence is reflected in something concrete."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "交通", "ru": "Транспорт", "en": "Transport"},
        "words": [
            {"hanzi": "卡车", "pinyin": "kǎchē", "meaning": {"zh": "", "ru": "грузовик", "en": "truck"}},
            {"hanzi": "列车", "pinyin": "lièchē", "meaning": {"zh": "", "ru": "поезд, состав", "en": "train"}},
            {"hanzi": "摩托车", "pinyin": "mótuōchē", "meaning": {"zh": "", "ru": "мотоцикл", "en": "motorcycle"}},
            {"hanzi": "行人", "pinyin": "xíngrén", "meaning": {"zh": "", "ru": "пешеход", "en": "pedestrian"}},
            {"hanzi": "车厢", "pinyin": "chēxiāng", "meaning": {"zh": "", "ru": "вагон, салон", "en": "carriage"}},
            {"hanzi": "车库", "pinyin": "chēkù", "meaning": {"zh": "", "ru": "гараж", "en": "garage"}},
            {"hanzi": "拐弯", "pinyin": "guǎiwān", "meaning": {"zh": "", "ru": "поворачивать", "en": "to turn"}},
            {"hanzi": "绕", "pinyin": "rào", "meaning": {"zh": "", "ru": "обходить, объезжать", "en": "to detour"}},
            {"hanzi": "长途", "pinyin": "chángtú", "meaning": {"zh": "", "ru": "дальний рейс", "en": "long-distance"}},
            {"hanzi": "运输", "pinyin": "yùnshū", "meaning": {"zh": "", "ru": "перевозить", "en": "to transport"}},
            {"hanzi": "汽油", "pinyin": "qìyóu", "meaning": {"zh": "", "ru": "бензин", "en": "gasoline"}},
            {"hanzi": "罚款", "pinyin": "fákuǎn", "meaning": {"zh": "", "ru": "штраф", "en": "fine"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_33_1.mp3",
             "prompt": {"zh": "詹森怎么解决堵车问题？", "ru": "Как Йенсен решал проблему пробок?", "en": "How did Jensen solve congestion?"},
             "options": ["修更多路", "让城市更堵", "禁止开车", "增加地铁"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "詹森方法的核心理念是什么？", "ru": "Какова главная идея метода Йенсена?", "en": "What is the core idea of Jensen's method?"},
             "options": ["修路越多越好", "开车更方便", "以堵治堵", "增加停车场"], "answer": 2},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["把", "大意", "请", "这篇文章的", "归纳一下"],
             "answer": "请把这篇文章的大意归纳一下。"},
            {"type": "make_sentence", "words": ["照常", "他还是", "第一个", "来到单位", "第二天早晨"],
             "answer": "第二天早晨他还是照常第一个来到单位。"},
            {"type": "short_essay", "words": ["交通", "行人", "拥挤", "缓解", "政府"], "min_length": 80},
        ],
    }

    return {
        "title": _t("以堵治堵——缓解交通有妙招", "Пробка против пробки", "", "Treating congestion with congestion", ""),
        "audio_files": {
            "textbook_1": "textbook_33_1.mp3",
            "vocab": "vocab_33.mp3",
            "workbook_33_1": "workbook_33_1.mp3",
        },
        "warmup": {
            "question": _t(
                "请你说说这幅图片反映了什么问题，它对你的生活有何影响。你知道哪些有关交通的词语？",
                "Что показывает эта картинка? Как это влияет на вашу жизнь? Какие слова о транспорте вы знаете?",
                "",
                "What does this picture show? How does it affect your life? What transport-related words do you know?",
                ""),
            "answers": ["堵车"],
        },
        "text_zh": (
            "城市汽车的数量迅速增长，最初还被视为是社会发展、经济繁荣的体现。但很快人们就发现了问题。随着车流量的增加，道路变得格外拥挤，堵车在大城市中已经成了家常便饭。\n"
            "解决交通拥堵的问题就要减少单位面积道路内的汽车数量，新建或加宽道路被公认为最基本的方法。但事实证明这只是我们美好的主观愿望，道路扩建的速度远远跟不上车流量增加的速度，面积的增加并未使道路空出空间来，甚至还会无形之中鼓励更多的司机开车上路，使得市中心的道路更加拥挤。\n"
            "那么，如何根治交通拥堵呢？这里我们不妨听听佩·詹森的故事。\n"
            "詹森一到欧洲环境保护署交通部工作，就接到了研究如何解决城市拥堵问题的任务。于是，他开始展开调查，研究收集上来的数据，归纳问题特点，并虚心咨询了有关专家。\n"
            "九月中旬的一天早晨，詹森照常提前出门赶在早高峰之前去交通部。他看到一个健身的人慢跑通过一个有过街天桥的路口时，为图省事没上天桥，而是横穿马路。结果，他被一辆车撞倒在地，虽然最后他只是受了点轻伤，而且有保险可以赔偿，但司机还是被吓得不轻。\n"
            "不过这件事倒是给了詹森启发：开车出行是为了省时省力，但如果情况相反呢？他决定要改变市民出行的观念，反其道而行之——让城市先堵起来，给司机制造麻烦，以堵治堵。\n"
            "经过多次努力，政府批准了他提出的改革措施，比如，增设红绿灯，让车辆不得不走走停停；在主要十字路口取消地下通道，让行人从地下重返地面；在购物广场、商务大厦的附近不建停车场等。同时，大力发展公共交通。\n"
            "半年过去了，虽然市民们有些抱怨，但效果非常明显，自愿放弃开私家车出门的人越来越多。这也难怪，与其堵在路上浪费时间和汽油，污染环境，倒不如改乘公交出行。这样一来，道路拥堵大为缓解。\n"
            "城市本是为人而建，如今却被汽车占有，詹森的目标很明确，就是期待能够解放城市，使之更适合人类生活。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Рост числа машин сначала считался признаком prosperity. Но вскоре выяснилось: чем больше машин, тем плотнее пробки. Расширение дорог не помогает — оно только поощряет больше людей садиться за руль. Как же радикально решить проблему? Йенсен из Европейского экологического агентства предложил парадоксальное решение: «пробка против пробки» — не расширять дороги, а наоборот усложнить вождение: добавить светофоры, убрать подземные переходы, не строить парковки у торговых центров, развивать общественный транспорт. Через полгода поток частных машин резко сократился. Цель Йенсена — освободить город от машин и сделать его удобным для людей.",
            "tk": "",
            "en": "The growth in cars was first seen as a sign of prosperity. But soon problems appeared: more cars meant more congestion. Widening roads doesn't help — it encourages more driving. How to cure it? Jensen from the European Environment Agency proposed a paradoxical solution: 'congestion against congestion' — don't widen roads, make driving less convenient: more traffic lights, remove underpasses, don't build parking near shopping malls, develop public transport. Six months later, private-car use dropped sharply. Jensen's goal: free the city from cars and make it more liveable for people.",
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
                "话题讨论：出行方式。1. 你们国家道路交通情况怎么样？2. 你平时出行一般采用何种方式？3. 你认为造成交通拥堵现象的主要原因是什么？应该如何解决？",
                "Обсуждение: способы передвижения. 1. Как обстоят дела с транспортом в вашей стране? 2. Как вы обычно передвигаетесь? 3. В чём причина пробок и как их решать?",
                "",
                "Discussion: transport. 1. What's transport like in your country? 2. How do you usually travel? 3. Causes of congestion and solutions.",
                ""),
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(11, 31, lesson31())
    save(11, 32, lesson32())
    save(11, 33, lesson33())
    print("Done.")