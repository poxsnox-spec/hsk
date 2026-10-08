# -*- coding: utf-8 -*-
"""Сборка JSON для HSK 5 (下册) — уроки 19-36."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "lessons"

LANGS = ["zh", "ru", "tk", "en", "uz", "tg", "id", "tr"]


def _t(zh, ru="", tk="", en="", uz="", tg="", id_="", tr=""):
    """Собирает словарь переводов."""
    return {"zh": zh, "ru": ru, "tk": tk, "en": en, "uz": uz, "tg": tg, "id": id_, "tr": tr}


def _vocab(hanzi, pinyin, pos, ru="", en=""):
    return {"hanzi": hanzi, "pinyin": pinyin, "pos": pos,
            "meaning": {"zh": "", "ru": ru, "tk": "", "en": en, "uz": "", "tg": "", "id": "", "tr": ""}}


def save(unit, lesson, data):
    d = DATA / f"unit{unit}"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"lesson{lesson:02d}.json"
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[+] {f.relative_to(ROOT)}")


# ============================================================
# UNIT 7 — 交流文化 (Cultural exchange) — уроки 19, 20, 21
# ============================================================

def lesson19():
    vocab = [
        _vocab("家乡", "jiāxiāng", "n.", "родина, родные места", "hometown"),
        _vocab("萝卜", "luóbo", "n.", "редька, репа", "turnip, radish"),
        _vocab("怀念", "huáiniàn", "v.", "скучать, тосковать", "to miss, to feel nostalgic"),
        _vocab("色彩", "sècǎi", "n.", "цвет, окраска", "color"),
        _vocab("想念", "xiǎngniàn", "v.", "скучать, вспоминать", "to recall with longing, to miss"),
        _vocab("青", "qīng", "adj.", "сине-зелёный", "greenish blue"),
        _vocab("紫", "zǐ", "adj.", "фиолетовый", "purple"),
        _vocab("赏心悦目", "shǎngxīn-yuèmù", "идиом", "услада для глаз", "pleasing to both the eye and the mind"),
        _vocab("般", "bān", "part.", "словно, как", "sort, kind"),
        _vocab("清淡", "qīngdàn", "adj.", "лёгкий, нежирный", "lightly flavored and not greasy"),
        _vocab("可口", "kěkǒu", "adj.", "вкусный", "tasty, delicious"),
        _vocab("夸", "kuā", "v.", "хвалить", "to praise"),
        _vocab("橘子", "júzi", "n.", "мандарин", "tangerine"),
        _vocab("梨", "lí", "n.", "груша", "pear"),
        _vocab("炒", "chǎo", "v.", "жарить в воке", "to stir-fry"),
        _vocab("煮", "zhǔ", "v.", "варить", "to boil, to stew"),
        _vocab("油炸", "yóuzhá", "v.", "жарить во фритюре", "to deep-fry"),
        _vocab("切", "qiē", "v.", "резать", "to cut, to chop, to slice"),
        _vocab("丝", "sī", "n.", "соломка, нить", "shred, anything threadlike"),
        _vocab("搅拌", "jiǎobàn", "v.", "размешивать", "to stir, to mix"),
        _vocab("均匀", "jūnyún", "adj.", "равномерный", "even, well-distributed"),
        _vocab("原料", "yuánliào", "n.", "сырьё, ингредиент", "raw material"),
        _vocab("擀", "gǎn", "v.", "раскатывать тесто", "to roll (dough etc.)"),
        _vocab("薄", "báo", "adj.", "тонкий", "thin"),
        _vocab("折叠", "zhédié", "v.", "складывать", "to fold"),
        _vocab("透明", "tòumíng", "adj.", "прозрачный", "transparent"),
        _vocab("淋", "lín", "v.", "поливать, разбрызгивать", "to spatter, to sprinkle"),
        _vocab("圈", "quān", "n.", "круг, кольцо", "circle, ring"),
        _vocab("烫", "tàng", "v./adj.", "обжигать; очень горячий", "to scald; scalding"),
        _vocab("盖", "gài", "v./n.", "накрывать; крышка", "to cover; lid"),
        _vocab("预防", "yùfáng", "v.", "предотвращать", "to guard against, to prevent"),
        _vocab("糊", "hú", "v.", "подгорать", "to be burnt"),
        _vocab("文火", "wénhuǒ", "n.", "слабый огонь", "slow fire, gentle heat"),
        _vocab("闻", "wén", "v.", "нюхать; слышать", "to smell"),
        _vocab("口味", "kǒuwèi", "n.", "вкус, пристрастие", "taste, flavor"),
        _vocab("少许", "shǎoxǔ", "adj.", "немного, чуть-чуть", "a little, some"),
        _vocab("酱油", "jiàngyóu", "n.", "соевый соус", "soy sauce"),
        _vocab("醋", "cù", "n.", "уксус", "vinegar"),
        _vocab("焦", "jiāo", "adj.", "подгоревший", "burnt, scorched"),
        _vocab("嫩", "nèn", "adj.", "нежный, мягкий", "soft, tender"),
        _vocab("特色", "tèsè", "n.", "характерная черта", "characteristic, distinctive feature"),
        _vocab("痰", "tán", "n.", "мокрота", "phlegm, sputum"),
        _vocab("平安", "píng'ān", "adj.", "спокойный, в безопасности", "safe, well"),
    ]

    grammar = [
        {
            "word": "般", "pos": "part.",
            "explanation": {
                "ru": "«般» — частица, означает «словно», «как». Ставится после существительного, образует определительную или обстоятельственную конструкцию.",
                "en": "«般» is a particle meaning 'like', 'as if'. Attached to a noun to form an attributive or adverbial phrase.",
            },
            "formula": {"ru": "сущ. + 般 + сущ. / 般 + 的 + сущ.", "en": "noun + 般 + noun / 般 + 的 + noun"},
            "examples": [
                {"zh": "紫的像山泉般清淡可口。", "ru": "Фиолетовая — словно горный ручей, лёгкая и вкусная.", "en": "The purple ones are light and tasty like a mountain spring."},
                {"zh": "说起那段往事，她的脸上露出了阳光般的笑容。", "ru": "Говоря о прошлом, её лицо озарила солнечная улыбка.", "en": "Speaking of the past, a sunny smile lit her face."},
                {"zh": "望着爸爸远去的背影，我的眼泪雨点般不停地往下掉。", "ru": "Глядя на удаляющуюся спину отца, мои слёзы падали, как дождь.", "en": "Watching my father's receding back, my tears fell like raindrops."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "他在下半场的进球，为球队赢得了一场像金子一样宝贵的胜利。他在下半场的进球，__。", "answer": "为球队赢得了一场金子般的胜利。"},
            ],
        },
        {
            "word": "闻", "pos": "v.",
            "explanation": {
                "ru": "«闻» как морфема означает «слышать, слух, новость». Как глагол — «нюхать, обонять».",
                "en": "«闻» as a morpheme means 'to hear, hearing, news'. As a verb — 'to smell'.",
            },
            "examples": [
                {"zh": "火最好用文火，等能闻到香味时，便可开锅了。", "ru": "Огонь лучше слабый; когда почувствуете аромат, можно открывать.", "en": "Use gentle heat; when you can smell the aroma, open the pot."},
                {"zh": "你们到各地去旅游，一定会增加对中国的了解，老话说：百闻不如一见。", "ru": "Путешествуя, вы лучше узнаете Китай — недаром говорят: «лучше один раз увидеть».", "en": "Travelling will increase your understanding of China — as the saying goes: 'seeing once is better than hearing a hundred times'."},
            ],
            "exercises": [
                {"type": "translate", "question": "Определите значение 闻: она приняла позицию 听而不闻 (слушать и не слышать).", "answer": "«слышать»"},
            ],
        },
        {
            "word": "趁", "pos": "prep.",
            "explanation": {
                "ru": "«趁» — предлог «воспользоваться (временем, случаем)». После него может стоять существительное, глагольная фраза, прилагательное или целое предложение.",
                "en": "«趁» is a preposition meaning 'to take advantage of (time, opportunity)'. Can be followed by noun, verb phrase, adjective, or clause.",
            },
            "formula": {"ru": "趁 + сущ./фраза/прил.", "en": "趁 + noun/verb phrase/adj."},
            "examples": [
                {"zh": "趁着这几天休息，我们去看看房子吧。", "ru": "Воспользуемся этими выходными и посмотрим дом.", "en": "Let's take these days off to look at houses."},
                {"zh": "趁电影还没开始，我去买两瓶矿泉水。", "ru": "Пока фильм не начался, схожу за водой.", "en": "While the movie hasn't started, I'll buy two bottles of water."},
                {"zh": "萝卜饼要趁热吃。", "ru": "Луобобин нужно есть горячим.", "en": "Turnip pancakes should be eaten hot."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "李老师退休了，她想__。", "answer": "趁这个机会好好休息一下。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "怀念", "word_b": "想念",
            "common": {"ru": "Оба — глаголы, оба выражают неспособность забыть человека или место, тоску по кому-то/чему-то.", "en": "Both are verbs, both express inability to forget a person or place, longing."},
            "differences": [
                {"ru": "«怀念» — книжный стиль, акцент на «часто вспоминать, не забывать».", "en": "«怀念» — literary; focuses on 'often remembering, not forgetting'."},
                {"ru": "«想念» — разговорный, акцент на «хочу увидеть кого-то».", "en": "«想念» — colloquial; focuses on 'wanting to see someone'."},
                {"ru": "«怀念» чаще об умерших или недоступных местах.", "en": "«怀念» more for the deceased or inaccessible places."},
                {"ru": "«想念» чаще о живых или о местах, которые можно вновь посетить.", "en": "«想念» more for the living or revisitable places."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "饮食 (Питание)", "ru": "Еда и напитки", "en": "Food and drink"},
        "words": [
            {"hanzi": "零食", "pinyin": "língshí", "meaning": {"zh": "", "ru": "перекус", "en": "snack", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "冰激凌", "pinyin": "bīngjīlíng", "meaning": {"zh": "", "ru": "мороженое", "en": "ice cream", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "酱油", "pinyin": "jiàngyóu", "meaning": {"zh": "", "ru": "соевый соус", "en": "soy sauce", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "醋", "pinyin": "cù", "meaning": {"zh": "", "ru": "уксус", "en": "vinegar", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "开水", "pinyin": "kāishuǐ", "meaning": {"zh": "", "ru": "кипяток", "en": "boiled water", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "点心", "pinyin": "diǎnxin", "meaning": {"zh": "", "ru": "закуска, пирожное", "en": "pastry, dim sum", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "营养", "pinyin": "yíngyǎng", "meaning": {"zh": "", "ru": "питание", "en": "nutrition", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "口味", "pinyin": "kǒuwèi", "meaning": {"zh": "", "ru": "вкус", "en": "taste", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "胃口", "pinyin": "wèikǒu", "meaning": {"zh": "", "ru": "аппетит", "en": "appetite", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "淡", "pinyin": "dàn", "meaning": {"zh": "", "ru": "пресный", "en": "bland", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "臭", "pinyin": "chòu", "meaning": {"zh": "", "ru": "вонючий", "en": "smelly", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "软", "pinyin": "ruǎn", "meaning": {"zh": "", "ru": "мягкий", "en": "soft", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "嫩", "pinyin": "nèn", "meaning": {"zh": "", "ru": "нежный", "en": "tender", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
            {"hanzi": "过期", "pinyin": "guòqī", "meaning": {"zh": "", "ru": "просроченный", "en": "expired", "tk": "", "uz": "", "tg": "", "id": "", "tr": ""}},
        ],
    }

    workbook = {
        "listening": [
            {
                "type": "mc", "audio": "workbook_19_1.mp3",
                "prompt": {"zh": "男的和女的是什么关系？", "ru": "Кем являются мужчина и женщина?", "en": "What is the relationship between the man and the woman?"},
                "options": ["同事", "夫妻", "顾客和老板", "客人和服务员"],
                "answer": 3,
            },
            {
                "type": "mc", "audio": "workbook_19_1.mp3",
                "prompt": {"zh": "女的为什么不想做饭？", "ru": "Почему женщина не хочет готовить?", "en": "Why doesn't the woman want to cook?"},
                "options": ["她不会做", "她太累了", "她不喜欢吃中餐", "她做的不好吃"],
                "answer": 3,
            },
        ],
        "reading": [
            {
                "type": "cloze",
                "text_zh": "白菜是十字花科的蔬菜，原产于中国北方，后引种南方，直到19世纪才传入日本和欧美。白菜在中国的栽种历史非常15，早在三国时期的《吴录》中，就有“陆逊催人种豆、菘”这样的内容，“菘”指的就是白菜。不过，到了隋唐以后，白菜的种植才得到大面积16。",
                "blanks": [
                    {"position": 15, "answer": "悠久", "options": ["清楚", "简单", "悠久", "复杂"]},
                    {"position": 16, "answer": "推广", "options": ["上升", "接受", "利用", "推广"]},
                ],
            },
        ],
        "writing": [
            {"type": "make_sentence", "words": ["要", "才好", "饺子", "趁热吃", "煮熟后"], "answer": "饺子煮熟后要趁热吃才好。"},
            {"type": "make_sentence", "words": ["像", "吹来", "深夜的", "刀子般地", "寒风"], "answer": "深夜的寒风吹来，像刀子般地（割在脸上）。"},
            {"type": "make_sentence", "words": ["我", "一股", "就闻到", "一进门", "扑鼻的香味"], "answer": "我一进门就闻到一股扑鼻的香味。"},
            {"type": "short_essay", "words": ["口味", "特色", "色彩", "想念", "趁"], "min_length": 80},
        ],
    }

    return {
        "title": _t("家乡的萝卜饼", "Луобобин родных мест", "", "Turnip pancakes in my hometown", "", "", "", ""),
        "audio_files": {
            "textbook_1": "textbook_19_1.mp3",
            "vocab": "vocab_19.mp3",
            "workbook_19_1": "workbook_19_1.mp3",
        },
        "warmup": {
            "question": _t(
                "下面的图片分别表示三种做菜的方法，请从本课的生词表中找出对应的说法，然后给它们排个顺序，并说说你为什么这么排序。",
                "На картинках три способа готовки — найдите соответствующие слова из нового словаря урока, расставьте их по порядку и объясните, почему.",
                "",
                "The pictures show three cooking methods — find the corresponding words in this lesson's vocabulary, order them, and explain why.",
            ),
            "answers": ["炒", "油炸", "煮"],
        },
        "text_zh": "家乡的众多美食中，萝卜饼是最让我怀念的。它那丰富的色彩、微甜的口感，至今仍让我十分想念。\n家乡的萝卜有青、红、紫三种。三种萝卜看起来赏心悦目，吃起来，青的甜中带点儿辣，红的辣中带着甜，紫的像山泉般清淡可口。父老乡亲们夸它说：“橘子、葡萄、梨，比不上咱的萝卜皮。”而萝卜饼就是用这三种颜色的萝卜做成的。\n萝卜饼的做法极其简单，既不必炒或煮，也不用油炸。先把三色萝卜洗净切丝，放入油、盐等，用筷子搅拌均匀，萝卜饼的原料便做成了。最关键的功夫是擀面。高手往往把面擀得薄如白纸，拌好的萝卜丝儿铺到饼上后，得再折叠两三次，要求饼熟之后表皮是透明的，能透过表皮看见萝卜丝儿。最后用刀切成块状，饼便做好了。\n接下来，拿一个平底锅，先在锅里淋一圈油，待油锅烫手时，将切好的萝卜饼一块一块地放进锅里。盖锅前须放进一些温水，预防糊底。火最好用文火，等能闻到香味时，便可开锅了。萝卜饼要趁热吃，喜欢口味重的，还可以加少许酱油和醋。刚出锅的萝卜饼，香味扑鼻，外焦里嫩，吃上一口，便让人永远忘不了。\n如今，美食家们对吃提出了更高的要求。他们不仅要观色、闻香、尝味、赏形，而且还要求食物具有养生方面的特色。我想，家乡的萝卜饼完全具备这几个方面的条件，人们不是常说吗——“鱼生火，肉生痰，青菜萝卜保平安”，养生的功能，让我更加喜爱它了。",
        "text_translation": {
            "zh": "",
            "ru": "Из многих блюд родных мест именно луобобин я вспоминаю с особой нежностью. Его богатая палитра, чуть сладкий вкус — до сих пор скучаю по нему.\nРедька у нас бывает трёх цветов: сине-зелёная, красная и фиолетовая. Все три радуют глаз: сине-зелёная — сладкая с легкой остринкой, красная — острая со сладостью, фиолетовая — словно горный ручей, лёгкая и вкусная. Земляки хвалят её: «Мандарин, виноград, груша — не сравнятся с нашей редечной кожурой». А луобобин как раз и делают из этих трёх видов редьки.\nГотовится луобобин предельно просто: не нужно ни жарить, ни варить, ни обжаривать во фритюре. Сначала трёхцветную редьку моют и шинкуют, добавляют масло, соль, размешивают палочками — начинка готова. Самое важное — раскатать тесто. Мастера раскатывают его тонким, как бумага, выкладывают начинку и складывают два-три раза — после готовки корка должна быть прозрачной, сквозь неё видны волокна редьки. В конце нарезают ножом на куски —饼 готов.\nЗатем берут сковороду, наливают по кругу масло; когда масло станет горячим, выкладывают куски луобобина один за другим. Перед закрытием крышки добавляют немного тёплой воды, чтобы не подгорело дно. Огонь лучше слабый: когда почувствуете аромат — можно открывать. Луобобин едят горячим; любители поострее могут добавить немного соевого соуса и уксуса. Только что со сковороды — аромат бьёт в нос, снаружи хрустящий, внутри нежный: попробуешь раз — не забудешь вовек.\nСегодня гурманы предъявляют к еде всё более высокие требования: не только смотреть на цвет, вдыхать аромат, пробовать вкус и любоваться формой, но и требовать от пищи оздоровительных свойств. Думаю, луобобин родных мест полностью отвечает всем этим условиям — недаром говорят: «Рыба рождает жар, мясо — мокроту, а зелень и редька хранят покой». Именно польза для здоровья заставляет меня любить его ещё больше.",
            "tk": "", "en": "Among the many delicacies of my hometown, turnip pancakes are what I miss most. Their rich colors and slightly sweet taste still make me nostalgic.\nThe local turnips come in three colors: greenish-blue, red and purple. All three are pleasing to the eye. The greenish ones are sweet with a hint of spice; the red ones are spicy with sweetness; the purple ones are light and tasty like a mountain spring. The elders praise them: 'Tangerines, grapes, pears — none compare to our turnip peel.' And turnip pancakes are made from exactly these three colors.\nMaking turnip pancakes is extremely simple — no stir-frying, boiling or deep-frying needed. First, wash and shred the three-colored turnips, add oil and salt, stir with chopsticks — the filling is ready. The crucial step is rolling the dough. Masters roll it thin as paper; after spreading the filling, fold it two or three times — when cooked the skin should be transparent, revealing the shredded turnip inside. Finally cut into pieces with a knife — the pancake is done.\nNext, take a frying pan, pour a ring of oil; when hot, place the pancake pieces one by one. Before covering, add some warm water to prevent burning. Use gentle heat; when you can smell the aroma, open the lid. Turnip pancakes should be eaten hot; those who like stronger flavors can add a little soy sauce and vinegar. Fresh from the pan, they smell wonderful — crisp outside and tender inside; one bite and you'll never forget them.\nToday foodies demand more: not just color, aroma, taste and shape, but also health benefits. I think my hometown's turnip pancakes meet all these conditions — as the saying goes: 'Fish causes heat, meat causes phlegm, green vegetables and turnip keep you safe.' Its health benefits make me love it even more.",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "中国菜：你喜欢什么口味的菜？不喜欢什么味道的菜？你比较喜欢哪些中国菜？你学过做中国菜吗？",
                "Китайская кухня: какие вкусы вам нравятся, а какие — нет? Какие китайские блюда предпочитаете? Пробовали готовить сами?",
                "",
                "Chinese cuisine: what flavors do you like or dislike? Which Chinese dishes do you prefer? Have you ever cooked one?",
            ),
            "writing_prompt": {
                "zh": "请以“我喜欢/会做的中国菜”为题，谈谈你这方面的经历。尽量用上本课所学的生词，字数不少于100字。",
                "ru": "Напишите эссе на тему «Китайское блюдо, которое я люблю / умею готовить». Используйте слова урока, не менее 100 иероглифов.",
                "en": "Write an essay titled 'The Chinese dish I like / can cook'. Use this lesson's vocabulary, at least 100 characters.",
            },
        },
        "workbook": workbook,
    }


# ============================================================
if __name__ == "__main__":
    save(7, 19, lesson19())
    print("Done.")