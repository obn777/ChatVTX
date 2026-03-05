import re

def solve(expression):
    """
    Анализ биологических последовательностей (ДНК/РНК).
    """
    text = expression.upper()
    
    # Извлекаем последовательность (только буквы A, C, G, T, U)
    sequence_match = re.search(r"[ACGTU]{4,}", text)
    if not sequence_match:
        return None # Возвращаем None, если это не био-запрос
    
    seq = sequence_match.group()
    
    # 1. Определение типа
    is_rna = "U" in seq
    is_dna = "T" in seq
    
    if is_rna and is_dna:
        return "Ошибка: последовательность содержит и T, и U (смесь ДНК и РНК)."

    # 2. Расчет GC-состава
    gc_count = seq.count('G') + seq.count('C')
    gc_content = round((gc_count / len(seq)) * 100, 2)
    
    # 3. Транскрипция
    if not is_rna:
        transcription = seq.replace('T', 'U')
        action = f"Транскрипция (РНК): {transcription}"
    else:
        action = "Это уже последовательность РНК."

    # 4. Обратный комплемент
    if not is_rna:
        pairs = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        complement = "".join([pairs.get(n, n) for n in seq])[::-1]
        action += f"\nОбратный комплемент: {complement}"

    return (f"🧬 [BIO]: {seq} | Длина: {len(seq)} bp | GC: {gc_content}% | {action}")
