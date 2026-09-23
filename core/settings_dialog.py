import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QListWidget, QListWidgetItem,
    QMessageBox, QComboBox, QFileDialog, QInputDialog,
    QFrame, QWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDrag
from .style import DIALOG_STYLE
from .config import (
    list_configs, create_config, delete_config, rename_config,
    load_config, save_students, save_cfg, import_students_from_txt,
    import_students_from_other_config
)


class _GroupNavList(QListWidget):
    def __init__(self, on_move_to_group, parent=None):
        super().__init__(parent)
        self.on_move_to_group = on_move_to_group
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DropOnly)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            item = self.itemAt(event.position().toPoint())
            if item:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        if item and event.mimeData().hasText():
            target_key = item.data(Qt.UserRole)
            if target_key is None:
                super().dropEvent(event)
                return
            data = event.mimeData().text()
            lines = data.split("\n")
            moved = []
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split("\x1f")
                if len(parts) == 2:
                    moved.append((parts[0], parts[1]))
            if moved:
                self.on_move_to_group(moved, target_key)
                event.acceptProposedAction()
                return
        super().dropEvent(event)


class _DraggableStudentList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.MoveAction)

    def startDrag(self, supportedActions):
        items = self.selectedItems()
        if not items:
            return
        mime = QMimeData()
        text_lines = []
        for item in items:
            src = item.source_group if hasattr(item, 'source_group') else ""
            text_lines.append(f"{item.name}\x1f{src}")
        mime.setText("\n".join(text_lines))
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)


class _StudentListItem(QListWidgetItem):
    def __init__(self, name, source_group):
        super().__init__(name)
        self.name = name
        self.source_group = source_group


class EditStudentsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑名单与分组")
        self.setStyleSheet(DIALOG_STYLE)
        self.resize(820, 600)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.config = config
        self.cfg = config["cfg"]
        self._current_group_key = "all"
        self._build_ui()
        self._populate_group_nav()
        self._render_students()

    def _all_student_names(self):
        names = []
        for g in self.cfg.get("groups", []):
            names.extend(g.get("student_names", []))
        names.extend(self.cfg.get("ungrouped", []))
        return names

    def _get_group_students(self, key):
        if key == "all":
            names = []
            for g in self.cfg.get("groups", []):
                names.extend(g.get("student_names", []))
            names.extend(self.cfg.get("ungrouped", []))
            return names
        if key == "ungrouped":
            return list(self.cfg.get("ungrouped", []))
        groups = self.cfg.get("groups", [])
        idx = int(key.replace("group_", ""))
        if 0 <= idx < len(groups):
            return list(groups[idx].get("student_names", []))
        return []

    def _set_group_students(self, key, students):
        if key == "ungrouped":
            self.cfg["ungrouped"] = students
        elif key.startswith("group_"):
            idx = int(key.replace("group_", ""))
            groups = self.cfg.get("groups", [])
            if 0 <= idx < len(groups):
                groups[idx]["student_names"] = students

    def _find_source_group_for(self, name):
        for g_idx, g in enumerate(self.cfg.get("groups", [])):
            if name in g.get("student_names", []):
                return f"group_{g_idx}"
        if name in self.cfg.get("ungrouped", []):
            return "ungrouped"
        return ""

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        title = QLabel("编辑名单与分组")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        body = QHBoxLayout()
        body.setSpacing(10)

        left = QVBoxLayout()
        self.left_title = QLabel("全部学生")
        self.left_title.setStyleSheet("color: #f5c842; font-weight: bold; font-size: 13px;")
        left.addWidget(self.left_title)

        self.student_list = _DraggableStudentList()
        self.student_list.setStyleSheet(
            "QListWidget { background-color: #1a1a2e; border: 1px solid #2a2a4a; border-radius: 10px; color: #eeeeee; padding: 4px; }"
            "QListWidget::item { padding: 6px 10px; border-radius: 6px; margin: 1px 2px; }"
            "QListWidget::item:selected { background-color: #e94560; color: white; }"
        )
        left.addWidget(self.student_list, 1)

        add_row = QHBoxLayout()
        self.add_edit = QLineEdit()
        self.add_edit.setPlaceholderText("输入姓名后回车添加（默认加入无分组）")
        self.add_edit.returnPressed.connect(self._add_student)
        add_row.addWidget(self.add_edit, 1)
        add_btn = QPushButton("添加")
        add_btn.setObjectName("green_btn")
        add_btn.clicked.connect(self._add_student)
        add_row.addWidget(add_btn)
        left.addLayout(add_row)

        btn_row1 = QHBoxLayout()
        rename_btn = QPushButton("重命名")
        rename_btn.setObjectName("ghost_btn")
        rename_btn.clicked.connect(self._rename_student)
        btn_row1.addWidget(rename_btn)

        remove_btn = QPushButton("删除")
        remove_btn.setObjectName("danger_btn")
        remove_btn.clicked.connect(self._remove_student)
        btn_row1.addWidget(remove_btn)
        left.addLayout(btn_row1)

        left_frame = QFrame()
        left_frame.setLayout(left)
        body.addWidget(left_frame, 2)

        right = QVBoxLayout()
        right_title = QLabel("分组（点击切换 / 拖拽学生到此处分组）")
        right_title.setStyleSheet("color: #f5c842; font-weight: bold; font-size: 13px;")
        right_title.setWordWrap(True)
        right.addWidget(right_title)

        self.group_nav = _GroupNavList(self._on_move_to_group)
        self.group_nav.setFixedWidth(180)
        self.group_nav.currentRowChanged.connect(self._on_group_selected)
        self.group_nav.setStyleSheet(
            "QListWidget { background-color: #1a1a2e; border: 1px solid #2a2a4a; border-radius: 10px; color: #eeeeee; padding: 4px; }"
            "QListWidget::item { padding: 8px 12px; border-radius: 6px; margin: 2px; }"
            "QListWidget::item:selected { background-color: #e94560; color: white; }"
            "QListWidget::item:hover:!selected { background-color: rgba(233,69,96,0.2); }"
        )
        right.addWidget(self.group_nav, 1)

        grp_btn_row = QHBoxLayout()
        add_grp_btn = QPushButton("新建组")
        add_grp_btn.setObjectName("green_btn")
        add_grp_btn.clicked.connect(self._add_group)
        grp_btn_row.addWidget(add_grp_btn)

        rename_grp_btn = QPushButton("重命名组")
        rename_grp_btn.setObjectName("ghost_btn")
        rename_grp_btn.clicked.connect(self._rename_group)
        grp_btn_row.addWidget(rename_grp_btn)

        del_grp_btn = QPushButton("删除组")
        del_grp_btn.setObjectName("danger_btn")
        del_grp_btn.clicked.connect(self._delete_group)
        grp_btn_row.addWidget(del_grp_btn)
        right.addLayout(grp_btn_row)

        right_frame = QFrame()
        right_frame.setLayout(right)
        body.addWidget(right_frame, 1)

        layout.addLayout(body, 1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("ghost_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setObjectName("green_btn")
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _populate_group_nav(self):
        self.group_nav.blockSignals(True)
        self.group_nav.clear()

        item_all = QListWidgetItem("全部")
        item_all.setData(Qt.UserRole, "all")
        self.group_nav.addItem(item_all)

        item_ung = QListWidgetItem(f"无分组 ({len(self.cfg.get('ungrouped', []))})")
        item_ung.setData(Qt.UserRole, "ungrouped")
        self.group_nav.addItem(item_ung)

        for g_idx, group in enumerate(self.cfg.get("groups", [])):
            gname = group.get("name", f"第{g_idx+1}组")
            gcount = len(group.get("student_names", []))
            item = QListWidgetItem(f"{gname} ({gcount})")
            item.setData(Qt.UserRole, f"group_{g_idx}")
            self.group_nav.addItem(item)

        self.group_nav.blockSignals(False)
        self.group_nav.setCurrentRow(0)

    def _on_group_selected(self, row):
        if row < 0:
            return
        item = self.group_nav.item(row)
        self._current_group_key = item.data(Qt.UserRole)
        label_map = {
            "all": "全部学生",
            "ungrouped": "无分组学生",
        }
        self.left_title.setText(label_map.get(self._current_group_key, "分组学生"))
        self._render_students()

    def _render_students(self):
        self.student_list.clear()
        students = self._get_group_students(self._current_group_key)
        for name in students:
            src = self._find_source_group_for(name)
            item = _StudentListItem(name, src)
            self.student_list.addItem(item)

    def _on_move_to_group(self, moved_items, target_key):
        for name, src_key in moved_items:
            if src_key and src_key != target_key:
                src_students = self._get_group_students(src_key)
                if name in src_students:
                    src_students.remove(name)
                    self._set_group_students(src_key, src_students)
            if target_key != "all":
                target_students = self._get_group_students(target_key)
                if name not in target_students:
                    target_students.append(name)
                    self._set_group_students(target_key, target_students)
        self._populate_group_nav()
        self._render_students()

    def _add_student(self):
        name = self.add_edit.text().strip()
        if not name:
            return
        all_names = set(self._all_student_names())
        if name in all_names:
            QMessageBox.warning(self, "提示", f"学生 \"{name}\" 已存在")
            return
        self.cfg.setdefault("ungrouped", []).append(name)
        self.add_edit.clear()
        self._populate_group_nav()
        self._render_students()

    def _rename_student(self):
        items = self.student_list.selectedItems()
        if len(items) != 1:
            QMessageBox.information(self, "提示", "请选择一名学生进行重命名")
            return
        item = items[0]
        old_name = item.name
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新名字：", text=old_name)
        if not ok or not new_name.strip() or new_name == old_name:
            return
        new_name = new_name.strip()
        all_names = set(self._all_student_names())
        if new_name in all_names:
            QMessageBox.warning(self, "提示", f"学生 \"{new_name}\" 已存在")
            return
        src_key = self._find_source_group_for(old_name)
        if src_key:
            students = self._get_group_students(src_key)
            students = [new_name if n == old_name else n for n in students]
            self._set_group_students(src_key, students)
        self._populate_group_nav()
        self._render_students()

    def _remove_student(self):
        items = self.student_list.selectedItems()
        if not items:
            return
        names = [item.name for item in items]
        ret = QMessageBox.question(
            self, "确认",
            f"确定删除 {len(names)} 名学生？\n{'、'.join(names)}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        for g in self.cfg.get("groups", []):
            g["student_names"] = [n for n in g.get("student_names", []) if n not in names]
        self.cfg["ungrouped"] = [n for n in self.cfg.get("ungrouped", []) if n not in names]
        self._populate_group_nav()
        self._render_students()

    def _add_group(self):
        name, ok = QInputDialog.getText(self, "新建组", "请输入组名：")
        if ok and name.strip():
            self.cfg.setdefault("groups", []).append({"name": name.strip(), "student_names": []})
            self._populate_group_nav()

    def _rename_group(self):
        row = self.group_nav.currentRow()
        if row < 0:
            return
        item = self.group_nav.item(row)
        key = item.data(Qt.UserRole)
        if not key or key == "all" or key == "ungrouped":
            QMessageBox.information(self, "提示", "请选择一个具体的分组进行重命名")
            return
        idx = int(key.replace("group_", ""))
        groups = self.cfg.get("groups", [])
        if idx < 0 or idx >= len(groups):
            return
        old_name = groups[idx]["name"]
        new_name, ok = QInputDialog.getText(self, "重命名组", "请输入新组名：", text=old_name)
        if ok and new_name.strip():
            groups[idx]["name"] = new_name.strip()
            self._populate_group_nav()

    def _delete_group(self):
        row = self.group_nav.currentRow()
        if row < 0:
            return
        item = self.group_nav.item(row)
        key = item.data(Qt.UserRole)
        if not key or key == "all" or key == "ungrouped":
            QMessageBox.information(self, "提示", "请选择一个具体的分组进行删除")
            return
        idx = int(key.replace("group_", ""))
        groups = self.cfg.get("groups", [])
        if idx < 0 or idx >= len(groups):
            return
        group = groups[idx]
        ret = QMessageBox.question(
            self, "确认",
            f"确定删除组 \"{group['name']}\"？\n组内学生将变为无分组。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self.cfg.setdefault("ungrouped", []).extend(group.get("student_names", []))
        self.cfg["groups"].pop(idx)
        self._populate_group_nav()
        self._render_students()

    def _save(self):
        all_names = self._all_student_names()
        save_students(self.config["name"], all_names)
        save_cfg(self.config["name"], self.cfg)
        self.accept()


class SettingsDialog(QDialog):
    config_changed = Signal(str)

    def __init__(self, current_config_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setStyleSheet(DIALOG_STYLE)
        self.resize(700, 580)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.current_config_name = current_config_name
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        title = QLabel("设置")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.tabs = QTabWidget()
        self._build_config_tab()
        self._build_students_tab()
        layout.addWidget(self.tabs, 1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton("关闭")
        close_btn.setObjectName("ghost_btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _build_config_tab(self):
        tab = QWidget()
        tl = QVBoxLayout(tab)
        tl.setContentsMargins(15, 15, 15, 15)
        tl.setSpacing(10)

        self.config_list = QListWidget()
        self.config_list.currentRowChanged.connect(self._on_config_selected)
        self._refresh_config_list()
        tl.addWidget(self.config_list, 1)

        btn_row = QHBoxLayout()

        new_btn = QPushButton("新建配置")
        new_btn.setObjectName("green_btn")
        new_btn.clicked.connect(self._create_config)
        btn_row.addWidget(new_btn)

        rename_btn = QPushButton("重命名")
        rename_btn.setObjectName("ghost_btn")
        rename_btn.clicked.connect(self._rename_config)
        btn_row.addWidget(rename_btn)

        delete_btn = QPushButton("删除配置")
        delete_btn.setObjectName("danger_btn")
        delete_btn.clicked.connect(self._delete_config)
        btn_row.addWidget(delete_btn)

        btn_row.addStretch()

        switch_btn = QPushButton("切换为此配置")
        switch_btn.setObjectName("gold_btn")
        switch_btn.clicked.connect(self._switch_config)
        btn_row.addWidget(switch_btn)

        tl.addLayout(btn_row)
        self.tabs.addTab(tab, "配置管理")

    def _build_students_tab(self):
        tab = QWidget()
        tl = QVBoxLayout(tab)
        tl.setContentsMargins(15, 15, 15, 15)
        tl.setSpacing(10)

        info = QLabel(f"当前配置：{self.current_config_name}")
        info.setStyleSheet("color: #f5c842; font-weight: bold; font-size: 15px;")
        tl.addWidget(info)

        edit_btn = QPushButton("编辑名单与分组")
        edit_btn.setObjectName("green_btn")
        edit_btn.clicked.connect(self._edit_students)
        tl.addWidget(edit_btn)

        import_txt_btn = QPushButton("从 TXT 文件导入")
        import_txt_btn.setObjectName("blue_btn")
        import_txt_btn.clicked.connect(self._import_from_txt)
        tl.addWidget(import_txt_btn)

        from_cfg_row = QHBoxLayout()
        from_cfg_label = QLabel("从其他配置导入：")
        from_cfg_label.setStyleSheet("color: #eeeeee;")
        from_cfg_row.addWidget(from_cfg_label, 1)

        self.from_cfg_combo = QComboBox()
        self._refresh_from_cfg_combo()
        from_cfg_row.addWidget(self.from_cfg_combo, 1)

        from_cfg_btn = QPushButton("导入")
        from_cfg_btn.setObjectName("ghost_btn")
        from_cfg_btn.clicked.connect(self._import_from_config)
        from_cfg_row.addWidget(from_cfg_btn)

        tl.addLayout(from_cfg_row)

        tip = QLabel(
            "导入说明：\n"
            "  - TXT 文件支持：回车、空格、英文逗号、中文逗号、中文顿号 作为分隔符\n"
            "  - 导入后原有名单将被覆盖，重复名字会自动去重\n"
            "  - 导入后所有学生初始为无分组状态\n"
            "  - 从其他配置导入会同时导入分组信息"
        )
        tip.setStyleSheet("color: #a8a8b3; font-size: 12px; padding: 10px;")
        tip.setWordWrap(True)
        tl.addWidget(tip)
        tl.addStretch()

        self.tabs.addTab(tab, "名单管理")

    def _refresh_config_list(self):
        self.config_list.clear()
        configs = list_configs()
        for name in configs:
            item = QListWidgetItem(name)
            if name == self.current_config_name:
                item.setForeground(Qt.yellow)
            self.config_list.addItem(item)

    def _refresh_from_cfg_combo(self):
        self.from_cfg_combo.clear()
        configs = [c for c in list_configs() if c != self.current_config_name]
        if not configs:
            self.from_cfg_combo.addItem("（没有其他配置）")
            self.from_cfg_combo.setEnabled(False)
        else:
            self.from_cfg_combo.setEnabled(True)
            self.from_cfg_combo.addItems(configs)

    def _on_config_selected(self, row):
        pass

    def _create_config(self):
        name, ok = QInputDialog.getText(self, "新建配置", "请输入配置名称：")
        if ok and name.strip():
            name = name.strip()
            ok2, err = create_config(name)
            if not ok2:
                QMessageBox.warning(self, "错误", err)
                return
            self._refresh_config_list()
            self._refresh_from_cfg_combo()

    def _rename_config(self):
        row = self.config_list.currentRow()
        if row < 0:
            QMessageBox.information(self, "提示", "请先选择一个配置")
            return
        old_name = self.config_list.item(row).text()
        new_name, ok = QInputDialog.getText(self, "重命名配置", "请输入新名称：", text=old_name)
        if ok and new_name.strip():
            new_name = new_name.strip()
            ok2, err = rename_config(old_name, new_name)
            if not ok2:
                QMessageBox.warning(self, "错误", err)
                return
            if old_name == self.current_config_name:
                self.current_config_name = new_name
                self.config_changed.emit(new_name)
            self._refresh_config_list()
            self._refresh_from_cfg_combo()

    def _delete_config(self):
        row = self.config_list.currentRow()
        if row < 0:
            QMessageBox.information(self, "提示", "请先选择一个配置")
            return
        name = self.config_list.item(row).text()
        if name == self.current_config_name:
            QMessageBox.warning(self, "错误", "不能删除当前正在使用的配置")
            return
        ret = QMessageBox.warning(
            self, "确认",
            f"即将删除配置 \"{name}\"！\n此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        ok2, err = delete_config(name)
        if not ok2:
            QMessageBox.warning(self, "错误", err)
            return
        self._refresh_config_list()
        self._refresh_from_cfg_combo()

    def _switch_config(self):
        row = self.config_list.currentRow()
        if row < 0:
            QMessageBox.information(self, "提示", "请先选择一个配置")
            return
        name = self.config_list.item(row).text()
        self.current_config_name = name
        self.config_changed.emit(name)
        self.accept()

    def _edit_students(self):
        config = load_config(self.current_config_name)
        dlg = EditStudentsDialog(config, self)
        if dlg.exec() == QDialog.Accepted:
            self.config_changed.emit(self.current_config_name)

    def _import_from_txt(self):
        ret = QMessageBox.warning(
            self, "确认",
            "即将覆盖原有名单！\n确定继续？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择名单文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            students = import_students_from_txt(self.current_config_name, content)
            QMessageBox.information(self, "成功", f"成功导入 {len(students)} 名学生！（已自动去重）")
            self.config_changed.emit(self.current_config_name)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入失败：{e}")

    def _import_from_config(self):
        if not self.from_cfg_combo.isEnabled():
            QMessageBox.information(self, "提示", "没有其他配置可导入")
            return
        src_name = self.from_cfg_combo.currentText()
        ret = QMessageBox.warning(
            self, "确认",
            f"即将从 \"{src_name}\" 覆盖当前配置的名单！\n确定继续？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        students = import_students_from_other_config(self.current_config_name, src_name)
        QMessageBox.information(self, "成功", f"成功导入 {len(students)} 名学生（含分组）！")
        self.config_changed.emit(self.current_config_name)