import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, JobQueue
)

ADMIN_ID = 604663433  # Твой Telegram ID для напоминаний

TOKEN = os.environ.get("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")

# ──────────────────────────────────────────────
#  БАЗА ВОПРОСОВ
# ──────────────────────────────────────────────
QUESTIONS = {
    "A": [
        {
            "ru": "Что такое ассюранс-задание?",
            "en": "What is an assurance engagement?",
            "opts_ru": [
                "Аудитор составляет отчётность вместо клиента",
                "Профессионал выражает заключение, повышающее доверие к предмету проверки",
                "Консультация по налогам",
                "Внутренняя проверка компанией своих процессов"
            ],
            "opts_en": [
                "The auditor prepares financial statements for the client",
                "A practitioner expresses a conclusion to enhance confidence in a subject matter",
                "A tax advisory service",
                "An internal review of company processes"
            ],
            "correct": 1,
            "explain_ru": "Ассюранс-задание (assurance engagement) — задание, в котором независимый профессионал изучает предмет (например, финансовую отчётность) и выдаёт заключение для повышения уверенности пользователей.",
            "explain_en": "An assurance engagement is one in which a practitioner expresses a conclusion designed to enhance the degree of confidence of intended users about the outcome of the evaluation of a subject matter."
        },
        {
            "ru": "Главная цель внешнего аудита финансовой отчётности?",
            "en": "What is the primary objective of an external audit?",
            "opts_ru": [
                "Найти все мошенничества в компании",
                "Выразить независимое мнение о достоверности финансовой отчётности",
                "Подготовить отчётность для налоговой",
                "Проверить эффективность работы сотрудников"
            ],
            "opts_en": [
                "To detect all fraud in the company",
                "To express an independent opinion on whether the financial statements give a true and fair view",
                "To prepare financial statements for tax purposes",
                "To assess employee performance"
            ],
            "correct": 1,
            "explain_ru": "Главная цель внешнего аудита — выразить независимое мнение (opinion) о том, отражает ли отчётность достоверно положение дел. Аудитор НЕ гарантирует нахождение всего мошенничества.",
            "explain_en": "The primary objective of an external audit is to express an opinion on whether the financial statements give a true and fair view. The auditor does NOT guarantee detection of all fraud."
        },
        {
            "ru": "Что означает профессиональный скептицизм (professional scepticism)?",
            "en": "What does professional scepticism mean?",
            "opts_ru": [
                "Аудитор не доверяет никому и думает, что клиент всегда врёт",
                "Аудитор критически оценивает доказательства, не принимая их слепо на веру",
                "Аудитор соглашается со всем, что говорит клиент",
                "Аудитор отказывается от задания при любых рисках"
            ],
            "opts_en": [
                "The auditor trusts no one and assumes the client always lies",
                "The auditor critically assesses evidence without blind acceptance",
                "The auditor agrees with everything management says",
                "The auditor refuses any engagement with risks"
            ],
            "correct": 1,
            "explain_ru": "Профессиональный скептицизм — баланс: аудитор не верит всему слепо, но и не подозревает всех автоматически. Он критически проверяет доказательства.",
            "explain_en": "Professional scepticism is an attitude that includes a questioning mind and critical assessment of audit evidence. It is a balance — not blind trust, but not automatic suspicion either."
        },
        {
            "ru": "Почему независимость аудитора важна?",
            "en": "Why is auditor independence important?",
            "opts_ru": [
                "Чтобы аудитор мог брать задания от одного клиента бесконечно",
                "Без независимости мнение аудитора теряет ценность для пользователей",
                "Независимость нужна только для госкомпаний",
                "Чтобы аудитор не платил налоги с гонорара"
            ],
            "opts_en": [
                "So the auditor can work for one client indefinitely",
                "Without independence, the auditor's opinion loses its value to users",
                "Independence is only required for public sector audits",
                "So the auditor pays no tax on fees"
            ],
            "correct": 1,
            "explain_ru": "Независимость бывает двух видов: в мышлении (independence of mind) и внешняя (independence in appearance). Если пользователи думают, что аудитор зависит от клиента — они не будут доверять его заключению.",
            "explain_en": "Independence has two aspects: independence of mind and independence in appearance. If users believe the auditor is not independent, they will not trust the audit opinion — making it worthless."
        },
    ],
    "B": [
        {
            "ru": "Из каких трёх компонентов состоит аудиторский риск?",
            "en": "What are the three components of audit risk?",
            "opts_ru": [
                "Риск мошенничества, риск ошибки, риск банкротства",
                "Неотъемлемый риск, риск контроля, риск необнаружения",
                "Налоговый риск, операционный риск, финансовый риск",
                "Риск клиента, риск аудитора, риск рынка"
            ],
            "opts_en": [
                "Fraud risk, error risk, bankruptcy risk",
                "Inherent risk, control risk, detection risk",
                "Tax risk, operational risk, financial risk",
                "Client risk, auditor risk, market risk"
            ],
            "correct": 1,
            "explain_ru": "Аудиторский риск = Неотъемлемый риск (IR) × Риск контроля (CR) × Риск необнаружения (DR). Первые два аудитор оценивает, третий — контролирует сам через процедуры.",
            "explain_en": "Audit Risk = Inherent Risk × Control Risk × Detection Risk. The auditor assesses IR and CR, then sets DR accordingly by choosing the nature, timing and extent of audit procedures."
        },
        {
            "ru": "Что такое существенность (materiality)?",
            "en": "What is materiality in auditing?",
            "opts_ru": [
                "Сумма всех активов компании",
                "Порог, при превышении которого ошибка влияет на решения пользователей",
                "Минимальная сумма дебиторской задолженности для проверки",
                "Размер аудиторского гонорара"
            ],
            "opts_en": [
                "The total value of company assets",
                "The threshold above which a misstatement could influence users' decisions",
                "The minimum receivable balance subject to testing",
                "The size of the audit fee"
            ],
            "correct": 1,
            "explain_ru": "Существенность (materiality) — пороговое значение. Если ошибка выше этого порога, она может изменить решение пользователя. Аудитор устанавливает уровень существенности сам — обычно % от выручки, прибыли или активов.",
            "explain_en": "Materiality is the threshold above which a misstatement, individually or in aggregate, could influence the economic decisions of users. It is typically set as a percentage of revenue, profit or total assets."
        },
        {
            "ru": "Что описывает высокий неотъемлемый риск (inherent risk)?",
            "en": "Which best describes high inherent risk?",
            "opts_ru": [
                "Компания использует надёжную систему внутреннего контроля",
                "Компания работает в волатильной отрасли со сложными операциями",
                "Аудитор хорошо знает отрасль клиента",
                "Компания давно на рынке со стабильными показателями"
            ],
            "opts_en": [
                "The company has a reliable internal control system",
                "The company operates in a volatile industry with complex transactions",
                "The auditor has strong industry knowledge",
                "The company has been in business for years with stable results"
            ],
            "correct": 1,
            "explain_ru": "Неотъемлемый риск (inherent risk) — риск того, что статья отчётности подвержена ошибкам по своей природе, независимо от контроля. Волатильные активы, субъективные оценки, сложные операции — всё это повышает IR.",
            "explain_en": "Inherent risk is the susceptibility of an assertion to a material misstatement, assuming no related controls. Complex transactions, subjective estimates and volatile industries increase inherent risk."
        },
        {
            "ru": "Что означает принцип непрерывности деятельности (going concern)?",
            "en": "What does the going concern principle mean?",
            "opts_ru": [
                "Компания планирует продать бизнес в течение года",
                "Предположение о том, что компания будет работать минимум 12 месяцев",
                "Компания обязана публиковать отчётность каждый квартал",
                "Аудитор проверяет компанию непрерывно без перерывов"
            ],
            "opts_en": [
                "The company plans to sell its business within one year",
                "The assumption that the entity will continue operating for at least 12 months",
                "The company must publish quarterly reports",
                "The auditor monitors the company on a continuous basis"
            ],
            "correct": 1,
            "explain_ru": "Going concern — базовое допущение: компания будет работать минимум 12 месяцев с даты отчётности. Аудитор обязан оценить угрозы этому принципу. Признаки угрозы: убытки, потеря клиентов, судебные иски.",
            "explain_en": "Going concern is the assumption that the entity will continue in operational existence for at least 12 months from the balance sheet date. The auditor must evaluate whether this assumption is appropriate."
        },
    ],
    "C": [
        {
            "ru": "Главная цель системы внутреннего контроля?",
            "en": "What is the main purpose of internal controls?",
            "opts_ru": [
                "Полностью исключить ошибки и мошенничество",
                "Дать разумную уверенность в достижении целей и надёжности отчётности",
                "Заменить работу внешнего аудитора",
                "Контролировать личные расходы сотрудников"
            ],
            "opts_en": [
                "To completely eliminate errors and fraud",
                "To provide reasonable assurance regarding achievement of objectives",
                "To replace the work of the external auditor",
                "To monitor personal employee expenses"
            ],
            "correct": 1,
            "explain_ru": "Внутренний контроль даёт только разумную уверенность (reasonable assurance), но не абсолютную. Причины: сговор сотрудников (collusion), нарушение правил, обход контроля руководством (management override).",
            "explain_en": "Internal controls provide only reasonable, not absolute, assurance. Limitations include collusion between employees, management override of controls, and human error."
        },
        {
            "ru": "Что такое разделение обязанностей (segregation of duties)?",
            "en": "What is segregation of duties?",
            "opts_ru": [
                "Разделение работы для повышения скорости",
                "Один человек не контролирует всю цепочку операции — снижает риск мошенничества",
                "Распределение задач по сложности между сотрудниками",
                "Система отпусков в бухгалтерии"
            ],
            "opts_en": [
                "Splitting work between departments to increase speed",
                "No single person controls an entire transaction — reduces fraud risk",
                "Allocating tasks by complexity among staff",
                "A leave management system for the finance team"
            ],
            "correct": 1,
            "explain_ru": "Разделение обязанностей (segregation of duties) — ключевой контроль: один человек не должен авторизовывать, выполнять и записывать одну операцию. Пример: тот, кто заказывает товар, не должен его и оплачивать.",
            "explain_en": "Segregation of duties ensures that no single individual controls all stages of a transaction (authorisation, execution, recording). Example: the person ordering goods should not also approve payment."
        },
        {
            "ru": "Что делает аудитор при обнаружении существенного недостатка контроля?",
            "en": "What does the auditor do when a significant control deficiency is found?",
            "opts_ru": [
                "Немедленно прекращает аудит",
                "Сообщает лицам, наделённым полномочиями (комитету по аудиту / руководству)",
                "Самостоятельно исправляет недостаток",
                "Игнорирует, если это не влияет на мнение"
            ],
            "opts_en": [
                "Immediately terminates the audit",
                "Reports it to those charged with governance (audit committee / management)",
                "Fixes the deficiency themselves",
                "Ignores it if it does not affect the opinion"
            ],
            "correct": 1,
            "explain_ru": "При обнаружении недостатков контроля аудитор сообщает тем, кто наделён полномочиями (those charged with governance) — совет директоров или комитет по аудиту. Аудитор НЕ исправляет сам — это угрожало бы независимости.",
            "explain_en": "The auditor must communicate significant deficiencies to those charged with governance (e.g. audit committee or board). The auditor must NOT fix deficiencies — doing so would compromise independence."
        },
    ],
    "D": [
        {
            "ru": "Какие доказательства считаются наиболее надёжными?",
            "en": "Which type of audit evidence is most reliable?",
            "opts_ru": [
                "Устные объяснения менеджмента клиента",
                "Документы от третьих лиц, полученные аудитором напрямую",
                "Внутренние документы, подготовленные бухгалтерией клиента",
                "Личные наблюдения аудитора без документального подтверждения"
            ],
            "opts_en": [
                "Oral explanations from client management",
                "Documents from third parties obtained directly by the auditor",
                "Internal documents prepared by the client's accounting team",
                "Auditor observations without documentary support"
            ],
            "correct": 1,
            "explain_ru": "Доказательства от третьих лиц, полученные напрямую аудитором (external evidence obtained directly) — наиболее надёжные. Пример: банковское подтверждение, пришедшее от банка напрямую. Менее надёжны внутренние документы клиента.",
            "explain_en": "External evidence obtained directly by the auditor is the most reliable. Example: a bank confirmation sent directly to the auditor by the bank. Client-generated internal documents are less reliable."
        },
        {
            "ru": "Что такое процедуры по существу (substantive procedures)?",
            "en": "What are substantive procedures?",
            "opts_ru": [
                "Тесты, проверяющие работу систем внутреннего контроля",
                "Процедуры, направленные на выявление существенных искажений в отчётности",
                "Анализ организационной структуры клиента",
                "Проверка квалификации сотрудников бухгалтерии"
            ],
            "opts_en": [
                "Tests that check whether internal controls are operating effectively",
                "Procedures designed to detect material misstatements in financial statements",
                "Analysis of the client's organisational structure",
                "Assessment of the qualifications of accounting staff"
            ],
            "correct": 1,
            "explain_ru": "Процедуры по существу (substantive procedures) делятся на: аналитические процедуры (analytical procedures) — сравнение цифр, коэффициентов; и детальные тесты (tests of detail) — проверка конкретных документов и остатков.",
            "explain_en": "Substantive procedures consist of: analytical procedures (comparing figures and ratios) and tests of detail (examining specific transactions, balances and disclosures). Both aim to detect material misstatements."
        },
        {
            "ru": "Почему аудиторы проверяют выборку (sample), а не 100% операций?",
            "en": "Why do auditors test a sample rather than 100% of transactions?",
            "opts_ru": [
                "Закон запрещает проверять все документы клиента",
                "Проверка всех операций нецелесообразна по времени и стоимости",
                "Клиент разрешает смотреть не более 50% документов",
                "Аудиторские стандарты требуют проверять ровно 25%"
            ],
            "opts_en": [
                "The law prohibits auditors from examining all client documents",
                "Testing 100% is impractical in terms of time and cost",
                "The client only permits access to 50% of documents",
                "Auditing standards require exactly 25% to be tested"
            ],
            "correct": 1,
            "explain_ru": "Аудиторская выборка (audit sampling) применяется когда проверка 100% нецелесообразна. По выборке аудитор делает выводы обо всей совокупности. Риск выборки (sampling risk) — вывод может не совпасть с реальностью всей совокупности.",
            "explain_en": "Audit sampling is used when it is not practical to test 100% of items. The auditor draws conclusions about the entire population from the sample. Sampling risk is the risk that the conclusion differs from what a 100% test would show."
        },
        {
            "ru": "Что проверяет аудитор при аудите запасов (inventory)?",
            "en": "What does the auditor test when auditing inventory?",
            "opts_ru": [
                "Только цены закупок",
                "Существование, полноту, оценку и права собственности на запасы",
                "Только физическое наличие запасов",
                "Только документы на отгрузку"
            ],
            "opts_en": [
                "Purchase prices only",
                "Existence, completeness, valuation and rights over inventory",
                "Physical presence of inventory only",
                "Delivery documents only"
            ],
            "correct": 1,
            "explain_ru": "При аудите запасов аудитор проверяет: существование (физический подсчёт), полноту (всё ли учтено), оценку (правильность стоимости, NRV), права собственности (принадлежит ли компании). Физическое наблюдение (physical observation) — ключевая процедура.",
            "explain_en": "When auditing inventory, the auditor tests: existence (physical count observation), completeness (all items recorded), valuation (cost vs NRV), and rights (ownership belongs to the entity). Physical observation is the key procedure."
        },
        {
            "ru": "Что такое внешнее подтверждение (external confirmation) и когда оно используется?",
            "en": "What is external confirmation and when is it used?",
            "opts_ru": [
                "Письмо от менеджмента клиента аудитору",
                "Прямой запрос аудитора третьей стороне для подтверждения данных",
                "Внутренняя проверка данных компанией",
                "Запрос в налоговую о задолженности клиента"
            ],
            "opts_en": [
                "A letter from client management to the auditor",
                "A direct request from the auditor to a third party to confirm information",
                "An internal data check by the company",
                "A request to the tax authority about the client's liabilities"
            ],
            "correct": 1,
            "explain_ru": "Внешнее подтверждение (external confirmation) — аудитор напрямую обращается к третьей стороне. Примеры: банковское подтверждение (bank confirmation), подтверждение дебиторской задолженности (debtor circularisation). Это одно из самых надёжных доказательств.",
            "explain_en": "External confirmation is a direct written response from a third party to the auditor. Examples: bank confirmation, debtor circularisation. It is among the most reliable forms of audit evidence because it comes from an independent source."
        },
        {
            "ru": "Как аудитор проверяет выручку (revenue)?",
            "en": "How does the auditor test revenue?",
            "opts_ru": [
                "Только запрашивает объяснения у менеджмента",
                "Аналитические процедуры + детальные тесты на реальность и полноту операций",
                "Только сверяет данные с налоговой декларацией",
                "Только проверяет банковские выписки"
            ],
            "opts_en": [
                "Only asks management for explanations",
                "Analytical procedures + tests of detail for occurrence and completeness",
                "Only reconciles to the tax return",
                "Only reviews bank statements"
            ],
            "correct": 1,
            "explain_ru": "При аудите выручки: аналитические процедуры (сравнение с прошлым годом, расчёт средней цены × объём), тесты на реальность операций (occurrence — подтверждение что продажи были), полноту (completeness — всё ли учтено). Риск завышения выручки всегда высокий.",
            "explain_en": "For revenue: analytical procedures (compare to prior year, price × volume analysis) plus tests of detail for occurrence (sales actually happened) and completeness (all sales recorded). Revenue is high-risk as management may overstate it."
        },
    ],
    "E": [
        {
            "ru": "Когда аудитор выдаёт немодифицированное заключение (unmodified opinion)?",
            "en": "When does the auditor issue an unmodified opinion?",
            "opts_ru": [
                "Когда компания является государственной",
                "Когда финансовая отчётность достоверна во всех существенных аспектах",
                "Когда аудит проводится впервые",
                "Когда клиент платит гонорар вовремя"
            ],
            "opts_en": [
                "When the company is state-owned",
                "When the financial statements give a true and fair view in all material respects",
                "When it is the first audit of the entity",
                "When the client pays the audit fee on time"
            ],
            "correct": 1,
            "explain_ru": "Немодифицированное заключение (unmodified / clean opinion) выдаётся, когда отчётность составлена верно во всех существенных аспектах. Это лучший результат для клиента. Модифицированные: Qualified, Adverse, Disclaimer.",
            "explain_en": "An unmodified (clean) opinion is issued when the financial statements give a true and fair view in all material respects. Modified opinions include: qualified, adverse, and disclaimer of opinion."
        },
        {
            "ru": "Разница между Qualified и Adverse opinion?",
            "en": "What is the difference between a qualified and an adverse opinion?",
            "opts_ru": [
                "Разницы нет, это одно и то же",
                "Qualified — искажения существенны, но не повсеместны. Adverse — существенны И повсеместны",
                "Qualified — мошенничество найдено, Adverse — нет",
                "Qualified для малого бизнеса, Adverse для крупного"
            ],
            "opts_en": [
                "There is no difference, they are the same",
                "Qualified — misstatements are material but not pervasive. Adverse — material AND pervasive",
                "Qualified means fraud found, Adverse means no fraud",
                "Qualified is for small businesses, Adverse for large ones"
            ],
            "correct": 1,
            "explain_ru": "Ключевое слово — pervasive (повсеместный). Qualified: проблема существенна, но ограничена конкретной областью. Adverse: проблема настолько серьёзна и пронизывает всю отчётность, что она в целом недостоверна.",
            "explain_en": "The key word is 'pervasive'. Qualified opinion: misstatement is material but NOT pervasive (limited to one area). Adverse opinion: misstatement is both material AND pervasive — the financial statements as a whole are misleading."
        },
        {
            "ru": "Что такое Emphasis of Matter (акцент на важных вопросах)?",
            "en": "What is an Emphasis of Matter paragraph?",
            "opts_ru": [
                "Часть отрицательного заключения аудитора",
                "Дополнительный абзац в чистом заключении, привлекающий внимание к важному вопросу",
                "Рекомендации по улучшению бизнеса клиента",
                "Требование повторно провести аудит"
            ],
            "opts_en": [
                "Part of an adverse audit opinion",
                "An additional paragraph in an unmodified report drawing attention to an important matter",
                "Business improvement recommendations for the client",
                "A requirement to repeat the audit"
            ],
            "correct": 1,
            "explain_ru": "Emphasis of Matter — абзац, добавляемый к ЧИСТОМУ заключению. Мнение аудитора не меняется, но он привлекает внимание к важному вопросу, уже раскрытому в отчётности. Типичный пример — существенная неопределённость going concern.",
            "explain_en": "An Emphasis of Matter paragraph is added to an UNMODIFIED opinion. The auditor's opinion is not changed, but attention is drawn to a matter already disclosed in the financial statements — e.g. a material uncertainty about going concern."
        },
    ],
}

