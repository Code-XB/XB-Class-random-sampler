import os
import json
import shutil
import re
from datetime import datetime
from .utils import parse_student_text


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FILE_STUDENTS = "students.txt"
FILE_CONFIG = "config.json"
FILE_HISTORY = "history.json"

_DISPLAY_KEY = "__display_name__"


def _safe_dir_name(name):
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|\s]+', "_", name)
    name = name.strip("_")
    if not name:
        name = "config"
    return name


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _scan():
    result = []
    for folder in os.listdir(DATA_DIR):
        full = os.path.join(DATA_DIR, folder)
        if not os.path.isdir(full):
            continue
        cfg_path = os.path.join(full, FILE_CONFIG)
        if not os.path.exists(cfg_path):
            continue
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
        display = cfg.get(_DISPLAY_KEY, folder)
        result.append({"folder": folder, "display": display})
    result.sort(key=lambda x: x["display"])
    return result


def list_configs():
    return [item["display"] for item in _scan()]


def _display_to_folder(display_name):
    for item in _scan():
        if item["display"] == display_name:
            return item["folder"]
    return None


def create_config(name):
    ensure_data_dir()
    folder = _safe_dir_name(name)
    path = os.path.join(DATA_DIR, folder)
    if os.path.exists(path):
        existing_display = None
        cfg_path = os.path.join(path, FILE_CONFIG)
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    existing_display = json.load(f).get(_DISPLAY_KEY)
            except Exception:
                pass
        if existing_display == name:
            return False, "配置已存在"
        base = folder
        i = 1
        while os.path.exists(os.path.join(DATA_DIR, f"{base}_{i}")):
            i += 1
        folder = f"{base}_{i}"
        path = os.path.join(DATA_DIR, folder)
    os.makedirs(path, exist_ok=True)
    _write(os.path.join(path, FILE_STUDENTS), "")
    cfg = _default_config()
    cfg[_DISPLAY_KEY] = name
    _write_json(os.path.join(path, FILE_CONFIG), cfg)
    _write_json(os.path.join(path, FILE_HISTORY), [])
    return True, ""


def delete_config(name):
    folder = _display_to_folder(name)
    if not folder:
        return False, "配置不存在"
    path = os.path.join(DATA_DIR, folder)
    if not os.path.exists(path):
        return False, "配置不存在"
    shutil.rmtree(path)
    return True, ""


def rename_config(old_name, new_name):
    folder = _display_to_folder(old_name)
    if not folder:
        return False, "配置不存在"
    path = os.path.join(DATA_DIR, folder)
    cfg_path = os.path.join(path, FILE_CONFIG)
    cfg = _read_json(cfg_path, _default_config())
    for item in _scan():
        if item["display"] == new_name and item["folder"] != folder:
            return False, "目标名称已存在"
    cfg[_DISPLAY_KEY] = new_name
    _write_json(cfg_path, cfg)
    return True, ""


def config_exists(name):
    return _display_to_folder(name) is not None


def _default_config():
    return {
        "groups": [],
        "ungrouped": [],
        "extract_count": 1,
        "dedup": True,
        "extracted_this_round": [],
        "selected_students": "all"
    }


