# -*- coding: utf-8 -*-
"""Уроки 34-36 (Unit 12 — 亲近自然)."""
from build_hsk5_lower import _vocab, _t, save


def lesson34():
    vocab = [
        _vocab("接触", "jiēchù", "v.", "контактировать, соприкасаться", "to contact, to get in touch with"),
        _vocab("特征", "tèzhēng", "n.", "характерная черта", "feature, characteristic"),
        _vocab("翅膀", "chìbǎng", "n.", "крыло", "wing"),
        _vocab("昆虫", "kūnchóng", "n.", "насекомое", "insect"),
        _vocab("天空", "tiānkōng", "n.", "небо", "sky"),
        _vocab("区分", "qūfēn", "v.", "различать, отличать", "to distinguish, to differentiate"),
        _vocab("唯一", "wéiyī", "adj.", "единственный", "only, sole"),
        _vocab("斑", "bān", "n.", "пятно, полоса", "spot, speckle, stripe"),
        _vocab("充当", "chōngdāng", "v.", "играть роль, служить", "to serve as, to play the part of"),
        _vocab("总之", "zǒngzhī", "conj.", "короче говоря", "in short, in brief"),
        _vocab("角色", "juésè", "n.", "роль, персонаж", "role, part"),
        _vocab("爱惜", "àixī", "v.", "беречь, дорожить", "to cherish, to treasure"),
        _vocab("保养", "bǎoyǎng", "v.", "ухаживать, поддерживать", "to take good care of"),
        _vocab("反复", "fǎnfù", "adv.", "неоднократно, снова и снова", "repeatedly, over and over again"),
        _vocab("啄", "zhuó", "v.", "клевать", "to peck"),
        _vocab("随身", "suíshēn", "adj.", "при себе, с собой", "to carry with one"),
        _vocab("梳子", "shūzi", "n.", "расчёска", "comb"),
        _vocab("光滑", "guānghuá", "adj.", "гладкий", "smooth, glossy"),
        _vocab("抓", "zhuā", "v.", "хватать, ловить", "to grab, to seize"),
        _vocab("寄生", "jìshēng", "v.", "паразитировать", "to live on another animal"),
        _vocab("肥皂", "féizào", "n.", "мыло", "soap"),
        _vocab("种类", "zhǒnglèi", "n.", "вид, разновидность", "kind, category"),
        _vocab("概括", "gàikuò", "adj./v.", "обобщённый; обобщать", "brief; to summarize"),
        _vocab("岛屿", "dǎoyǔ", "n.", "остров", "island"),
        _vocab("知更鸟", "zhīgēngniǎo", "n.", "малиновка", "robin, redbreast"),
        _vocab("坑", "kēng", "n.", "яма, углубление", "pit, hollow"),
        _vocab("池塘", "chítáng", "n.", "пруд", "pond"),
        _vocab("老鹰", "lǎoyīng", "n.", "орёл, ястреб", "eagle, hawk"),
        _vocab("痛快", "tòngkuài", "adj.", "с удовольствием, от души", "to one's heart's content"),
        _vocab("迎接", "yíngjiē", "v.", "встречать, приветствовать", "to receive, to greet"),
        _vocab("洗礼", "xǐlǐ", "n.", "крещение, омовение", "baptism, washing ceremony"),
        _vocab("沙子", "shāzi", "n.", "песок", "sand"),
        _vocab("干燥", "gānzào", "adj.", "сухой", "dry, arid"),
        _vocab("秘密", "mìmì", "adj./n.", "секретный; секрет", "secret"),
    ]

    grammar = [
        {
            "word": "总之", "pos": "conj.",
            "explanation": {"ru": "«总之» — союз, подводит итог сказанному выше: «в общем, короче говоря».",
                            "en": "«总之» — conjunction, sums up what was said: 'in short, in a word'."},
            "formula": {"ru": "……, 总之 + 总结性小句", "en": "..., 总之 + summary clause"},
            "examples": [
                {"zh": "暑假我可能去上海、南京，还有杭州，总之，想去南方几个城市转转。",
                 "ru": "На летних каникулах я, возможно, поеду в Шанхай, Нанкин и Ханчжоу — короче, хочу проехаться по нескольким южным городам.",
                 "en": "In summer vacation I might go to Shanghai, Nanjing, and Hangzhou — in short, I want to tour several southern cities."},
                {"zh": "总之，在鸟儿的生活中，羽毛充当着十分重要的角色。",
                 "ru": "Словом, в жизни птиц перья играют очень важную роль.",
                 "en": "In short, feathers play a very important role in birds' lives."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "不管你去不去，__。", "answer": "总之我都要去。"},
            ],
        },
        {
            "word": "动词+过", "pos": "structure",
            "explanation": {"ru": "Конструкция «动词+过» означает «через действие изменить направление» или «переместить положение».",
                            "en": "The pattern 'verb + 过' means 'change direction by action' or 'shift position'."},
            "formula": {"ru": "动词 + 过", "en": "verb + 过"},
            "examples": [
                {"zh": "他转过身，一句话也不说。",
                 "ru": "Он повернулся и не сказал ни слова.",
                 "en": "He turned around without saying a word."},
                {"zh": "它们只要有时间，就会情不自禁地背过头去，反复地啄着羽毛。",
                 "ru": "Как только у них есть время, они невольно поворачивают голову назад и снова и снова перебирают перья клювом.",
                 "en": "Whenever they have time, they can't help turning their heads back and pecking their feathers repeatedly."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "你回__头就可以看见我了。", "answer": "过"},
            ],
        },
        {
            "word": "动词+开", "pos": "structure",
            "explanation": {"ru": "Конструкция «动词+开» означает «развернуть, распахнуть, развернуться».",
                            "en": "The pattern 'verb + 开' means 'to spread, to unfold, to open wide'."},
            "formula": {"ru": "动词 + 开", "en": "verb + 开"},
            "examples": [
                {"zh": "猴子突然站了起来，张开手臂，抱住了管理员。",
                 "ru": "Обезьяна вдруг встала, раскрыла объятия и обняла смотрителя.",
                 "en": "The monkey suddenly stood up, spread its arms, and hugged the keeper."},
                {"zh": "而老鹰的洗澡方式更是直接，它们会在雨中张开双翅痛快地迎接洗礼！",
                 "ru": "А орлы моются ещё проще — они распахивают крылья под дождём, принимая такое «крещение»!",
                 "en": "Eagles bathe even more directly — they spread their wings in the rain, happily welcoming the shower!"},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "回家时，妈妈张__双臂迎接我。", "answer": "开"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "反复", "word_b": "重复",
            "common": {"ru": "Оба означают «больше одного раза».",
                       "en": "Both mean 'more than once'."},
            "differences": [
                {"ru": "«反复» — наречие: «снова и снова»; также глагол о возврате болезни; существительное о нестабильности.",
                 "en": "«反复» — adverb: 'over and over'; also verb of illness relapsing; noun of instability."},
                {"ru": "«重复» — глагол: «повторять одно и то же».",
                 "en": "«重复» — verb: 'to repeat the same thing'."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "地理环境", "ru": "Географическая среда", "en": "Geographical environment"},
        "words": [
            {"hanzi": "天空", "pinyin": "tiānkōng", "meaning": {"zh": "", "ru": "небо", "en": "sky"}},
            {"hanzi": "陆地", "pinyin": "lùdì", "meaning": {"zh": "", "ru": "земля, суша", "en": "land"}},
            {"hanzi": "土地", "pinyin": "tǔdì", "meaning": {"zh": "", "ru": "земля, почва", "en": "land, soil"}},
            {"hanzi": "池塘", "pinyin": "chítáng", "meaning": {"zh": "", "ru": "пруд", "en": "pond"}},
            {"hanzi": "沙漠", "pinyin": "shāmò", "meaning": {"zh": "", "ru": "пустыня", "en": "desert"}},
            {"hanzi": "沙滩", "pinyin": "shātān", "meaning": {"zh": "", "ru": "пляж", "en": "beach"}},
            {"hanzi": "岛屿", "pinyin": "dǎoyǔ", "meaning": {"zh": "", "ru": "остров", "en": "island"}},
            {"hanzi": "岸", "pinyin": "àn", "meaning": {"zh": "", "ru": "берег", "en": "bank"}},
            {"hanzi": "洞", "pinyin": "dòng", "meaning": {"zh": "", "ru": "пещера, дыра", "en": "hole, cave"}},
            {"hanzi": "木头", "pinyin": "mùtou", "meaning": {"zh": "", "ru": "дерево, древесина", "en": "wood"}},
            {"hanzi": "石头", "pinyin": "shítou", "meaning": {"zh": "", "ru": "камень", "en": "stone"}},
            {"hanzi": "灰尘", "pinyin": "huīchén", "meaning": {"zh": "", "ru": "пыль", "en": "dust"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_34_1.mp3",
             "prompt": {"zh": "鸟儿最重要的特征是什么？", "ru": "Какая самая важная черта птиц?", "en": "What is the most important feature of birds?"},
             "options": ["会飞", "有翅膀", "有羽毛", "吃昆虫"], "answer": 2},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "鸟儿怎么保养羽毛？", "ru": "Как птицы ухаживают за перьями?", "en": "How do birds care for their feathers?"},
             "options": ["用肥皂", "梳理和洗澡", "用沙子洗", "不保养"], "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["没接触过", "的", "业务", "我从来", "这方面"],
             "answer": "我从来没接触过这方面的业务。"},
            {"type": "make_sentence", "words": ["戏剧", "今天学的", "的种类", "概括一下", "请你"],
             "answer": "请你概括一下今天学的戏剧的种类。"},
            {"type": "short_essay", "words": ["秘密", "唯一", "痛快", "爱惜", "总之"], "min_length": 80},
        ],
    }

    return {
        "title": _t("鸟儿的护肤术", "Уход за перьями у птиц", "", "How birds take care of their feathers", ""),
        "audio_files": {
            "textbook_1": "textbook_34_1.mp3",
            "vocab": "vocab_34.mp3",
            "workbook_34_1": "workbook_34_1.mp3",
        },
        "warmup": {
            "question": _t(
                "说起鸟儿，你会想到它们的哪些特征？请给老师和同学们讲一讲。",
                "Когда вы думаете о птицах, какие их черты приходят на ум? Расскажите классу.",
                "",
                "When you think of birds, what features come to mind? Tell the class.",
                ""),
            "answers": ["池塘"],
        },
        "text_zh": (
            "大家都接触过鸟儿吧？那你知道鸟儿最重要的特征是什么吗？是有翅膀会飞？还是吃昆虫？\n"
            "作为一只鸟儿，不管是天空中飞的，陆地上走的，或者能入水的，都必须拥有羽毛。没错儿，区分鸟儿和其他动物的唯一特征就是羽毛，而不是会不会飞！羽毛的作用很多，既可以保暖，又可以保护皮肤；羽毛上的颜色和斑还能充当保护色；当然，更关键的是，羽毛有助于飞行；甚至还有一些鸟儿的部分羽毛有“触觉”。总之，在鸟儿的生活中，羽毛充当着十分重要的角色。所以，鸟儿非常爱惜羽毛，每天都会花很长时间来保养自己的“羽衣”。\n"
            "整理羽毛是保养的基本功，它们只要有时间，就会情不自禁地背过头去，反复地啄着羽毛，就像随身带了一把梳子梳头发一样，顺便上上油，让羽毛更光滑。另外，鸟儿在理毛的时候，还会抓出一点儿寄生虫。\n"
            "毫无疑问，洗澡也是保养的一大基本项目。不过，鸟儿洗澡用不着肥皂，而且不同种类的鸟儿选择的“澡堂”也不一样，概括来说，就是以方便为原则。比如，海鸟在岛屿上生活，就会选择海水；知更鸟喜欢路旁的浅水坑；寒带的鸟呢，因为江河池塘不好找，只好以雪代水；而老鹰的洗澡方式更是直接，它们会在雨中张开双翅痛快地迎接洗礼！沙浴也是一些鸟儿喜欢的保养方式。所谓沙浴，就是用沙子洗澡，它们之所以放弃了用水洗澡，在很大程度上和它们的生活环境有关，它们大多生活在沙漠等干燥的环境，爱在地面上活动。\n"
            "另外，睡眠是鸟儿们最佳的保养方式，虽然我们很少看到睡眠中的鸟儿，那是因为它们通常会寻找一处秘密的地方休息。大多数鸟儿1天大约睡8小时，有些鸟儿差不多要睡1天，而另一些鸟儿几乎一点儿也就不用睡。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Все мы видели птиц, но знаете ли вы, какая их черта самая главная? Не умение летать, а перья! Только перья отличают птиц от других животных. Они греют, защищают кожу, служат маскировкой, помогают летать, а у некоторых видов даже осязают. Неудивительно, что птицы так тщательно ухаживают за ними: чистят клювом, «смазывают» маслом, вылавливают паразитов. Купаются они тоже по-разному: морские — в море, малиновки — в лужах, полярные — в снегу, а орлы — прямо под дождём, распахнув крылья. Некоторые предпочитают «песчаные ванны» — особенно живущие в пустыне. Ну и, конечно, сон — лучший уход: большинство птиц спит около 8 часов в сутки, а некоторые — почти круглосуточно.",
            "tk": "",
            "en": "We've all seen birds — but do you know their most important feature? Not flight, but feathers! Feathers are the only feature that distinguishes birds from other animals. They provide warmth, protect skin, serve as camouflage, help with flight, and some even have a tactile function. No wonder birds care for them so carefully: preening with their beaks, spreading oil, removing parasites. Their bathing methods vary: seabirds in the sea, robins in shallow puddles, polar birds in snow, and eagles directly in the rain with wings spread wide. Some prefer 'sand baths' — especially those living in deserts. And, of course, sleep is the best care: most birds sleep about 8 hours a day, some nearly the whole day.",
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
                "话题讨论：养宠物。1. 你养过宠物吗？你对养宠物有什么看法？2. 如果你养过或正在养宠物，请说说你和宠物的故事。3. 如果你对养宠物没有兴趣，请说明原因。",
                "Обсуждение: домашние питомцы. 1. У вас были питомцы? Как вы к этому относитесь? 2. Расскажите историю о питомце. 3. Если не интересуетесь — почему?",
                "",
                "Discussion: pets. 1. Have you had pets? What do you think? 2. Share a story. 3. If not interested — why?",
                ""),
        },
        "workbook": workbook,
    }


def lesson35():
    vocab = [
        _vocab("炎热", "yánrè", "adj.", "жаркий, знойный", "scorching, burning hot"),
        _vocab("歇", "xiē", "v.", "отдыхать, передохнуть", "to rest, to take a rest"),
        _vocab("开水", "kāishuǐ", "n.", "кипяток", "boiled water"),
        _vocab("冰激凌", "bīngjīlíng", "n.", "мороженое", "ice cream"),
        _vocab("肌肉", "jīròu", "n.", "мышцы", "muscle"),
        _vocab("恢复", "huīfù", "v.", "восстанавливать, восстанавливаться", "to recover, to regain"),
        _vocab("湿润", "shīrùn", "adj.", "влажный", "moist, humid"),
        _vocab("荫凉", "yīnliáng", "adj.", "тенистый и прохладный", "shady and cool"),
        _vocab("指挥", "zhǐhuī", "v.", "командовать, управлять", "to command, to direct"),
        _vocab("赶快", "gǎnkuài", "adv.", "скорее, поскорее", "at once, hurriedly"),
        _vocab("汗腺", "hànxiàn", "n.", "потовые железы", "sweat gland"),
        _vocab("毛孔", "máokǒng", "n.", "поры", "pore"),
        _vocab("冒", "mào", "v.", "просачиваться, выделяться", "to emit, to give off"),
        _vocab("片", "piàn", "n.", "ломтик, пластинка", "flat and thin piece"),
        _vocab("常识", "chángshí", "n.", "здравый смысл, общие знания", "common knowledge"),
        _vocab("根", "gēn", "n.", "корень", "root"),
        _vocab("吸收", "xīshōu", "v.", "впитывать, поглощать", "to absorb, to take in"),
        _vocab("控制", "kòngzhì", "v.", "контролировать, управлять", "to control"),
        _vocab("成分", "chéngfèn", "n.", "состав, компонент", "element, component"),
        _vocab("梢", "shāo", "n.", "верхушка, кончик", "tip, thin end of a twig"),
        _vocab("管子", "guǎnzi", "n.", "трубка, труба", "tube, pipe"),
        _vocab("玻璃", "bāli", "n.", "стекло", "glass"),
        _vocab("测验", "cèyàn", "v.", "проверять, тестировать", "to test"),
        _vocab("根本", "gēnběn", "adv.", "вовсе не, совершенно не", "at all, simply"),
        _vocab("枝干", "zhīgàn", "n.", "ветви и ствол", "branch, limb"),
        _vocab("释放", "shìfàng", "v.", "выделять, освобождать", "to release, to emit"),
        _vocab("自动", "zìdòng", "adv.", "автоматически, самопроизвольно", "voluntarily, spontaneously"),
        _vocab("补充", "bǔchōng", "v.", "восполнять, дополнять", "to supplement, to replenish"),
        _vocab("抽", "chōu", "v.", "вытягивать, откачивать", "to draw, to obtain by drawing"),
        _vocab("蒸腾", "zhēngténg", "v.", "испаряться", "to rise, to vaporize"),
        _vocab("特殊", "tèshū", "adj.", "особенный, специальный", "special, particular"),
        _vocab("内部", "nèibù", "n.", "внутренняя часть", "inside, interior"),
        _vocab("系统", "xìtǒng", "n.", "система", "system"),
        _vocab("状况", "zhuàngkuàng", "n.", "состояние, положение", "condition, situation"),
        _vocab("秩序", "zhìxù", "n.", "порядок", "order, orderly state"),
    ]

    grammar = [
        {
            "word": "赶快", "pos": "adv.",
            "explanation": {"ru": "«赶快» — наречие: «скорее, поторапливайся», сделать что-то в сжатые сроки.",
                            "en": "«赶快» — adverb: 'hurry up, at once' — do something within a tight timeframe."},
            "formula": {"ru": "赶快 + 动词", "en": "赶快 + verb"},
            "examples": [
                {"zh": "一旦温度上升，大脑就会指挥我们的身体赶快出汗。",
                 "ru": "Как только температура поднимается, мозг командует телу быстрее потеть.",
                 "en": "Once the temperature rises, the brain instructs the body to sweat quickly."},
                {"zh": "这份材料下午开会要用，你赶快把它复印一下。",
                 "ru": "Эти материалы нужны на совещании после обеда, срочно сделай копию.",
                 "en": "These materials are needed for the afternoon meeting — make copies right away."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "__，要不该赶上堵车了。", "answer": "赶快走吧"},
            ],
        },
        {
            "word": "片", "pos": "n./m.",
            "explanation": {"ru": "«片» — существительное: «плоский тонкий предмет»; счётное слово для плоских предметов, звуков, пейзажей.",
                            "en": "«片» — noun: 'a flat thin piece'; measure word for flat objects, sounds, scenery."},
            "formula": {"ru": "一片 + 名词", "en": "一片 + noun"},
            "examples": [
                {"zh": "大树出的“汗”，通常是从叶片的气孔里冒出来的。",
                 "ru": "«Пот» большого дерева обычно выступает из устьиц листовых пластинок.",
                 "en": "The tree's 'sweat' usually comes out through the leaf blades' stomata."},
                {"zh": "窗外有一棵大树，秋风中，叶子一片片地掉落下来。",
                 "ru": "За окном большое дерево — осенний ветер срывает один за другим листья.",
                 "en": "Outside the window a big tree — in the autumn wind, leaves fall one by one."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "今天早上我吃了两__面包。", "answer": "片"},
            ],
        },
        {
            "word": "根本", "pos": "n./adj./adv.",
            "explanation": {"ru": "«根本» — сущ.: «основа, суть»; прил.: «основной, главный»; нареч.: «вовсе не, совершенно не» (в отрицаниях).",
                            "en": "«根本» — noun: 'root, basis'; adj.: 'fundamental'; adv.: 'at all, simply' (in negatives)."},
            "formula": {"ru": "根本 + 不/没 + 动词", "en": "根本 + 不/没 + verb"},
            "examples": [
                {"zh": "经过测验计算发现，以大树输送管道的尺寸产生的毛细作用，根本无法把水分送到几十米高的地方。",
                 "ru": "Расчёты показали, что капиллярный эффект в трубках дерева вовсе не способен поднять воду на десятки метров.",
                 "en": "Calculations revealed that capillary action in a tree's pipes simply cannot lift water dozens of meters high."},
                {"zh": "他根本就是在故意找我们的麻烦。",
                 "ru": "Он просто нарочно ищет, к чему бы придраться.",
                 "en": "He is simply deliberately making trouble for us."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "你觉得他说的话有道理吗？——__。",
                 "answer": "根本没有道理"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "特殊", "word_b": "特别",
            "common": {"ru": "Как прилагательные оба означают «не такой, как все».",
                       "en": "As adjectives both mean 'different from the ordinary'."},
            "differences": [
                {"ru": "«特殊» — чаще в письменной речи, обозначает необычное качество.",
                 "en": "«特殊» — mostly literary, denotes an unusual quality."},
                {"ru": "«特别» — и в устной, и в письменной речи; может быть наречием: «особенно».",
                 "en": "«特别» — used in both speech and writing; can be an adverb meaning 'especially'."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "动物、植物", "ru": "Животные, растения", "en": "Animals and plants"},
        "words": [
            {"hanzi": "老鼠", "pinyin": "lǎoshǔ", "meaning": {"zh": "", "ru": "мышь, крыса", "en": "mouse, rat"}},
            {"hanzi": "蜜蜂", "pinyin": "mìfēng", "meaning": {"zh": "", "ru": "пчела", "en": "bee"}},
            {"hanzi": "蛇", "pinyin": "shé", "meaning": {"zh": "", "ru": "змея", "en": "snake"}},
            {"hanzi": "狮子", "pinyin": "shīzi", "meaning": {"zh": "", "ru": "лев", "en": "lion"}},
            {"hanzi": "兔子", "pinyin": "tùzi", "meaning": {"zh": "", "ru": "заяц, кролик", "en": "rabbit"}},
            {"hanzi": "大象", "pinyin": "dàxiàng", "meaning": {"zh": "", "ru": "слон", "en": "elephant"}},
            {"hanzi": "猴子", "pinyin": "hóuzi", "meaning": {"zh": "", "ru": "обезьяна", "en": "monkey"}},
            {"hanzi": "猪", "pinyin": "zhū", "meaning": {"zh": "", "ru": "свинья", "en": "pig"}},
            {"hanzi": "蝴蝶", "pinyin": "húdié", "meaning": {"zh": "", "ru": "бабочка", "en": "butterfly"}},
            {"hanzi": "昆虫", "pinyin": "kūnchóng", "meaning": {"zh": "", "ru": "насекомое", "en": "insect"}},
            {"hanzi": "小麦", "pinyin": "xiǎomài", "meaning": {"zh": "", "ru": "пшеница", "en": "wheat"}},
            {"hanzi": "竹子", "pinyin": "zhúzi", "meaning": {"zh": "", "ru": "бамбук", "en": "bamboo"}},
            {"hanzi": "根", "pinyin": "gēn", "meaning": {"zh": "", "ru": "корень", "en": "root"}},
            {"hanzi": "果实", "pinyin": "guǒshí", "meaning": {"zh": "", "ru": "плод", "en": "fruit"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_35_1.mp3",
             "prompt": {"zh": "植物为什么要出汗？", "ru": "Почему растения «потеют»?", "en": "Why do plants 'sweat'?"},
             "options": ["为了降温", "为了运输养分", "为了开花", "为了排毒"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "大树是怎么把水运到高处的？", "ru": "Как дерево поднимает воду наверх?", "en": "How does a tree lift water up?"},
             "options": ["毛细作用", "水泵", "蒸腾拉力", "风"], "answer": 2},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["缓解", "吃什么", "食物", "有可能", "疲劳"],
             "answer": "吃什么食物有可能缓解疲劳？"},
            {"type": "make_sentence", "words": ["交来的", "这是他", "补充材料", "上次", "面试后"],
             "answer": "这是他上次面试后交来的补充材料。"},
            {"type": "short_essay", "words": ["测验", "特殊", "秩序", "歇", "恢复"], "min_length": 80},
        ],
    }

    return {
        "title": _t("植物会出汗", "Растения тоже потеют", "", "Plants also sweat", ""),
        "audio_files": {
            "textbook_1": "textbook_35_1.mp3",
            "vocab": "vocab_35.mp3",
            "workbook_35_1": "workbook_35_1.mp3",
        },
        "warmup": {
            "question": _t(
                "请问问你的同学或朋友，他们在炎热的夏天运动之后，常常用什么办法给自己降温。",
                "Спросите друга: чем он обычно охлаждается после спорта в жаркий летний день?",
                "",
                "Ask a friend: what do they usually do to cool down after sports on a hot summer day?",
                ""),
            "answers": ["秩序"],
        },
        "text_zh": (
            "炎热的夏天，踢完一场球赛，每个队员都已经是汗如雨下。如果这个时候，能到大树下歇一歇，喝口凉开水，吃个冰激凌，放松放松肌肉，缓解一下疲劳，那一定是件美事，可以很快恢复活力。不过，你知道吗，我们之所以能在大树下享受这种湿润荫凉，也是因为大树在“出汗”呢！\n"
            "人体要保持相对稳定的温度，一旦温度上升，大脑就会指挥我们的身体赶快出汗，这时所有汗腺开始工作，汗水就从毛孔里冒了出来。大树出的“汗”，通常是从叶片的气孔里冒出来的，不过，这种“出汗”可不是为了降低温度，而是为了运输养分。\n"
            "我们都知道这样的常识——植物的根会吸收养分和水分，但是你有没有想过，植物是怎么控制这些成分，把它们运输到十几米甚至上百米的树梢的呢？\n"
            "最初人们认为大树是通过毛细作用来提水的。所谓“毛细作用”，简单来说，就是水会顺着很细很细的管子向上“爬”，我们在家可以用一个比较细的玻璃管体验一下。玻璃管越细，水爬升的高度就越高。可是，经过测验计算发现，以大树输送管道的尺寸产生的毛细作用，根本无法把水分送到几十米高的地方。\n"
            "实际上，大树利用的是枝干顶端的那些叶片。叶子通过不停地向空气中释放水汽，迫使树干中的水分自动前来补充，这样节节传递，就像是把树根吸收的水分给抽了上来。因为跟蒸腾作用有关，这种特殊的提升力就被称为“蒸腾拉力”。不过，这个大树内部的供水系统具体的运转状况是怎么样的，它们遵守的是一种什么样的秩序，为什么会产生如此巨大的拉力，到目前还是个谜。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Жарким летом после футбола каждый игрок обливается потом. Как приятно отдохнуть под деревом, выпить прохладной воды, съесть мороженое, расслабить мышцы и снять усталость! Но знаете ли вы, что этой прохладой и влагой под деревом мы обязаны тому, что дерево тоже «потеет»? Человек поддерживает стабильную температуру: чуть что — мозг командует потеть, железы работают, пот выступает из пор. «Пот» дерева выходит из устьиц листьев — но не для охлаждения, а для транспорта питательных веществ. Сначала думали, что дерево поднимает воду капиллярным эффектом, но расчёты показали: при диаметре сосудов дерева капиллярный эффект не поднимет воду на десятки метров. Оказывается, дерево использует листья: они выпускают пар в воздух, заставляя воду в стволе автоматически подтягиваться — как насос. Это называется «транспирационной тягой». Впрочем, как именно работает эта система и почему возникает такая мощная тяга — до сих пор загадка.",
            "tk": "",
            "en": "On a hot summer day, after a football match, everyone is drenched in sweat. How wonderful it would be to rest under a big tree, drink cool water, eat ice cream, relax the muscles and relieve fatigue! But did you know that the coolness and moisture under the tree are thanks to the tree also 'sweating'? The human body maintains a stable temperature: once it rises, the brain tells the body to sweat, glands work, sweat comes out of the pores. A tree's 'sweat' comes out through the stomata of its leaves — but not for cooling: it's for transporting nutrients. People first thought trees lifted water via capillary action, but calculations showed that at the tree's pipe diameters, capillary action can't lift water dozens of meters. In fact, the tree uses the leaves at the tips of its branches: they keep releasing water vapor into the air, forcing water in the trunk to automatically replenish, stage by stage — like pumping water up. Because it's related to transpiration, this special lifting force is called 'transpiration pull'. How exactly the tree's internal water-supply system works, what order it follows, and why such a huge pull arises — remains a mystery.",
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
                "话题讨论：植物的功能。1. 你喜欢什么样的植物？2. 在你的国家最常见或最有名的植物是什么？3. 在你的生活中，植物起了什么作用？",
                "Обсуждение: роль растений. 1. Какие растения вам нравятся? 2. Самые известные растения вашей страны? 3. Какую роль растения играют в вашей жизни?",
                "",
                "Discussion: plants. 1. What plants do you like? 2. Most famous plants in your country? 3. Role of plants in your life?",
                ""),
        },
        "workbook": workbook,
    }


def lesson36():
    vocab = [
        _vocab("养", "yǎng", "v.", "выращивать, разводить", "to raise, to keep, to grow"),
        _vocab("除非", "chúfēi", "conj.", "если только не, разве что", "only if, unless"),
        _vocab("奋斗", "fèndòu", "v.", "бороться, добиваться", "to fight, to strive"),
        _vocab("乐趣", "lèqù", "n.", "удовольствие, радость", "joy, pleasure"),
        _vocab("在乎", "zàihu", "v.", "заботиться, придавать значение", "to care, to mind"),
        _vocab("朵", "duǒ", "m.", "счётное слово для цветов и облаков", "used for flowers and clouds"),
        _vocab("剪刀", "jiǎndāo", "n.", "ножницы", "scissors"),
        _vocab("捡", "jiǎn", "v.", "подбирать, поднимать", "to pick up"),
        _vocab("装饰", "zhuāngshì", "n.", "украшение, декор", "decoration"),
        _vocab("结合", "jiéhé", "v.", "соединять, сочетать", "to combine, to integrate"),
        _vocab("暴雨", "bàoyǔ", "n.", "ливень", "rainstorm"),
        _vocab("紧急", "jǐnjí", "adj.", "срочный, экстренный", "urgent, emergent"),
        _vocab("劳驾", "láojià", "v.", "будьте добры, потрудитесь", "to trouble sb. to do sth."),
        _vocab("抢救", "qiǎngjiù", "v.", "спасать, срочно помогать", "to rescue, to save"),
        _vocab("腰", "yāo", "n.", "поясница, талия", "waist"),
        _vocab("直", "zhí", "adv.", "непрерывно, прямо", "continuously, straight"),
        _vocab("不然", "bùrán", "conj.", "иначе, а то", "or else, otherwise"),
        _vocab("回报", "huíbào", "v.", "воздавать, окупаться", "to repay, to requite"),
        _vocab("真理", "zhēnlǐ", "n.", "истина", "truth"),
        _vocab("浇", "jiāo", "v.", "поливать", "to water, to pour"),
        _vocab("潮湿", "cháoshī", "adj.", "влажный, сырой", "wet, moist"),
        _vocab("施肥", "shīféi", "v.", "удобрять", "to apply fertilizer"),
        _vocab("熟练", "shúliàn", "adj.", "опытный, натренированный", "skilled, practiced"),
        _vocab("应付", "yìngfu", "v.", "справляться, управляться", "to handle, to cope with"),
        _vocab("鲜艳", "xiānyàn", "adj.", "яркий, цветастый", "bright-colored"),
        _vocab("自豪", "zìháo", "adj.", "гордый", "proud"),
        _vocab("吹", "chuī", "v.", "хвастаться, дуть", "to boast, to brag"),
        _vocab("爱心", "àixīn", "n.", "любовь, милосердие", "love, compassion"),
        _vocab("分享", "fēnxiǎng", "v.", "делиться", "to share"),
        _vocab("昙花", "tánhuā", "n.", "эпифиллум (цветок)", "broad-leaved epiphyllum"),
        _vocab("庆祝", "qìngzhù", "v.", "праздновать", "to celebrate"),
        _vocab("保留", "bǎoliú", "v.", "сохранять, оставлять", "to reserve, to save"),
        _vocab("菊花", "júhuā", "n.", "хризантема", "chrysanthemum"),
        _vocab("砸", "zá", "v.", "разбивать, обрушивать", "to crush, to smash"),
        _vocab("悲伤", "bēishāng", "adj.", "печальный, скорбный", "sad, sorrowful"),
        _vocab("反正", "fǎnzhèng", "adv.", "всё равно, как бы то ни было", "anyway, no matter what"),
        _vocab("热爱", "rè'ài", "v.", "горячо любить", "to love ardently"),
    ]

    grammar = [
        {
            "word": "除非", "pos": "conj./prep.",
            "explanation": {"ru": "«除非» — союз: «только если не, разве что»; часто с «才, 否则, 不然». Как предлог: «кроме, за исключением».",
                            "en": "«除非» — conjunction: 'only if, unless'; often with 才, 否则, 不然. As preposition: 'except for'."},
            "formula": {"ru": "除非 + A，否则 + B；除非 + A，才 + B", "en": "除非 + A，否则 + B; 除非 + A，才 + B"},
            "examples": [
                {"zh": "可除非是那些好种易活、自己会奋斗的花草，否则他是不养的。",
                 "ru": "Но если это не были неприхотливые растения, умеющие бороться за себя сами, он их не разводил.",
                 "en": "But unless the plants were easy to grow and self-sufficient, he wouldn't keep them."},
                {"zh": "除非急需一大笔钱，我才会考虑卖了这房子。",
                 "ru": "Только если мне срочно понадобится крупная сумма, я подумаю о продаже дома.",
                 "en": "Only if I desperately need a big sum would I consider selling the house."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "他工作时不喜欢别人打扰，__。",
                 "answer": "除非有急事，否则别人的电话他都不接"},
            ],
        },
        {
            "word": "直", "pos": "adv.",
            "explanation": {"ru": "«直» — наречие: «прямо, напрямик, непосредственно»; также «непрерывно, постоянно».",
                            "en": "«直» — adverb: 'straight, directly'; also 'continuously, non-stop'."},
            "formula": {"ru": "直 + 单音节动词", "en": "直 + monosyllabic verb"},
            "examples": [
                {"zh": "几百盆花，要很快地抢到屋里去，累得腰酸腿疼，热汗直流。",
                 "ru": "Несколько сотен горшков нужно быстро унести в дом — до боли в пояснице и ногах, пот льётся ручьём.",
                 "en": "Hundreds of pots had to be quickly carried inside — back and legs aching, sweat pouring down."},
                {"zh": "这趟车可以直达北京，非常方便。",
                 "ru": "Этот поезд идёт прямо до Пекина, очень удобно.",
                 "en": "This train goes directly to Beijing — very convenient."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "早晨6点，闹钟在我头上__，我真不想起床。",
                 "answer": "直响"},
            ],
        },
        {
            "word": "反正", "pos": "adv.",
            "explanation": {"ru": "«反正» — наречие: «так или иначе, в любом случае, всё равно». Также подчёркивает решимость.",
                            "en": "«反正» — adverb: 'anyway, in any case, regardless'. Also emphasizes determination."},
            "formula": {"ru": "反正 + 小句", "en": "反正 + clause"},
            "examples": [
                {"zh": "我不知道花草们受我的照顾，感谢我不感谢，反正我要感谢它们。",
                 "ru": "Не знаю, благодарны ли цветы за мою заботу — но в любом случае я благодарен им.",
                 "en": "I don't know if the plants are grateful for my care — but in any case, I'm grateful to them."},
                {"zh": "你别再说了，反正我是不会考虑的。",
                 "ru": "Не говори больше — я всё равно не буду это рассматривать.",
                 "en": "Don't say any more — I won't consider it anyway."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "算了，__，还是别打扰他们了。",
                 "answer": "反正不是什么要紧事"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "应付", "word_b": "处理",
            "common": {"ru": "Оба глагола означают «принимать меры в отношении человека или дела».",
                       "en": "Both verbs mean 'to take measures towards a person or matter'."},
            "differences": [
                {"ru": "«应付» — акцент на подходящем реагировании; также «делать что-то несерьёзно, для вида».",
                 "en": "«应付» — focuses on responding appropriately; also 'to do sth perfunctorily'."},
                {"ru": "«处理» — акцент на решении проблемы; также «распоряжаться, устраивать» и «уценить, распродать».",
                 "en": "«处理» — focuses on solving a problem; also 'to arrange, dispose of' and 'to sell at a discount'."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "行为2", "ru": "Поведение 2", "en": "Behavior 2"},
        "words": [
            {"hanzi": "拆", "pinyin": "chāi", "meaning": {"zh": "", "ru": "разбирать, разбирать на части", "en": "to dismantle"}},
            {"hanzi": "撕", "pinyin": "sī", "meaning": {"zh": "", "ru": "рвать, разрывать", "en": "to tear"}},
            {"hanzi": "摸", "pinyin": "mō", "meaning": {"zh": "", "ru": "трогать, щупать", "en": "to touch"}},
            {"hanzi": "拍", "pinyin": "pāi", "meaning": {"zh": "", "ru": "хлопать, фотографировать", "en": "to pat, to shoot"}},
            {"hanzi": "抓", "pinyin": "zhuā", "meaning": {"zh": "", "ru": "хватать", "en": "to grab"}},
            {"hanzi": "捡", "pinyin": "jiǎn", "meaning": {"zh": "", "ru": "подбирать", "en": "to pick up"}},
            {"hanzi": "摘", "pinyin": "zhāi", "meaning": {"zh": "", "ru": "срывать, собирать", "en": "to pluck"}},
            {"hanzi": "披", "pinyin": "pī", "meaning": {"zh": "", "ru": "накидывать, надевать на плечи", "en": "to drape over"}},
            {"hanzi": "偷", "pinyin": "tōu", "meaning": {"zh": "", "ru": "воровать", "en": "to steal"}},
            {"hanzi": "抢", "pinyin": "qiǎng", "meaning": {"zh": "", "ru": "отбирать, хватать", "en": "to grab, to rob"}},
            {"hanzi": "捐", "pinyin": "juān", "meaning": {"zh": "", "ru": "жертвовать", "en": "to donate"}},
            {"hanzi": "扶", "pinyin": "fú", "meaning": {"zh": "", "ru": "поддерживать, помогать идти", "en": "to support"}},
            {"hanzi": "挡", "pinyin": "dǎng", "meaning": {"zh": "", "ru": "заслонять, блокировать", "en": "to block"}},
            {"hanzi": "拦", "pinyin": "lán", "meaning": {"zh": "", "ru": "останавливать, преграждать", "en": "to stop, to intercept"}},
            {"hanzi": "退", "pinyin": "tuì", "meaning": {"zh": "", "ru": "возвращать, отступать", "en": "to return, to retreat"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_36_1.mp3",
             "prompt": {"zh": "老舍养什么花？", "ru": "Какие цветы выращивал Лао Шэ?", "en": "What flowers did Lao She grow?"},
             "options": ["南方的名花", "容易养的花", "北京本地的花", "什么花都喜欢"], "answer": 1},
        ],
        "reading": [
            {"type": "mc",
             "prompt": {"zh": "作者对养花的态度是什么？", "ru": "Как автор относится к выращиванию цветов?", "en": "What is the author's attitude to gardening?"},
             "options": ["很累", "有喜有悲", "浪费时间", "没有意义"], "answer": 1},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["唯一", "她", "我生命中", "是", "在乎的人"],
             "answer": "她是我生命中唯一在乎的人。"},
            {"type": "make_sentence", "words": ["需要设计", "这次", "服装", "色彩鲜艳的", "演出"],
             "answer": "这次演出需要设计色彩鲜艳的服装。"},
            {"type": "short_essay", "words": ["奋斗", "热爱", "熟练", "庆祝", "不然"], "min_length": 80},
        ],
    }

    return {
        "title": _t("老舍与养花", "Лао Шэ и цветы", "", "Lao She and his flowers", ""),
        "audio_files": {
            "textbook_1": "textbook_36_1.mp3",
            "vocab": "vocab_36.mp3",
            "workbook_36_1": "workbook_36_1.mp3",
        },
        "warmup": {
            "question": _t(
                "你知道哪些有关养花的词语，请写在下面的横线上，并说说它们分别是什么意思。你养过花吗？介绍一下你在这方面的经验。",
                "Какие слова о выращивании цветов вы знаете? Запишите и объясните. Есть ли у вас опыт?",
                "",
                "What words about growing flowers do you know? Write them and explain. Do you have any experience?",
                ""),
            "answers": [],
        },
        "text_zh": (
            "作家老舍先生爱花，他养的花很多，满满摆了一院子。可除非是那些好种易活、自己会奋斗的花草，否则他是不养的。因为他知道北京的气候对养花来说，不算很好，想把南方的名花养活并非易事。\n"
            "老舍把养花当作一种生活乐趣。他不在乎花开得大小好坏，只要开花，他就高兴。每天老舍像好朋友似的照管着花草。工作的时候，经常写几十个字，就到院中去转转，瞧瞧这棵，看看那朵，有时拿起剪刀给它们剪剪枝，有时蹲下捡几块小石头放在花盆里做点儿装饰，然后回到屋中再写一会儿，然后再出去，就这样脑力和体力很好地结合，身心也得到放松。\n"
            "写作是件艰苦的工作，养花也是如此。有时赶上狂风暴雨，情况紧急，他就得劳驾全家人抢救花草。几百盆花，要很快地抢到屋里去，累得腰酸腿疼，热汗直流。第二天，天气好了，又得一盆盆地搬出去。可是，他并不抱怨，在他看来，任何事都要有付出，不然怎么会有回报？这是生活的真理。\n"
            "一来二去，他慢慢地总结出一些养花的经验：有的花喜干，就别多浇水；有的花喜欢潮湿的环境，就别放在太阳地里。给花换盆剪枝施肥的活儿他越做越熟练，花生病长虫他也知道如何应付了。看着院子里那鲜艳的花朵，老舍自豪地说，“不是乱吹，这就是知识啊！多得些知识，一定不是坏事。”\n"
            "老舍很有爱心，更懂得快乐要分享。每到昙花开放的时候，他就约上几位朋友来家里赏花庆祝。花分根了，一棵分为几棵，他会毫无保留地送给朋友们。看着友人高兴地拿走自己的劳动果实，老舍心里十分欢喜。有一次，送牛奶的小伙子进门就夸“好香”，这让老舍先生感到格外高兴。\n"
            "当然，也有伤心的时候。一年夏天，下了暴雨，邻居家的墙倒了，菊花被砸死了一百多棵，这下可把老舍难受坏了，一连几天人们都看不到他脸上的笑容。\n"
            "“有喜有悲，有笑有泪”，这是老舍对养花、对生活的体验。“我不知道花草们受我的照顾，感谢我不感谢，反正我要感谢它们。”老舍在自己的文章中这样写道。从中我们不难看出老舍先生对大自然的热爱，对生活的热爱。"
        ),
        "text_translation": {
            "zh": "",
            "ru": "Писатель Лао Шэ любил цветы и разводил их в большом количестве — целый двор был ими уставлен. Но брался он только за неприхотливые растения, которые сами умеют бороться за себя. Он считал выращивание цветов радостью жизни: не важно, крупные цветы или мелкие — если цветут, уже хорошо. За работой он выходил во двор, рассматривал, подрезал, подправлял — так умственный труд сочетался с физическим, и душа отдыхала. Но бывало и трудно: в грозу приходилось всей семьёй спасать цветы, переносить сотни горшков, потом обратно. Лао Шэ не жаловался: без усилий не бывает награды. Постепенно он набрался опыта: одним цветам нужно меньше воды, другим — больше тени, как удобрять и бороться с вредителями. Глядя на яркие цветы, он с гордостью говорил: «Это же знание!» Он с радостью делился с друзьями — приглашал полюбоваться эпифиллумом, раздавал отростки. Но были и печали: однажды ливень обрушил соседскую стену и убил больше сотни хризантем — Лао Шэ несколько дней ходил мрачный. «Есть радость и печаль, смех и слёзы» — так он говорил о цветах и о жизни. «Не знаю, благодарны ли цветы за мою заботу — но я благодарен им». В этих словах — любовь к природе и к жизни.",
            "tk": "",
            "en": "The writer Lao She loved flowers and grew many — the whole yard was filled with them. But he only kept easy-to-grow plants that could fend for themselves; Beijing's climate isn't ideal for gardening, and growing famous southern flowers is no easy task. Gardening was a joy of life for him: size and quality didn't matter — if they bloomed, he was happy. He tended them like dear friends; while writing, he'd often go out to the yard, inspect, prune, place pebbles for decoration — combining mental and physical activity, relaxing body and mind. But there were hard times too: in storms the whole family had to rush hundreds of pots indoors and out again — no complaining, though, since without effort there's no reward. Over time he gained experience: some flowers like dry soil, some like moisture; he grew skilled at repotting, pruning, fertilizing, and dealing with pests. Gazing at the bright blossoms he'd proudly say, 'This is knowledge!' He loved sharing: invited friends to admire the epiphyllum, gave away seedlings. But there were sorrows too: once a rainstorm knocked down a neighbour's wall and killed over a hundred chrysanthemums — Lao She was depressed for days. 'Joy and sorrow, laughter and tears' — that was his experience of flowers and life. 'I don't know if the plants are grateful for my care — but I'm grateful to them.' In those words: love of nature, love of life.",
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
                "话题讨论：人与自然。1. 描述一个给你留下深刻印象的自然景观，说说你的感受。2. 有人说，大自然和人类就像母子一样，你同意这种说法吗？3. 有人认为人类应该尊重大自然，也有人认为人类可以征服大自然，你同意哪种观点？",
                "Обсуждение: человек и природа. 1. Опишите яркое природное явление. 2. Природа и человек как мать и дитя? Согласны? 3. Уважать природу или покорять её?",
                "",
                "Discussion: human and nature. 1. Describe a striking natural scene. 2. Nature and humans like mother and child? Agree? 3. Respect or conquer nature?",
                ""),
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(12, 34, lesson34())
    save(12, 35, lesson35())
    save(12, 36, lesson36())
    print("Done.")