BLOCK_NAMES = {
    "A": "Блок A · Суть аудита",
    "B": "Блок B · Риски и планирование",
    "C": "Блок C · Внутренний контроль",
    "D": "Блок D · Доказательства ★",
    "E": "Блок E · Заключение аудитора",
    "ALL": "Все блоки вместе",
}


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Все блоки", callback_data="start_ALL")],
        [
            InlineKeyboardButton("A · Суть", callback_data="start_A"),
            InlineKeyboardButton("B · Риски", callback_data="start_B"),
        ],
        [
            InlineKeyboardButton("C · Контроль", callback_data="start_C"),
            InlineKeyboardButton("E · Заключение", callback_data="start_E"),
        ],
        [InlineKeyboardButton("🔬 D · Доказательства (отдельно)", callback_data="start_D")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="stats")],
        [InlineKeyboardButton("📜 История ответов", callback_data="history")],
    ])


def show_question_text(q, num, total):
    letters = ["А", "Б", "В", "Г"]
    opts_text = "\n".join([f"{letters[i]}. {opt}" for i, opt in enumerate(q["opts_ru"])])
    text = (
        f"📝 *Вопрос {num}/{total}*\n"
        f"_{q['en']}_\n\n"
        f"*{q['ru']}*\n\n"
        f"{opts_text}"
    )
    return text


def build_answer_keyboard(question_idx):
    letters = ["А", "Б", "В", "Г"]
    rows = [[
        InlineKeyboardButton(letters[i], callback_data=f"ans_{question_idx}_{i}")
        for i in range(4)
    ]]
    return InlineKeyboardMarkup(rows)


def save_history(context, entry: str):
    history = context.user_data.setdefault("history", [])
    history.append(entry)
    # Храним последние 50 записей
    if len(history) > 50:
        context.user_data["history"] = history[-50:]


def init_session(context, mode):
    if mode == "ALL":
        pool = []
        for block_questions in QUESTIONS.values():
            pool.extend(block_questions)
    else:
        pool = list(QUESTIONS.get(mode, []))
    random.shuffle(pool)
    context.user_data["session"] = {
        "mode": mode,
        "pool": pool,
        "idx": 0,
        "correct": 0,
        "wrong": 0,
        "total": len(pool),
    }


def get_stats(context):
    s = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    return s


def update_stats(context, correct: bool):
    s = context.user_data.setdefault("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    if correct:
        s["correct"] += 1
    else:
        s["wrong"] += 1


# ──────────────────────────────────────────────
#  HANDLERS
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Привет"
    await update.message.reply_text(
        f"👋 {name}!\n\n"
        "Это тренажёр по *ACCA AA* — Audit & Assurance.\n\n"
        "После каждого ответа ты получишь:\n"
        "• объяснение на *русском*\n"
        "• то же самое на *английском* — чтобы привыкать к терминам\n\n"
        "Выбери режим:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── START SESSION ──
    if data.startswith("start_"):
        mode = data.split("_")[1]
        init_session(context, mode)
        s = context.user_data["session"]
        context.user_data["stats"] = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
        context.user_data["stats"]["sessions"] += 1
        await query.edit_message_text(
            f"✅ Режим: *{BLOCK_NAMES[mode]}*\n"
            f"Вопросов: *{s['total']}*\n\n"
            "Поехали! 🚀",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ Начать", callback_data="next")
            ]])
        )
        return

    # ── NEXT QUESTION ──
    if data == "next":
        s = context.user_data.get("session")
        if not s or s["idx"] >= s["total"]:
            await query.edit_message_text(
                "Сессия завершена! Нажми /start чтобы начать заново.",
                reply_markup=get_main_keyboard()
            )
            return
        q = s["pool"][s["idx"]]
        num = s["idx"] + 1
        total = s["total"]
        text = show_question_text(q, num, total)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=build_answer_keyboard(s["idx"])
        )
        return

    # ── ANSWER ──
    if data.startswith("ans_"):
        _, q_idx_str, ans_str = data.split("_")
        q_idx = int(q_idx_str)
        ans = int(ans_str)
        s = context.user_data.get("session")
        if not s or s["idx"] != q_idx:
            return
        q = s["pool"][q_idx]
        correct = q["correct"]
        is_correct = ans == correct
        letters = ["А", "Б", "В", "Г"]

        if is_correct:
            result_line = "✅ *Верно!*"
            s["correct"] += 1
        else:
            result_line = (
                f"❌ *Неверно.*\n"
                f"Правильный ответ: *{letters[correct]}. {q['opts_ru'][correct]}*"
            )
            s["wrong"] += 1

        update_stats(context, is_correct)
        s["idx"] += 1

        # Сохраняем в историю
        history_entry = (
            f"❓ {q['ru']}\n"
            f"{'✅' if is_correct else '❌'} Твой ответ: {letters[ans]}. {q['opts_ru'][ans]}"
            + (f"\n✔️ Правильно: {letters[correct]}. {q['opts_ru'][correct]}" if not is_correct else "")
        )
        save_history(context, history_entry)

        pct = round((s["correct"] / s["idx"]) * 100) if s["idx"] > 0 else 0
        progress = f"Прогресс: {s['correct']}/{s['idx']} ({pct}%)"

        text = (
            f"{result_line}\n\n"
            f"📖 *RU:* {q['explain_ru']}\n\n"
            f"🇬🇧 *EN:* _{q['explain_en']}_\n\n"
            f"─────────────\n{progress}"
        )

        if s["idx"] >= s["total"]:
            # Session finished
            pct_final = round((s["correct"] / s["total"]) * 100)
            emoji = "🏆" if pct_final >= 80 else "📚" if pct_final >= 50 else "💪"
            text += (
                f"\n\n{emoji} *Раунд завершён!*\n"
                f"Результат: *{s['correct']}/{s['total']} ({pct_final}%)*\n\n"
                f"Проходной балл AA: 50% — "
                + ("ты уже там! 🎉" if pct_final >= 50 else "ещё немного!")
            )
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next"),
                    InlineKeyboardButton("🏠 Меню", callback_data="menu")
                ]])
            )
        return

    # ── STATS ──
    if data == "stats":
        s_all = get_stats(context)
        total = s_all["correct"] + s_all["wrong"]
        pct = round((s_all["correct"] / total) * 100) if total > 0 else 0
        text = (
            f"📊 *Твоя статистика*\n\n"
            f"✅ Верно: {s_all['correct']}\n"
            f"❌ Неверно: {s_all['wrong']}\n"
            f"📝 Всего ответов: {total}\n"
            f"🎯 Точность: {pct}%\n"
            f"🔄 Сессий: {s_all['sessions']}\n\n"
            f"Проходной балл на AA — 50%"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── HISTORY ──
    if data == "history":
        history = context.user_data.get("history", [])
        if not history:
            await query.edit_message_text(
                "📜 История пока пуста — начни отвечать на вопросы!",
                reply_markup=get_main_keyboard()
            )
            return
        text = "📜 *Твоя история ответов (последние 10):*\n\n"
        text += "\n\n".join(history[-10:])
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── MENU ──
    if data == "menu":
        await query.edit_message_text(
            "Выбери режим:",
            reply_markup=get_main_keyboard()
        )
        return


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = context.user_data.get("history", [])
    if not history:
        await update.message.reply_text(
            "📜 История пока пуста — начни отвечать на вопросы!",
            reply_markup=get_main_keyboard()
        )
        return
    text = "📜 *Твоя история ответов (последние):*\n\n"
    text += "\n\n".join(history[-10:])
    await update.message.reply_text(text, parse_mode="Markdown")
    text = (
        "⏰ *Напоминание от твоего ACCA AA тренажёра!*\n\n"
        "Прошло 2 недели — пора добавить новые вопросы в бота! 📚\n\n"
        "Что сделать:\n"
        "1. Напиши мне в Claude — я добавлю новые вопросы\n"
        "2. Вставь код в GitHub → бот обновится автоматически\n\n"
        "Не останавливайся — ты молодец! 💪"
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Напоминание каждые 14 дней
    app.job_queue.run_repeating(
        send_reminder,
        interval=timedelta(days=14),
        first=timedelta(days=14),
        name="biweekly_reminder"
    )

    print("Бот запущен ✅")
    app.run_polling()


if __name__ == "__main__":
    main()        },
        {
            "ru": "Главная цель внешнего аудита финансовой отчётности?",
            "en": "What is the primary objective of an external audit?",
            "opts_ru": [
                "Найти все мошенничества в компании",
                "Выразить независимое мнение о достоверности финансовой отчётности",
                "Подготовить отчётность для налоговой",
                "Проверить эффективность работы сотрудников"
            ],
            "opts_en": [
                "To detect all fraud in the company",
                "To express an independent opinion on whether the financial statements give a true and fair view",
                "To prepare financial statements for tax purposes",
                "To assess employee performance"
            ],
            "correct": 1,
            "explain_ru": "Главная цель внешнего аудита — выразить независимое мнение (opinion) о том, отражает ли отчётность достоверно положение дел. Аудитор НЕ гарантирует нахождение всего мошенничества.",
            "explain_en": "The primary objective of an external audit is to express an opinion on whether the financial statements give a true and fair view. The auditor does NOT guarantee detection of all fraud."
        },
        {
            "ru": "Что означает профессиональный скептицизм (professional scepticism)?",
            "en": "What does professional scepticism mean?",
            "opts_ru": [
                "Аудитор не доверяет никому и думает, что клиент всегда врёт",
                "Аудитор критически оценивает доказательства, не принимая их слепо на веру",
                "Аудитор соглашается со всем, что говорит клиент",
                "Аудитор отказывается от задания при любых рисках"
            ],
            "opts_en": [
                "The auditor trusts no one and assumes the client always lies",
                "The auditor critically assesses evidence without blind acceptance",
                "The auditor agrees with everything management says",
                "The auditor refuses any engagement with risks"
            ],
            "correct": 1,
            "explain_ru": "Профессиональный скептицизм — баланс: аудитор не верит всему слепо, но и не подозревает всех автоматически. Он критически проверяет доказательства.",
            "explain_en": "Professional scepticism is an attitude that includes a questioning mind and critical assessment of audit evidence. It is a balance — not blind trust, but not automatic suspicion either."
        },
        {
            "ru": "Почему независимость аудитора важна?",
            "en": "Why is auditor independence important?",
            "opts_ru": [
                "Чтобы аудитор мог брать задания от одного клиента бесконечно",
                "Без независимости мнение аудитора теряет ценность для пользователей",
                "Независимость нужна только для госкомпаний",
                "Чтобы аудитор не платил налоги с гонорара"
            ],
            "opts_en": [
                "So the auditor can work for one client indefinitely",
                "Without independence, the auditor's opinion loses its value to users",
                "Independence is only required for public sector audits",
                "So the auditor pays no tax on fees"
            ],
            "correct": 1,
            "explain_ru": "Независимость бывает двух видов: в мышлении (independence of mind) и внешняя (independence in appearance). Если пользователи думают, что аудитор зависит от клиента — они не будут доверять его заключению.",
            "explain_en": "Independence has two aspects: independence of mind and independence in appearance. If users believe the auditor is not independent, they will not trust the audit opinion — making it worthless."
        },
    ],
    "B": [
        {
            "ru": "Из каких трёх компонентов состоит аудиторский риск?",
            "en": "What are the three components of audit risk?",
            "opts_ru": [
                "Риск мошенничества, риск ошибки, риск банкротства",
                "Неотъемлемый риск, риск контроля, риск необнаружения",
                "Налоговый риск, операционный риск, финансовый риск",
                "Риск клиента, риск аудитора, риск рынка"
            ],
            "opts_en": [
                "Fraud risk, error risk, bankruptcy risk",
                "Inherent risk, control risk, detection risk",
                "Tax risk, operational risk, financial risk",
                "Client risk, auditor risk, market risk"
            ],
            "correct": 1,
            "explain_ru": "Аудиторский риск = Неотъемлемый риск (IR) × Риск контроля (CR) × Риск необнаружения (DR). Первые два аудитор оценивает, третий — контролирует сам через процедуры.",
            "explain_en": "Audit Risk = Inherent Risk × Control Risk × Detection Risk. The auditor assesses IR and CR, then sets DR accordingly by choosing the nature, timing and extent of audit procedures."
        },
        {
            "ru": "Что такое существенность (materiality)?",
            "en": "What is materiality in auditing?",
            "opts_ru": [
                "Сумма всех активов компании",
                "Порог, при превышении которого ошибка влияет на решения пользователей",
                "Минимальная сумма дебиторской задолженности для проверки",
                "Размер аудиторского гонорара"
            ],
            "opts_en": [
                "The total value of company assets",
                "The threshold above which a misstatement could influence users' decisions",
                "The minimum receivable balance subject to testing",
                "The size of the audit fee"
            ],
            "correct": 1,
            "explain_ru": "Существенность (materiality) — пороговое значение. Если ошибка выше этого порога, она может изменить решение пользователя. Аудитор устанавливает уровень существенности сам — обычно % от выручки, прибыли или активов.",
            "explain_en": "Materiality is the threshold above which a misstatement, individually or in aggregate, could influence the economic decisions of users. It is typically set as a percentage of revenue, profit or total assets."
        },
        {
            "ru": "Что описывает высокий неотъемлемый риск (inherent risk)?",
            "en": "Which best describes high inherent risk?",
            "opts_ru": [
                "Компания использует надёжную систему внутреннего контроля",
                "Компания работает в волатильной отрасли со сложными операциями",
                "Аудитор хорошо знает отрасль клиента",
                "Компания давно на рынке со стабильными показателями"
            ],
            "opts_en": [
                "The company has a reliable internal control system",
                "The company operates in a volatile industry with complex transactions",
                "The auditor has strong industry knowledge",
                "The company has been in business for years with stable results"
            ],
            "correct": 1,
            "explain_ru": "Неотъемлемый риск (inherent risk) — риск того, что статья отчётности подвержена ошибкам по своей природе, независимо от контроля. Волатильные активы, субъективные оценки, сложные операции — всё это повышает IR.",
            "explain_en": "Inherent risk is the susceptibility of an assertion to a material misstatement, assuming no related controls. Complex transactions, subjective estimates and volatile industries increase inherent risk."
        },
        {
            "ru": "Что означает принцип непрерывности деятельности (going concern)?",
            "en": "What does the going concern principle mean?",
            "opts_ru": [
                "Компания планирует продать бизнес в течение года",
                "Предположение о том, что компания будет работать минимум 12 месяцев",
                "Компания обязана публиковать отчётность каждый квартал",
                "Аудитор проверяет компанию непрерывно без перерывов"
            ],
            "opts_en": [
                "The company plans to sell its business within one year",
                "The assumption that the entity will continue operating for at least 12 months",
                "The company must publish quarterly reports",
                "The auditor monitors the company on a continuous basis"
            ],
            "correct": 1,
            "explain_ru": "Going concern — базовое допущение: компания будет работать минимум 12 месяцев с даты отчётности. Аудитор обязан оценить угрозы этому принципу. Признаки угрозы: убытки, потеря клиентов, судебные иски.",
            "explain_en": "Going concern is the assumption that the entity will continue in operational existence for at least 12 months from the balance sheet date. The auditor must evaluate whether this assumption is appropriate."
        },
    ],
    "C": [
        {
            "ru": "Главная цель системы внутреннего контроля?",
            "en": "What is the main purpose of internal controls?",
            "opts_ru": [
                "Полностью исключить ошибки и мошенничество",
                "Дать разумную уверенность в достижении целей и надёжности отчётности",
                "Заменить работу внешнего аудитора",
                "Контролировать личные расходы сотрудников"
            ],
            "opts_en": [
                "To completely eliminate errors and fraud",
                "To provide reasonable assurance regarding achievement of objectives",
                "To replace the work of the external auditor",
                "To monitor personal employee expenses"
            ],
            "correct": 1,
            "explain_ru": "Внутренний контроль даёт только разумную уверенность (reasonable assurance), но не абсолютную. Причины: сговор сотрудников (collusion), нарушение правил, обход контроля руководством (management override).",
            "explain_en": "Internal controls provide only reasonable, not absolute, assurance. Limitations include collusion between employees, management override of controls, and human error."
        },
        {
            "ru": "Что такое разделение обязанностей (segregation of duties)?",
            "en": "What is segregation of duties?",
            "opts_ru": [
                "Разделение работы для повышения скорости",
                "Один человек не контролирует всю цепочку операции — снижает риск мошенничества",
                "Распределение задач по сложности между сотрудниками",
                "Система отпусков в бухгалтерии"
            ],
            "opts_en": [
                "Splitting work between departments to increase speed",
                "No single person controls an entire transaction — reduces fraud risk",
                "Allocating tasks by complexity among staff",
                "A leave management system for the finance team"
            ],
            "correct": 1,
            "explain_ru": "Разделение обязанностей (segregation of duties) — ключевой контроль: один человек не должен авторизовывать, выполнять и записывать одну операцию. Пример: тот, кто заказывает товар, не должен его и оплачивать.",
            "explain_en": "Segregation of duties ensures that no single individual controls all stages of a transaction (authorisation, execution, recording). Example: the person ordering goods should not also approve payment."
        },
        {
            "ru": "Что делает аудитор при обнаружении существенного недостатка контроля?",
            "en": "What does the auditor do when a significant control deficiency is found?",
            "opts_ru": [
                "Немедленно прекращает аудит",
                "Сообщает лицам, наделённым полномочиями (комитету по аудиту / руководству)",
                "Самостоятельно исправляет недостаток",
                "Игнорирует, если это не влияет на мнение"
            ],
            "opts_en": [
                "Immediately terminates the audit",
                "Reports it to those charged with governance (audit committee / management)",
                "Fixes the deficiency themselves",
                "Ignores it if it does not affect the opinion"
            ],
            "correct": 1,
            "explain_ru": "При обнаружении недостатков контроля аудитор сообщает тем, кто наделён полномочиями (those charged with governance) — совет директоров или комитет по аудиту. Аудитор НЕ исправляет сам — это угрожало бы независимости.",
            "explain_en": "The auditor must communicate significant deficiencies to those charged with governance (e.g. audit committee or board). The auditor must NOT fix deficiencies — doing so would compromise independence."
        },
    ],
    "D": [
        {
            "ru": "Какие доказательства считаются наиболее надёжными?",
            "en": "Which type of audit evidence is most reliable?",
            "opts_ru": [
                "Устные объяснения менеджмента клиента",
                "Документы от третьих лиц, полученные аудитором напрямую",
                "Внутренние документы, подготовленные бухгалтерией клиента",
                "Личные наблюдения аудитора без документального подтверждения"
            ],
            "opts_en": [
                "Oral explanations from client management",
                "Documents from third parties obtained directly by the auditor",
                "Internal documents prepared by the client's accounting team",
                "Auditor observations without documentary support"
            ],
            "correct": 1,
            "explain_ru": "Доказательства от третьих лиц, полученные напрямую аудитором (external evidence obtained directly) — наиболее надёжные. Пример: банковское подтверждение, пришедшее от банка напрямую. Менее надёжны внутренние документы клиента.",
            "explain_en": "External evidence obtained directly by the auditor is the most reliable. Example: a bank confirmation sent directly to the auditor by the bank. Client-generated internal documents are less reliable."
        },
        {
            "ru": "Что такое процедуры по существу (substantive procedures)?",
            "en": "What are substantive procedures?",
            "opts_ru": [
                "Тесты, проверяющие работу систем внутреннего контроля",
                "Процедуры, направленные на выявление существенных искажений в отчётности",
                "Анализ организационной структуры клиента",
                "Проверка квалификации сотрудников бухгалтерии"
            ],
            "opts_en": [
                "Tests that check whether internal controls are operating effectively",
                "Procedures designed to detect material misstatements in financial statements",
                "Analysis of the client's organisational structure",
                "Assessment of the qualifications of accounting staff"
            ],
            "correct": 1,
            "explain_ru": "Процедуры по существу (substantive procedures) делятся на: аналитические процедуры (analytical procedures) — сравнение цифр, коэффициентов; и детальные тесты (tests of detail) — проверка конкретных документов и остатков.",
            "explain_en": "Substantive procedures consist of: analytical procedures (comparing figures and ratios) and tests of detail (examining specific transactions, balances and disclosures). Both aim to detect material misstatements."
        },
        {
            "ru": "Почему аудиторы проверяют выборку (sample), а не 100% операций?",
            "en": "Why do auditors test a sample rather than 100% of transactions?",
            "opts_ru": [
                "Закон запрещает проверять все документы клиента",
                "Проверка всех операций нецелесообразна по времени и стоимости",
                "Клиент разрешает смотреть не более 50% документов",
                "Аудиторские стандарты требуют проверять ровно 25%"
            ],
            "opts_en": [
                "The law prohibits auditors from examining all client documents",
                "Testing 100% is impractical in terms of time and cost",
                "The client only permits access to 50% of documents",
                "Auditing standards require exactly 25% to be tested"
            ],
            "correct": 1,
            "explain_ru": "Аудиторская выборка (audit sampling) применяется когда проверка 100% нецелесообразна. По выборке аудитор делает выводы обо всей совокупности. Риск выборки (sampling risk) — вывод может не совпасть с реальностью всей совокупности.",
            "explain_en": "Audit sampling is used when it is not practical to test 100% of items. The auditor draws conclusions about the entire population from the sample. Sampling risk is the risk that the conclusion differs from what a 100% test would show."
        },
        {
            "ru": "Что проверяет аудитор при аудите запасов (inventory)?",
            "en": "What does the auditor test when auditing inventory?",
            "opts_ru": [
                "Только цены закупок",
                "Существование, полноту, оценку и права собственности на запасы",
                "Только физическое наличие запасов",
                "Только документы на отгрузку"
            ],
            "opts_en": [
                "Purchase prices only",
                "Existence, completeness, valuation and rights over inventory",
                "Physical presence of inventory only",
                "Delivery documents only"
            ],
            "correct": 1,
            "explain_ru": "При аудите запасов аудитор проверяет: существование (физический подсчёт), полноту (всё ли учтено), оценку (правильность стоимости, NRV), права собственности (принадлежит ли компании). Физическое наблюдение (physical observation) — ключевая процедура.",
            "explain_en": "When auditing inventory, the auditor tests: existence (physical count observation), completeness (all items recorded), valuation (cost vs NRV), and rights (ownership belongs to the entity). Physical observation is the key procedure."
        },
        {
            "ru": "Что такое внешнее подтверждение (external confirmation) и когда оно используется?",
            "en": "What is external confirmation and when is it used?",
            "opts_ru": [
                "Письмо от менеджмента клиента аудитору",
                "Прямой запрос аудитора третьей стороне для подтверждения данных",
                "Внутренняя проверка данных компанией",
                "Запрос в налоговую о задолженности клиента"
            ],
            "opts_en": [
                "A letter from client management to the auditor",
                "A direct request from the auditor to a third party to confirm information",
                "An internal data check by the company",
                "A request to the tax authority about the client's liabilities"
            ],
            "correct": 1,
            "explain_ru": "Внешнее подтверждение (external confirmation) — аудитор напрямую обращается к третьей стороне. Примеры: банковское подтверждение (bank confirmation), подтверждение дебиторской задолженности (debtor circularisation). Это одно из самых надёжных доказательств.",
            "explain_en": "External confirmation is a direct written response from a third party to the auditor. Examples: bank confirmation, debtor circularisation. It is among the most reliable forms of audit evidence because it comes from an independent source."
        },
        {
            "ru": "Как аудитор проверяет выручку (revenue)?",
            "en": "How does the auditor test revenue?",
            "opts_ru": [
                "Только запрашивает объяснения у менеджмента",
                "Аналитические процедуры + детальные тесты на реальность и полноту операций",
                "Только сверяет данные с налоговой декларацией",
                "Только проверяет банковские выписки"
            ],
            "opts_en": [
                "Only asks management for explanations",
                "Analytical procedures + tests of detail for occurrence and completeness",
                "Only reconciles to the tax return",
                "Only reviews bank statements"
            ],
            "correct": 1,
            "explain_ru": "При аудите выручки: аналитические процедуры (сравнение с прошлым годом, расчёт средней цены × объём), тесты на реальность операций (occurrence — подтверждение что продажи были), полноту (completeness — всё ли учтено). Риск завышения выручки всегда высокий.",
            "explain_en": "For revenue: analytical procedures (compare to prior year, price × volume analysis) plus tests of detail for occurrence (sales actually happened) and completeness (all sales recorded). Revenue is high-risk as management may overstate it."
        },
    ],
    "E": [
        {
            "ru": "Когда аудитор выдаёт немодифицированное заключение (unmodified opinion)?",
            "en": "When does the auditor issue an unmodified opinion?",
            "opts_ru": [
                "Когда компания является государственной",
                "Когда финансовая отчётность достоверна во всех существенных аспектах",
                "Когда аудит проводится впервые",
                "Когда клиент платит гонорар вовремя"
            ],
            "opts_en": [
                "When the company is state-owned",
                "When the financial statements give a true and fair view in all material respects",
                "When it is the first audit of the entity",
                "When the client pays the audit fee on time"
            ],
            "correct": 1,
            "explain_ru": "Немодифицированное заключение (unmodified / clean opinion) выдаётся, когда отчётность составлена верно во всех существенных аспектах. Это лучший результат для клиента. Модифицированные: Qualified, Adverse, Disclaimer.",
            "explain_en": "An unmodified (clean) opinion is issued when the financial statements give a true and fair view in all material respects. Modified opinions include: qualified, adverse, and disclaimer of opinion."
        },
        {
            "ru": "Разница между Qualified и Adverse opinion?",
            "en": "What is the difference between a qualified and an adverse opinion?",
            "opts_ru": [
                "Разницы нет, это одно и то же",
                "Qualified — искажения существенны, но не повсеместны. Adverse — существенны И повсеместны",
                "Qualified — мошенничество найдено, Adverse — нет",
                "Qualified для малого бизнеса, Adverse для крупного"
            ],
            "opts_en": [
                "There is no difference, they are the same",
                "Qualified — misstatements are material but not pervasive. Adverse — material AND pervasive",
                "Qualified means fraud found, Adverse means no fraud",
                "Qualified is for small businesses, Adverse for large ones"
            ],
            "correct": 1,
            "explain_ru": "Ключевое слово — pervasive (повсеместный). Qualified: проблема существенна, но ограничена конкретной областью. Adverse: проблема настолько серьёзна и пронизывает всю отчётность, что она в целом недостоверна.",
            "explain_en": "The key word is 'pervasive'. Qualified opinion: misstatement is material but NOT pervasive (limited to one area). Adverse opinion: misstatement is both material AND pervasive — the financial statements as a whole are misleading."
        },
        {
            "ru": "Что такое Emphasis of Matter (акцент на важных вопросах)?",
            "en": "What is an Emphasis of Matter paragraph?",
            "opts_ru": [
                "Часть отрицательного заключения аудитора",
                "Дополнительный абзац в чистом заключении, привлекающий внимание к важному вопросу",
                "Рекомендации по улучшению бизнеса клиента",
                "Требование повторно провести аудит"
            ],
            "opts_en": [
                "Part of an adverse audit opinion",
                "An additional paragraph in an unmodified report drawing attention to an important matter",
                "Business improvement recommendations for the client",
                "A requirement to repeat the audit"
            ],
            "correct": 1,
            "explain_ru": "Emphasis of Matter — абзац, добавляемый к ЧИСТОМУ заключению. Мнение аудитора не меняется, но он привлекает внимание к важному вопросу, уже раскрытому в отчётности. Типичный пример — существенная неопределённость going concern.",
            "explain_en": "An Emphasis of Matter paragraph is added to an UNMODIFIED opinion. The auditor's opinion is not changed, but attention is drawn to a matter already disclosed in the financial statements — e.g. a material uncertainty about going concern."
        },
    ],
}

