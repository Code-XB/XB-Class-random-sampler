from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QCheckBox,
    QGridLayout, QMessageBox, QInputDialog, QFrame
)
from PySide6.QtCore import Qt
from .style import DIALOG_STYLE
from .utils import match_student, get_random_color
from .config import save_cfg, save_students


class StudentDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择学生")
        self.setStyleSheet(DIALOG_STYLE)
        self.resize(780, 680)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.config = config
        self.cfg = config["cfg"]
        self.current_group_key = None
        self._student_widgets = {}
        self._group_map = {}
        self._current_group_cbs = []

        self._build_ui()
        self._load_selection()
        self._populate_groups_list()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        title = QLabel("选择学生")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        header_row = QHBoxLayout()
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("输入汉字或拼音首字母筛选...")
        self.filter_edit.textChanged.connect(self._apply_filter)
        header_row.addWidget(self.filter_edit, 1)

        self.selected_info = QLabel("已选择: 0 / 0 人")
        self.selected_info.setObjectName("selected_info")
        header_row.addWidget(self.selected_info)
        layout.addLayout(header_row)

        body = QHBoxLayout()
        body.setSpacing(12)

        left_frame = QFrame()
        left_frame.setStyleSheet(
            "QFrame { background-color: #16213e; border: 1px solid #2a2a4a; border-radius: 12px; }"
        )
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(3)

        self.group_list = QListWidget()
        self.group_list.setFixedWidth(160)
        self.group_list.currentRowChanged.connect(self._on_group_selected)
        self.group_list.setStyleSheet(
            "QListWidget { background: transparent; border: none; outline: none; }"
            "QListWidget::item { padding: 8px 12px; border-radius: 8px; margin: 2px 4px; color: #eeeeee; }"
            "QListWidget::item:selected { background-color: #e94560; color: white; }"
            "QListWidget::item:hover:!selected { background-color: rgba(233,69,96,0.2); }"
        )
        left_layout.addWidget(self.group_list)

        body.addWidget(left_frame)

        right_frame = QFrame()
        right_frame.setStyleSheet(
            "QFrame { background-color: #16213e; border: 1px solid #2a2a4a; border-radius: 12px; }"
        )
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(15, 10, 15, 10)
        right_layout.setSpacing(8)

        self.group_header = QLabel("")
        self.group_header.setObjectName("group_label")
        self.group_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #f5c842; padding: 5px;")
        right_layout.addWidget(self.group_header)

        self.group_select_cb = QCheckBox("全选该组")
        self.group_select_cb.setStyleSheet(
            "QCheckBox { color: #eeeeee; font-size: 13px; }"
            "QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px; border: 2px solid #2a2a4a; background-color: #1a1a2e; }"
            "QCheckBox::indicator:checked { background-color: #e94560; border-color: #e94560; }"
        )
        self.group_select_cb.stateChanged.connect(self._on_current_group_toggle)
        right_layout.addWidget(self.group_select_cb)

        self.student_area = QFrame()
        self.student_area_layout = QGridLayout(self.student_area)
        self.student_area_layout.setContentsMargins(5, 5, 5, 5)
        self.student_area_layout.setHorizontalSpacing(20)
        self.student_area_layout.setVerticalSpacing(8)
        right_layout.addWidget(self.student_area, 1)

        body.addWidget(right_frame, 1)

        layout.addLayout(body, 1)

        ctrl_row = QHBoxLayout()
        add_stu_btn = QPushButton("添加学生")
        add_stu_btn.setObjectName("green_btn")
        add_stu_btn.clicked.connect(self._add_student)
        ctrl_row.addWidget(add_stu_btn)

        rename_stu_btn = QPushButton("重命名学生")
        rename_stu_btn.setObjectName("ghost_btn")
        rename_stu_btn.clicked.connect(self._rename_student)
        ctrl_row.addWidget(rename_stu_btn)

        del_stu_btn = QPushButton("删除学生")
        del_stu_btn.setObjectName("danger_btn")
        del_stu_btn.clicked.connect(self._delete_student)
        ctrl_row.addWidget(del_stu_btn)

        ctrl_row.addStretch()

        select_all_btn = QPushButton("全选")
        select_all_btn.setObjectName("ghost_btn")
        select_all_btn.clicked.connect(self._select_all)
        ctrl_row.addWidget(select_all_btn)

        select_none_btn = QPushButton("全不选")
        select_none_btn.setObjectName("ghost_btn")
        select_none_btn.clicked.connect(self._select_none)
        ctrl_row.addWidget(select_none_btn)

        invert_btn = QPushButton("反选")
        invert_btn.setObjectName("ghost_btn")
        invert_btn.clicked.connect(self._invert_selection)
        ctrl_row.addWidget(invert_btn)

        layout.addLayout(ctrl_row)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("ghost_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        confirm_btn = QPushButton("确定")
        confirm_btn.setObjectName("green_btn")
        confirm_btn.clicked.connect(self._on_confirm)
        btn_row.addWidget(confirm_btn)
        layout.addLayout(btn_row)

    def _populate_groups_list(self):
        self.group_list.clear()
        self._group_map.clear()

        groups = self.cfg.get("groups", [])
        for g_idx, group in enumerate(groups):
            group_name = group.get("name", f"第{g_idx+1}组")
            key = f"group_{g_idx}"
            item = QListWidgetItem(f"{group_name} ({len(group.get('student_names', []))})")
            item.setData(Qt.UserRole, key)
            self._group_map[key] = group_name
            self.group_list.addItem(item)

        ungrouped = self.cfg.get("ungrouped", [])
        if ungrouped:
            key = "ungrouped"
            item = QListWidgetItem(f"无分组 ({len(ungrouped)})")
            item.setData(Qt.UserRole, key)
            self._group_map[key] = "无分组"
            self.group_list.addItem(item)

        if self.group_list.count() > 0:
            self.group_list.setCurrentRow(0)

    def _get_group_students(self, key):
        if key == "ungrouped":
            return self.cfg.get("ungrouped", [])
        groups = self.cfg.get("groups", [])
        idx = int(key.replace("group_", ""))
        if 0 <= idx < len(groups):
            return groups[idx].get("student_names", [])
        return []

    def _set_group_students(self, key, students):
        if key == "ungrouped":
            self.cfg["ungrouped"] = students
        else:
            groups = self.cfg.get("groups", [])
            idx = int(key.replace("group_", ""))
            if 0 <= idx < len(groups):
                groups[idx]["student_names"] = students

    def _on_group_selected(self, row):
        if row < 0:
            return
        item = self.group_list.item(row)
        key = item.data(Qt.UserRole)
        self.current_group_key = key
        self.group_header.setText(self._group_map.get(key, ""))
        self._render_students_in_group()

    def _render_students_in_group(self):
        while self.student_area_layout.count():
            item = self.student_area_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self._current_group_cbs = []
        if self.current_group_key is None:
            self.group_select_cb.blockSignals(True)
            self.group_select_cb.setChecked(False)
            self.group_select_cb.setEnabled(False)
            self.group_select_cb.blockSignals(False)
            return

        students = self._get_group_students(self.current_group_key)
        max_cols = 4
        all_checked = True

        for i, name in enumerate(students):
            cb = QCheckBox(name)
            cb.setStyleSheet(
                "QCheckBox { font-size: 13px; color: #eeeeee; padding: 3px; }"
                "QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px; border: 2px solid #2a2a4a; background-color: #1a1a2e; }"
                "QCheckBox::indicator:checked { background-color: #e94560; border-color: #e94560; }"
            )
            cb.stateChanged.connect(self._on_current_group_toggle_state)
            cb.blockSignals(True)
            cb.setChecked(self._is_student_selected(name))
            cb.blockSignals(False)
            self._current_group_cbs.append((cb, name))
            self.student_area_layout.addWidget(cb, i // max_cols, i % max_cols)
            if not cb.isChecked():
                all_checked = False

        self.group_select_cb.blockSignals(True)
        if not students:
            self.group_select_cb.setCheckState(Qt.Unchecked)
            self.group_select_cb.setEnabled(False)
        elif all_checked:
            self.group_select_cb.setCheckState(Qt.Checked)
            self.group_select_cb.setEnabled(True)
        else:
            self.group_select_cb.setCheckState(Qt.Unchecked)
            self.group_select_cb.setEnabled(True)
        self.group_select_cb.blockSignals(False)

        self._apply_filter(self.filter_edit.text())

    def _is_student_selected(self, name):
        selected = self.cfg.get("selected_students", "all")
        if selected == "all":
            return True
        if isinstance(selected, list):
            return name in selected
        return False

    def _collect_all_student_names(self):
        names = []
        for g in self.cfg.get("groups", []):
            names.extend(g.get("student_names", []))
        names.extend(self.cfg.get("ungrouped", []))
        return names

    def _on_current_group_toggle(self, state):
        checked = state == Qt.Checked
        for cb, name in self._current_group_cbs:
            cb.blockSignals(True)
            cb.setChecked(checked)
            cb.blockSignals(False)
            self._set_student_selected(name, checked)
        self._update_selected_count()

    def _on_current_group_toggle_state(self, state):
        all_checked = all(cb.isChecked() for cb, _ in self._current_group_cbs)
        some_checked = any(cb.isChecked() for cb, _ in self._current_group_cbs)
        self.group_select_cb.blockSignals(True)
        if all_checked:
            self.group_select_cb.setCheckState(Qt.Checked)
        elif some_checked:
            self.group_select_cb.setCheckState(Qt.PartiallyChecked)
        else:
            self.group_select_cb.setCheckState(Qt.Unchecked)
        self.group_select_cb.blockSignals(False)
        self._update_selected_count()

    def _set_student_selected(self, name, checked):
        selected = self.cfg.get("selected_students", "all")
        if checked:
            if selected == "all":
                return
            if name not in selected:
                selected.append(name)
            self.cfg["selected_students"] = selected
        else:
            if selected == "all":
                selected = [n for n in self._collect_all_student_names() if n != name]
                self.cfg["selected_students"] = selected
            elif name in selected:
                selected.remove(name)

    def _update_selected_count(self):
        all_names = self._collect_all_student_names()
        selected = self.cfg.get("selected_students", "all")
        if selected == "all":
            count = len(all_names)
        else:
            count = len([n for n in selected if n in all_names])
        self.selected_info.setText(f"已选择: {count} / {len(all_names)} 人")

    def _select_all(self):
        self.cfg["selected_students"] = "all"
        self._render_students_in_group()
        self._update_selected_count()

    def _select_none(self):
        all_names = self._collect_all_student_names()
        self.cfg["selected_students"] = []
        self._render_students_in_group()
        self._update_selected_count()

    def _invert_selection(self):
        all_names = self._collect_all_student_names()
        current = self.cfg.get("selected_students", "all")
        if current == "all":
            self.cfg["selected_students"] = []
        elif isinstance(current, list):
            self.cfg["selected_students"] = [n for n in all_names if n not in current]
        self._render_students_in_group()
        self._update_selected_count()

    def _apply_filter(self, text):
        keyword = text.strip()
        for cb, name in self._current_group_cbs:
            cb.setVisible(match_student(name, keyword))

    def _load_selection(self):
        pass

    def _collect_all_current_selections(self):
        return self.cfg.get("selected_students", "all")

    def _add_student(self):
        if self.current_group_key is None:
            QMessageBox.information(self, "提示", "请先选择一个分组")
            return
        name, ok = QInputDialog.getText(self, "添加学生", "请输入学生姓名：")
        if not ok or not name.strip():
            return
        name = name.strip()
        all_names = set(self._collect_all_student_names())
        if name in all_names:
            QMessageBox.warning(self, "提示", f"学生 \"{name}\" 已存在")
            return
        students = list(self._get_group_students(self.current_group_key))
        students.append(name)
        self._set_group_students(self.current_group_key, students)
        save_students(self.config["name"], self._collect_all_student_names())
        save_cfg(self.config["name"], self.cfg)
        self._populate_groups_list()
        items = self.group_list.findItems(
            self._group_map.get(self.current_group_key, ""), Qt.MatchExactly
        )
        if items:
            self.group_list.setCurrentRow(self.group_list.row(items[0]))
        self._update_selected_count()

    def _rename_student(self):
        selected = [cb for cb, _ in self._current_group_cbs if cb.isChecked()]
        if len(selected) != 1:
            QMessageBox.information(self, "提示", "请勾选且仅勾选一名学生进行重命名")
            return
        old_name = selected[0].text()
        new_name, ok = QInputDialog.getText(self, "重命名学生", "请输入新名字：", text=old_name)
        if not ok or not new_name.strip() or new_name == old_name:
            return
        new_name = new_name.strip()
        all_names = set(self._collect_all_student_names())
        if new_name in all_names:
            QMessageBox.warning(self, "提示", f"学生 \"{new_name}\" 已存在")
            return
        students = [new_name if n == old_name else n for n in self._get_group_students(self.current_group_key)]
        self._set_group_students(self.current_group_key, students)

        cur = self.cfg.get("selected_students", "all")
        if cur == "all":
            pass
        elif old_name in cur:
            idx = cur.index(old_name)
            cur[idx] = new_name
        save_students(self.config["name"], self._collect_all_student_names())
        save_cfg(self.config["name"], self.cfg)
        self._populate_groups_list()
        self._render_students_in_group()
        self._update_selected_count()

    def _delete_student(self):
        to_delete = [name for cb, name in self._current_group_cbs if cb.isChecked()]
        if not to_delete:
            QMessageBox.information(self, "提示", "请先勾选要删除的学生")
            return
        ret = QMessageBox.warning(
            self, "确认",
            f"确定删除以下 {len(to_delete)} 名学生？\n{'、'.join(to_delete)}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        students = [n for n in self._get_group_students(self.current_group_key) if n not in to_delete]
        self._set_group_students(self.current_group_key, students)

        cur = self.cfg.get("selected_students", "all")
        if isinstance(cur, list):
            for n in to_delete:
                if n in cur:
                    cur.remove(n)
        save_students(self.config["name"], self._collect_all_student_names())
        save_cfg(self.config["name"], self.cfg)
        self._populate_groups_list()
        self._render_students_in_group()
        self._update_selected_count()

    def _on_confirm(self):
        selected = self.cfg.get("selected_students", "all")
        all_names = self._collect_all_student_names()

        if selected == "all":
            pass
        elif not selected:
            ret = QMessageBox.question(
                self, "确认",
                "没有选择任何同学，将视为全班抽取。\n是否继续？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            if ret != QMessageBox.Yes:
                return
            self.cfg["selected_students"] = "all"
        else:
            if len(selected) == len(all_names):
                self.cfg["selected_students"] = "all"

        save_cfg(self.config["name"], self.cfg)
        self.accept()