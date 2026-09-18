# -*- coding: utf-8 -*-
"""Подсчёт результатов прогона чек-листа веб-приложения «Тест-лаборатория».

Читает CSV-файл с результатами проверок и выводит сводку по модулям:
сколько проверок пройдено, сколько провалено и какова доля успешных.
"""
import csv
import sys
from collections import Counter, defaultdict

PASSED = 'passed'
FAILED = 'failed'
SKIPPED = 'skipped'


def read_results(path):
    """Читает результаты прогона: id, module, title, status."""
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def summarize(rows):
    """Считает статистику по каждому модулю."""
    stats = defaultdict(Counter)
    for row in rows:
        stats[row['module']][row['status']] += 1
    return stats


def pass_rate(counter):
    """Доля успешных проверок без учёта пропущенных, %."""
    executed = counter[PASSED] + counter[FAILED]
    if executed == 0:
        return None
    return round(counter[PASSED] / executed * 100, 1)


def fmt_rate(value):
    """Проценты для печати; прочерк, если не выполнено ни одной проверки."""
    return '-' if value is None else f'{value}'


def main(path):
    rows = read_results(path)
    if not rows:
        print('Файл с результатами пуст')
        return 1

    stats = summarize(rows)
    total = Counter()
    print(f'{"Модуль":<24}{"Всего":>7}{"Пройдено":>10}{"Провалено":>11}{"Успех, %":>10}')
    for module in sorted(stats):
        c = stats[module]
        total.update(c)
        print(f'{module:<24}{sum(c.values()):>7}{c[PASSED]:>10}'
              f'{c[FAILED]:>11}{fmt_rate(pass_rate(c)):>10}')

    print('-' * 62)
    print(f'{"Итого":<24}{sum(total.values()):>7}{total[PASSED]:>10}'
          f'{total[FAILED]:>11}{fmt_rate(pass_rate(total)):>10}')

    if total[SKIPPED]:
        print(f'\nНе выполнено проверок: {total[SKIPPED]}')
    if total[FAILED]:
        print(f'\nПрогон не пройден: провалено проверок - {total[FAILED]}')
        return 1
    print('\nПрогон пройден полностью')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Использование: python checklist_report.py results.csv')
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