def _write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _read(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def load_config(name):
    folder = _display_to_folder(name)
    if not folder:
        return None
    path = os.path.join(DATA_DIR, folder)
    if not os.path.exists(path):
        return None
    cfg_path = os.path.join(path, FILE_CONFIG)
    cfg_data = _read_json(cfg_path, None)
    display = name
    if cfg_data and _DISPLAY_KEY in cfg_data:
        display = cfg_data[_DISPLAY_KEY]
    config = {
        "name": display,
        "_folder": folder,
        "_path": path,
        "students_path": os.path.join(path, FILE_STUDENTS),
        "config_path": cfg_path,
        "history_path": os.path.join(path, FILE_HISTORY),
        "students": [],
        "cfg": _default_config(),
        "history": []
    }
    config["students"] = [s for s in _read(config["students_path"]).splitlines() if s.strip()]
    if cfg_data:
        config["cfg"].update(cfg_data)
    config["history"] = _read_json(config["history_path"], [])
    return config


def save_students(name, students):
    folder = _display_to_folder(name)
    if not folder:
        return
    _write(os.path.join(DATA_DIR, folder, FILE_STUDENTS), "\n".join(students))


def save_cfg(name, cfg):
    folder = _display_to_folder(name)
    if not folder:
        return
    _write_json(os.path.join(DATA_DIR, folder, FILE_CONFIG), cfg)


def save_history(name, history):
    folder = _display_to_folder(name)
    if not folder:
        return
    _write_json(os.path.join(DATA_DIR, folder, FILE_HISTORY), history)


def append_history(name, names):
    folder = _display_to_folder(name)
    if not folder:
        return []
    path = os.path.join(DATA_DIR, folder, FILE_HISTORY)
    history = _read_json(path, [])
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    if history and history[-1].get("date") == today:
        history[-1]["records"].append({
            "time": now_time,
            "names": list(names)
        })
    else:
        history.append({
            "date": today,
            "records": [{"time": now_time, "names": list(names)}]
        })
    _write_json(path, history)
    return history


def get_all_students_from_config(config):
    cfg = config["cfg"]
    all_names = []
    for g in cfg.get("groups", []):
        all_names.extend(g.get("student_names", []))
    all_names.extend(cfg.get("ungrouped", []))
    return all_names


def reset_round_extracted(config):
    cfg = config["cfg"]
    cfg["extracted_this_round"] = []
    save_cfg(config["name"], cfg)


def import_students_from_txt(name, txt_content):
    students = parse_student_text(txt_content)
    save_students(name, students)
    cfg = load_config(name)["cfg"]
    cfg["groups"] = []
    cfg["ungrouped"] = list(students)
    save_cfg(name, cfg)
    return students


def import_students_from_other_config(target_name, source_name):
    src = load_config(source_name)
    if not src:
        return []
    src_names = get_all_students_from_config(src)
    seen = set()
    deduped_students = []
    for s in src_names:
        if s not in seen:
            seen.add(s)
            deduped_students.append(s)
    save_students(target_name, deduped_students)
    cfg = load_config(target_name)["cfg"]
    cfg["groups"] = src["cfg"].get("groups", [])
    cfg["ungrouped"] = src["cfg"].get("ungrouped", [])
    save_cfg(target_name, cfg)
    return deduped_students


def ensure_default_config():
    ensure_data_dir()
    configs = list_configs()
    if not configs:
        create_config("默认配置")
        return "默认配置"
    return configs[0]


def migrate_legacy():
    ensure_data_dir()
    for folder in os.listdir(DATA_DIR):
        full = os.path.join(DATA_DIR, folder)
        if not os.path.isdir(full):
            continue
        old_students = os.path.join(full, "名单.txt")
        old_cfg = os.path.join(full, "配置.json")
        old_hist = os.path.join(full, "历史记录.json")
        new_students = os.path.join(full, FILE_STUDENTS)
        new_cfg = os.path.join(full, FILE_CONFIG)
        new_hist = os.path.join(full, FILE_HISTORY)

        has_legacy = os.path.exists(old_students) or os.path.exists(old_cfg) or os.path.exists(old_hist)
        has_new = os.path.exists(new_students) or os.path.exists(new_cfg) or os.path.exists(new_hist)
        if not has_legacy or has_new:
            continue

        if os.path.exists(old_students) and not os.path.exists(new_students):
            shutil.move(old_students, new_students)
        if os.path.exists(old_cfg) and not os.path.exists(new_cfg):
            shutil.move(old_cfg, new_cfg)
        if os.path.exists(old_hist) and not os.path.exists(new_hist):
            shutil.move(old_hist, new_hist)

        display_name = folder
        try:
            with open(new_cfg, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if not cfg.get(_DISPLAY_KEY):
                cfg[_DISPLAY_KEY] = display_name
                with open(new_cfg, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass