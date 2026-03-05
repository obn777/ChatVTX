import re

class BioAnalyzer:
    """
    Модуль анализа био-цепочек с функцией синтеза белка.
    Интегрирован в LogicProcessor для экспресс-анализа ДНК/РНК.
    """
    def __init__(self):
        # Паттерн ищет цепочки нуклеотидов от 4 символов и выше
        self.pattern = re.compile(r"[ACGTU]{4,}")
        
        # Полная таблица генетического кода (РНК -> Аминокислота)
        self.codon_table = {
            'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
            'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
            'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
            'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
            'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
            'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
            'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
            'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
            'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
            'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_', 'UGA':'_',
            'UGC':'C', 'UGU':'C', 'UGG':'W',
        }

    def translate(self, rna_seq: str) -> str:
        """Трансляция РНК в последовательность аминокислот."""
        protein = ""
        # Итерируемся по триплетам, отсекая лишний хвост
        for i in range(0, len(rna_seq) - (len(rna_seq) % 3), 3):
            codon = rna_seq[i:i+3]
            protein += self.codon_table.get(codon, "?")
        return protein

    def analyze(self, text: str):
        """Основной метод анализа входного текста."""
        text = text.upper()
        match = self.pattern.search(text)
        if not match: 
            return None
        
        seq = match.group()
        length = len(seq)
        has_t, has_u = 'T' in seq, 'U' in seq
        
        # Валидация: ДНК не может содержать Урацил, а РНК — Тимин одновременно
        if has_t and has_u: 
            return "ОШИБКА БИО-АНАЛИЗА: Обнаружена некорректная смесь Тимина и Урацила."
        
        is_rna = has_u
        # Для трансляции всегда используем РНК-вид (T заменяем на U)
        rna_for_translation = seq if is_rna else seq.replace('T', 'U')
        protein = self.translate(rna_for_translation)
        
        # Расчет GC-состава (показатель стабильности цепи)
        gc_content = round(((seq.count('G') + seq.count('C')) / length) * 100, 1)
        
        # Формируем отчет
        seq_type = "РНК" if is_rna else "ДНК"
        result = (
            f"🧬 БИО-ОТЧЕТ: Обнаружена цепочка {seq_type}. "
            f"Длина {length} пар нуклеотидов. "
            f"Гэ Цэ состав {gc_content} процентов. "
            f"Синтезированный белок: {protein}"
        )
        return result

# Инициализация для экспорта
bio_tool = BioAnalyzer()