BLOCK_NAMES = {
    "A": "Блок A · Суть аудита",
    "B": "Блок B · Риски и планирование",
    "C": "Блок C · Внутренний контроль",
    "D": "Блок D · Доказательства ★",
    "E": "Блок E · Заключение аудитора",
    "ALL": "Все блоки вместе",
}


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Все блоки", callback_data="start_ALL")],
        [
            InlineKeyboardButton("A · Суть", callback_data="start_A"),
            InlineKeyboardButton("B · Риски", callback_data="start_B"),
        ],
        [
            InlineKeyboardButton("C · Контроль", callback_data="start_C"),
            InlineKeyboardButton("E · Заключение", callback_data="start_E"),
        ],
        [InlineKeyboardButton("🔬 D · Доказательства (отдельно)", callback_data="start_D")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="stats")],
    ])


def build_question_keyboard(opts_ru, question_idx):
    letters = ["А", "Б", "В", "Г"]
    rows = []
    for i, opt in enumerate(opts_ru):
        rows.append([InlineKeyboardButton(
            f"{letters[i]}. {opt[:40]}{'…' if len(opt)>40 else ''}",
            callback_data=f"ans_{question_idx}_{i}"
        )])
    return InlineKeyboardMarkup(rows)


def init_session(context, mode):
    if mode == "ALL":
        pool = []
        for block_questions in QUESTIONS.values():
            pool.extend(block_questions)
    else:
        pool = list(QUESTIONS.get(mode, []))
    random.shuffle(pool)
    context.user_data["session"] = {
        "mode": mode,
        "pool": pool,
        "idx": 0,
        "correct": 0,
        "wrong": 0,
        "total": len(pool),
    }


