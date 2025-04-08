import os
import re
import time
from datetime import datetime
from tqdm import tqdm

def process_db_line(line):
    line = line.replace('\"', '')
    line = re.sub(r'(?:^|,)\s*/ntm-alfacheck-api/alfacheck-cc\#get\s*,?', ',', line)
    line = re.sub(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?)\s*\+\d{4}', r'\1', line)
    line = re.sub(r',([^ ])', r', \1', line)
    line = line.replace('&', ', ')
    line = re.sub(r'eosapp[1-3], ?', '', line)
    return line.strip()

def process_elk_line(line):
    line = line.replace('\"', '')
    date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', line)
    if date_match:
        dt = datetime.strptime(date_match.group(1), '%d.%m.%Y')
        new_date = dt.strftime('%Y-%m-%d')
        line = line.replace(date_match.group(1), new_date)
    line = line.replace("GET method /alfacheck-cc, request = AlfaCheckRequest", "")
    line = re.sub(r'(?:^|,)\s*eosapp[1-3]\s*,?', ',', line)
    line = re.sub(r',+', ',', line)
    line = re.sub(r',([^ ])', r', \1', line)
    line = line.replace('(', '').replace(')', '')
    line = re.sub(r'(?:^|,\s*)[a-zA-Z0-9]+\=null', '', line)
    line = re.sub(r'\s*,\s*', ', ', line)
    return line.strip()

def parse_attributes(line):
    attributes = {}
    for part in line.split(', '):
        if '=' in part:
            key, value = part.split('=', 1)
            attributes[key] = value
    return attributes

def compare_structures(db_attr, elk_attr):
    db_keys = set(db_attr.keys()) - {'time'}
    elk_keys = set(elk_attr.keys()) - {'time'}
    return db_keys == elk_keys and all(db_attr[k] == elk_attr[k] for k in db_keys)

def extract_time(line):
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?)', line)
    if match:
        dt_str = match.group(1)
        try:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
        except:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return None

def alfacheck_cc(service_name: str, inputs: dict) -> dict:
    base_path_general = os.path.dirname(inputs['db_path'])
    output_dir = os.path.join(base_path_general, 'pre_result_data_output')
    safe_service_name = service_name.replace("/", "_").replace("\\", "_")

    with tqdm(total=100, desc="Преобразование данных", unit="step") as pbar:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        db_output_path = os.path.join(output_dir, f"output_DB_{safe_service_name}.txt")
        elk_output_path = os.path.join(output_dir, f"output_ELK_{safe_service_name}.txt")

        # Обработка и фильтрация БД
        with open(inputs['db_path'], 'r') as db_file, open(db_output_path, 'w') as db_out:
            valid_lines = [process_db_line(line) for line in db_file if len(line.strip()) > 110]
            db_out.write('\n'.join(valid_lines) + '\n')
            pbar.update(30)

        # Сортировка БД по времени (по убыванию)
        db_lines = []
        with open(db_output_path, 'r') as f:
            for line in f:
                dt = extract_time(line)
                if dt:
                    db_lines.append((dt, line.strip()))
        db_lines.sort(key=lambda x: x[0], reverse=True)  # Сортировка по убыванию
        with open(db_output_path, 'w') as f:
            f.write('\n'.join([line for _, line in db_lines]) + '\n')
        pbar.update(20)

        # Обработка и фильтрация ELK
        with open(inputs['elk_path'], 'r') as elk_file, open(elk_output_path, 'w') as elk_out:
            valid_lines = [process_elk_line(line) for line in elk_file if len(line.strip()) > 50]
            elk_out.write('\n'.join(valid_lines) + '\n')
            pbar.update(30)

        # Сортировка ELK по времени (по убыванию)
        elk_lines = []
        with open(elk_output_path, 'r') as f:
            for line in f:
                dt = extract_time(line)
                if dt:
                    elk_lines.append((dt, line.strip()))
        elk_lines.sort(key=lambda x: x[0], reverse=True)  # Сортировка по убыванию
        with open(elk_output_path, 'w') as f:
            f.write('\n'.join([line for _, line in elk_lines]) + '\n')
        pbar.update(20)

    result_dir = os.path.join(base_path_general, 'result_data_output')
    os.makedirs(result_dir, exist_ok=True)

    match_path = os.path.join(result_dir, f"match_{safe_service_name}.txt")
    not_match_path = os.path.join(result_dir, f"not_match_{safe_service_name}.txt")

    with open(db_output_path, 'r') as db_file, open(elk_output_path, 'r') as elk_file:
        db_lines = [line.strip() for line in db_file if line.strip()]
        elk_lines = [line.strip() for line in elk_file if line.strip()]

    used_db = set()
    used_elk = set()
    matches = []
    not_matches = []

    with tqdm(total=len(elk_lines), desc="Поиск совпадений", unit="строка") as pbar:
        for j, elk_line in enumerate(elk_lines):
            if j in used_elk:
                pbar.update(1)
                continue

            best_delta = None
            best_db_index = None

            elk_attr = parse_attributes(elk_line)
            elk_time = extract_time(elk_line)

            if not elk_time:
                not_matches.append(f"ELK: {elk_line}\nDB: <время не распознано>")
                used_elk.add(j)
                pbar.update(1)
                continue

            # Поиск наилучшей DB для текущей ELK
            for i in range(len(db_lines)):
                if i in used_db:
                    continue

                db_line = db_lines[i]
                db_attr = parse_attributes(db_line)
                db_time = extract_time(db_line)

                if not db_time:
                    continue

                if compare_structures(db_attr, elk_attr):
                    delta = abs((elk_time - db_time).total_seconds())
                    if delta <= 30:
                        if (best_delta is None) or (delta < best_delta):
                            best_delta = delta
                            best_db_index = i

            if best_db_index is not None:
                db_line = db_lines[best_db_index]
                matches.append(f"ELK: {elk_line}\nDB: {db_line}")
                used_elk.add(j)
                used_db.add(best_db_index)
            else:
                not_matches.append(f"ELK: {elk_line}\nDB: <нет совпадений>")

            pbar.update(1)

    # Обработка оставшихся строк DB
    for i in range(len(db_lines)):
        if i not in used_db:
            not_matches.append(f"ELK: <нет совпадений>\nDB: {db_lines[i]}")

    # Запись результатов
    with open(match_path, 'w') as f:
        f.write('\n\n'.join(matches))

    with open(not_match_path, 'w') as f:
        f.write('\n\n'.join(not_matches))

    print(f"\nРезультаты для {service_name}:")
    print(f"Совпадения: {len(matches)} пар")
    print(f"Не совпали: {len(not_matches)} пар")

    return {
        'status': 'success',
        'message': 'Анализ завершен',
        'data': {
            'matches': len(matches),
            'not_matches': len(not_matches)
        }
    }