def get_stats(context):
    s = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    return s


def update_stats(context, correct: bool):
    s = context.user_data.setdefault("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    if correct:
        s["correct"] += 1
    else:
        s["wrong"] += 1


# ──────────────────────────────────────────────
#  HANDLERS
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Привет"
    await update.message.reply_text(
        f"👋 {name}!\n\n"
        "Это тренажёр по *ACCA AA* — Audit & Assurance.\n\n"
        "После каждого ответа ты получишь:\n"
        "• объяснение на *русском*\n"
        "• то же самое на *английском* — чтобы привыкать к терминам\n\n"
        "Выбери режим:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── START SESSION ──
    if data.startswith("start_"):
        mode = data.split("_")[1]
        init_session(context, mode)
        s = context.user_data["session"]
        context.user_data["stats"] = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
        context.user_data["stats"]["sessions"] += 1
        await query.edit_message_text(
            f"✅ Режим: *{BLOCK_NAMES[mode]}*\n"
            f"Вопросов: *{s['total']}*\n\n"
            "Поехали! 🚀",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ Начать", callback_data="next")
            ]])
        )
        return

    # ── NEXT QUESTION ──
    if data == "next":
        s = context.user_data.get("session")
        if not s or s["idx"] >= s["total"]:
            await query.edit_message_text(
                "Сессия завершена! Нажми /start чтобы начать заново.",
                reply_markup=get_main_keyboard()
            )
            return
        q = s["pool"][s["idx"]]
        num = s["idx"] + 1
        total = s["total"]
        block = q.get("block_label", "")
        text = (
            f"📝 *Вопрос {num}/{total}*\n\n"
            f"{q['ru']}\n\n"
            f"🇬🇧 _{q['en']}_"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=build_question_keyboard(q["opts_ru"], s["idx"])
        )
        return

    # ── ANSWER ──
    if data.startswith("ans_"):
        _, q_idx_str, ans_str = data.split("_")
        q_idx = int(q_idx_str)
        ans = int(ans_str)
        s = context.user_data.get("session")
        if not s or s["idx"] != q_idx:
            return
        q = s["pool"][q_idx]
        correct = q["correct"]
        is_correct = ans == correct
        letters = ["А", "Б", "В", "Г"]

        if is_correct:
            result_line = "✅ *Верно!*"
            s["correct"] += 1
        else:
            result_line = (
                f"❌ *Неверно.*\n"
                f"Правильный ответ: *{letters[correct]}. {q['opts_ru'][correct]}*"
            )
            s["wrong"] += 1

        update_stats(context, is_correct)
        s["idx"] += 1

        pct = round((s["correct"] / s["idx"]) * 100) if s["idx"] > 0 else 0
        progress = f"Прогресс: {s['correct']}/{s['idx']} ({pct}%)"

        text = (
            f"{result_line}\n\n"
            f"📖 *RU:* {q['explain_ru']}\n\n"
            f"🇬🇧 *EN:* _{q['explain_en']}_\n\n"
            f"─────────────\n{progress}"
        )

        if s["idx"] >= s["total"]:
            # Session finished
            pct_final = round((s["correct"] / s["total"]) * 100)
            emoji = "🏆" if pct_final >= 80 else "📚" if pct_final >= 50 else "💪"
            text += (
                f"\n\n{emoji} *Раунд завершён!*\n"
                f"Результат: *{s['correct']}/{s['total']} ({pct_final}%)*\n\n"
                f"Проходной балл AA: 50% — "
                + ("ты уже там! 🎉" if pct_final >= 50 else "ещё немного!")
            )
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next"),
                    InlineKeyboardButton("🏠 Меню", callback_data="menu")
                ]])
            )
        return

    # ── STATS ──
    if data == "stats":
        s_all = get_stats(context)
        total = s_all["correct"] + s_all["wrong"]
        pct = round((s_all["correct"] / total) * 100) if total > 0 else 0
        text = (
            f"📊 *Твоя статистика*\n\n"
            f"✅ Верно: {s_all['correct']}\n"
            f"❌ Неверно: {s_all['wrong']}\n"
            f"📝 Всего ответов: {total}\n"
            f"🎯 Точность: {pct}%\n"
            f"🔄 Сессий: {s_all['sessions']}\n\n"
            f"Проходной балл на AA — 50%"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── MENU ──
    if data == "menu":
        await query.edit_message_text(
            "Выбери режим:",
            reply_markup=get_main_keyboard()
        )
        return


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⏰ *Напоминание от твоего ACCA AA тренажёра!*\n\n"
        "Прошло 2 недели — пора добавить новые вопросы в бота! 📚\n\n"
        "Что сделать:\n"
        "1. Напиши мне в Claude — я добавлю новые вопросы\n"
        "2. Вставь код в GitHub → бот обновится автоматически\n\n"
        "Не останавливайся — ты молодец! 💪"
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Напоминание каждые 14 дней
    app.job_queue.run_repeating(
        send_reminder,
        interval=timedelta(days=14),
        first=timedelta(days=14),
        name="biweekly_reminder"
    )

    print("Бот запущен ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
