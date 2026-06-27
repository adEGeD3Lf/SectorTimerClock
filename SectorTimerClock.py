import sys
import math
import json
import os
import re
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QColorDialog, QFontDialog,
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
                             QPushButton, QCheckBox, QGroupBox, QScrollArea, QFrame,
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox,
                             QSpinBox, QDoubleSpinBox, QSizePolicy)
from PySide6.QtCore import QTimer, Qt, QPoint, QRectF
from PySide6.QtGui import QPainter, QColor, QPolygon, QFont, QPen

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# ============================================================
# 多言語辞書
# ============================================================
LANG = {
    "ja": {
        # タイマー設定ダイアログ
        "timer_dialog_title": "タイマー設定",
        "timer_duration_label": "残り時間で設定 (例: 1:30:00→1時間30分 / 45:00→45分 / 10→10分)",
        "timer_time_label": "時刻で設定 (終了時刻を指定)",
        "btn_remember": "記憶",
        "btn_delete": "削除",
        "btn_add_fav": "お気に入りに追加",
        "btn_start": "開始",
        "fav_label": "お気に入り管理（お気に入りに登録すると時計の右クリックメニューからタイマーを開始できます）",
        "btn_up": "↑ 上へ",
        "btn_down": "↓ 下へ",
        "btn_del_fav": "削除",
        "btn_cancel": "キャンセル",
        "fav_prefix_duration": "残り",
        "fav_prefix_time": "時刻",
        # 設定ダイアログ
        "settings_dialog_title": "詳細設定",
        "group_general": "全体設定",
        "cb_always_on_top": "常に最前面",
        "cb_smooth_second": "秒針をスムーズにする",
        "cb_save_window_pos": "ウィンドウ位置を記憶する",
        "slider_opacity": "透明度(%)",
        "slider_diameter": "直径(px)",
        "group_dial": "文字盤の設定",
        "lbl_numbers": "【数字】",
        "btn_color": "色",
        "btn_font": "フォント",
        "slider_num_radius": "距離(px)",
        "lbl_mark5": "【５分目盛り】",
        "lbl_mark1": "【１分目盛り】",
        "slider_mark_width": "太さ(px)",
        "slider_mark_len": "長さ(%)",
        "lbl_date": "【日付】",
        "cb_date_show": "表示する",
        "slider_date_opacity": "透明度(%)",
        "slider_date_radius": "距離(上下)(px)",
        "lbl_date_format": "形式:",
        "group_hands": "針の設定",
        "lbl_hour_hand": "【短針】",
        "lbl_minute_hand": "【長針】",
        "lbl_second_hand": "【秒針】",
        "slider_hand_len": "長さ(%)",
        "slider_hand_width": "太さ(px)",
        "group_timer": "タイマー表示",
        "lbl_mode_h": "【Ｈモード】",
        "lbl_mode_m": "【Ｍモード】",
        "lbl_mode_s": "【Ｓモード】",
        "slider_radius": "半径(%)",
        "lbl_ring": "【リング】",
        "slider_ring_width": "太さ(%)",
        "lbl_flash": "【終了時の点滅】",
        "slider_flash_interval": "間隔(秒)",
        "btn_close": "閉じる",
        "btn_color_settings": "色設定",
        # 右クリックメニュー
        "menu_timer_reset": "タイマー終了",
        "menu_timer_set": "タイマー設定",
        "menu_date_flip": "日付の上下位置変更",
        "menu_language": "language",
        "menu_lang_ja": "日本語",
        "menu_lang_en": "English",
        "menu_settings": "詳細設定",
        "menu_quit": "終了",
        "orphan_seq_msg": "保存されていないシーケンスがお気に入りに登録されていたので、お気に入りから削除しました。",
        "seq_interrupt_msg": "シーケンスタイマーが実行中です。中断しますか？",
        "seq_interrupt_ok": "中断する",
        "seq_interrupt_cancel": "戻る",
        # 日付フォーマット
        "date_formats": ["date_simple", "date_with_weekday_short", "date_with_weekday_long", "date_full"],
        # 色段階設定ダイアログ
        "color_stages_title": "色段階設定",
        "col_threshold": "残り時間",
        "col_color": "色",
        "btn_add_stage": "段階を追加",
        "btn_del_stage": "段階を削除",
        "threshold_unit_h": "時間",
        "threshold_unit_m": "分",
        "threshold_unit_s": "秒",
        "stage_note": "※ 残り時間が閾値以下になると対応する色に変わります（降順で並べ替え）",
        # シーケンスタイマー
        "seq_label": "シーケンスタイマー（ステップの順にタイマーを開始できます）",
        "seq_name_label": "シーケンス名:",
        "seq_steps_label": "ステップ一覧",
        "seq_col_type": "種別",
        "seq_col_value": "値",
        "seq_type_duration": "残り",
        "seq_type_time": "時刻",
        "btn_seq_add_dur": "シーケンスに追加",
        "btn_seq_add_time": "シーケンスに追加",
        "btn_seq_del": "１つのステップを削除",
        "btn_seq_clear": "ステップ一覧を削除",
        "btn_seq_add_fav": "お気に入りに追加",
        "fav_prefix_seq": "シーケンス",
        "btn_seq_save": "保存",
        "btn_seq_load": "読み込み",
        "btn_seq_delete_saved": "保存済み削除",
        "btn_seq_start": "シーケンス開始",
        "btn_seq_start_from": "ここからシーケンス開始",
        "seq_saved_label": "保存済みシーケンス:",
        "seq_name_placeholder": "シーケンス名を入力",
        "seq_err_no_steps": "ステップが空です",
        "seq_err_no_name": "シーケンス名を入力してください",
        "seq_err_name_exists": "同名のシーケンスが既に存在します",
        "seq_err_no_select_step": "開始するステップを選択してください",
        "seq_delete_fav_confirm": "このシーケンスはお気に入りに登録されています。削除しますか？",
        "seq_delete_ok": "削除する",
        "seq_delete_cancel": "キャンセル",
        "btn_step_add": "ステップを追加",
        "step_format_error": "形式エラー: [種別] HH:MM:SS の形式で入力してください",
    },
    "en": {
        # Timer dialog
        "timer_dialog_title": "Timer Settings",
        "timer_duration_label": "Set by duration (e.g. 1:30:00→1h30m / 45:00→45min / 10→10min)",
        "timer_time_label": "Set by time (specify end time)",
        "btn_remember": "Save",
        "btn_delete": "Delete",
        "btn_add_fav": "Add to Favorites",
        "btn_start": "Start",
        "fav_label": "Manage Favorites (Favorites can be started from the clock's right-click menu)",
        "btn_up": "↑ Up",
        "btn_down": "↓ Down",
        "btn_del_fav": "Delete",
        "btn_cancel": "Cancel",
        "fav_prefix_duration": "Dur:",
        "fav_prefix_time": "Time:",
        # Settings dialog
        "settings_dialog_title": "Settings",
        "group_general": "General",
        "cb_always_on_top": "Always on Top",
        "cb_smooth_second": "Smooth Second Hand",
        "cb_save_window_pos": "Remember Window Position",
        "slider_opacity": "Opacity(%)",
        "slider_diameter": "Diameter(px)",
        "group_dial": "Dial Settings",
        "lbl_numbers": "[Numbers]",
        "btn_color": "Color",
        "btn_font": "Font",
        "slider_num_radius": "Distance(px)",
        "lbl_mark5": "[5-min Marks]",
        "lbl_mark1": "[1-min Marks]",
        "slider_mark_width": "Width(px)",
        "slider_mark_len": "Length(%)",
        "lbl_date": "[Date]",
        "cb_date_show": "Show",
        "slider_date_opacity": "Opacity(%)",
        "slider_date_radius": "Distance(up/down)(px)",
        "lbl_date_format": "Format:",
        "group_hands": "Hand Settings",
        "lbl_hour_hand": "[Hour Hand]",
        "lbl_minute_hand": "[Minute Hand]",
        "lbl_second_hand": "[Second Hand]",
        "slider_hand_len": "Length(%)",
        "slider_hand_width": "Width(px)",
        "group_timer": "Timer Display",
        "lbl_mode_h": "[H Mode]",
        "lbl_mode_m": "[M Mode]",
        "lbl_mode_s": "[S Mode]",
        "slider_radius": "Radius(%)",
        "lbl_ring": "[Ring]",
        "slider_ring_width": "Width(%)",
        "lbl_flash": "[Finish Flash]",
        "slider_flash_interval": "Interval(sec)",
        "btn_close": "Close",
        "btn_color_settings": "Color Settings",
        # Context menu
        "menu_timer_reset": "Stop Timer",
        "menu_timer_set": "Timer Settings",
        "menu_date_flip": "Toggle Date Position",
        "menu_language": "Language",
        "menu_lang_ja": "日本語",
        "menu_lang_en": "English",
        "menu_settings": "Settings",
        "menu_quit": "Quit",
        "orphan_seq_msg": "Some favorites referenced sequences that no longer exist and have been removed from Favorites.",
        "seq_interrupt_msg": "A sequence timer is running. Do you want to interrupt it?",
        "seq_interrupt_ok": "Interrupt",
        "seq_interrupt_cancel": "Cancel",
        # Date formats
        "date_formats": ["date_simple", "date_with_weekday_short", "date_with_weekday_long", "date_full"],
        # Color stages dialog
        "color_stages_title": "Color Stage Settings",
        "col_threshold": "Remaining Time",
        "col_color": "Color",
        "btn_add_stage": "Add Stage",
        "btn_del_stage": "Delete Stage",
        "threshold_unit_h": "h",
        "threshold_unit_m": "min",
        "threshold_unit_s": "sec",
        "stage_note": "※ Color changes when remaining time falls below threshold (sorted descending)",
        # Sequence timer
        "seq_label": "Sequence Timer (Start timers in step order)",
        "seq_name_label": "Name:",
        "seq_steps_label": "Steps",
        "seq_col_type": "Type",
        "seq_col_value": "Value",
        "seq_type_duration": "Dur",
        "seq_type_time": "Time",
        "btn_seq_add_dur": "Add to Sequence",
        "btn_seq_add_time": "Add to Sequence",
        "btn_seq_del": "Delete Step",
        "btn_seq_clear": "Clear All Steps",
        "btn_seq_add_fav": "Add to Favorites",
        "fav_prefix_seq": "Seq:",
        "btn_seq_save": "Save",
        "btn_seq_load": "Load",
        "btn_seq_delete_saved": "Delete Saved",
        "btn_seq_start": "Start Sequence",
        "btn_seq_start_from": "Start Sequence From Here",
        "seq_saved_label": "Saved Sequences:",
        "seq_name_placeholder": "Enter sequence name",
        "seq_err_no_steps": "No steps defined",
        "seq_err_no_name": "Please enter a sequence name",
        "seq_err_name_exists": "A sequence with this name already exists",
        "seq_err_no_select_step": "Please select a step to start from",
        "seq_delete_fav_confirm": "This sequence is registered in Favorites. Delete anyway?",
        "seq_delete_ok": "Delete",
        "seq_delete_cancel": "Cancel",
        "btn_step_add": "Add Step",
        "step_format_error": "Format error: enter as [type] HH:MM:SS",
    },
}

# ============================================================
# デフォルト色段階設定
# ============================================================
# 明度180/255 ≒ #b4 → 各色をやや暗めに設定
# 各エントリ: {"threshold": 秒数, "color": "#rrggbb"}
# threshold降順で並べる（最初にマッチした色を使用）
DEFAULT_COLOR_STAGES = {
    "wedge_stages_h": [
        {"threshold": 7200, "color": "#0056d8"},   # 残り2時間超 → 青
        {"threshold": 3600, "color": "#007ec7"},   # 残り1h〜2h → 水色系
    ],
    "wedge_stages_m": [
        {"threshold": 3600, "color": "#005555"},   # 残り60分以下 → 暗青緑
        {"threshold": 2700, "color": "#005a00"},   # 残り45分以下 → 暗緑
        {"threshold": 1800, "color": "#486400"},   # 残り30分以下 → 暗黄緑
        {"threshold": 900,  "color": "#969600"},   # 残り15分以下 → 暗黄
        {"threshold": 300,  "color": "#c86700"},   # 残り5分以下  → 暗オレンジ
    ],
    "wedge_stages_s": [
        {"threshold": 60,   "color": "#820000"},   # 残り60秒以下 → 暗赤
        {"threshold": 10,   "color": "#960096"},   # 残り10秒以下 → 暗赤紫
    ],
}


def get_wedge_color(stages, rem):
    """
    残り時間remに対応する色を返す。
    stagesはthreshold降順のリスト。
    降順に走査し、rem <= threshold を満たす最後のエントリ（＝最小threshold）の色を使う。
    つまり「remが超えていない閾値の中で最も小さいもの」の色が適用される。
    remがどの閾値も超えていない場合は最大thresholdの色（モード突入直後）を使う。
    """
    matched_color = None
    for stage in sorted(stages, key=lambda x: x["threshold"], reverse=True):
        if rem <= stage["threshold"]:
            matched_color = stage["color"]
        else:
            break
    if matched_color:
        return matched_color
    # remがどのthresholdより大きい場合は最大thresholdの色（モード突入直後）
    if stages:
        top = max(stages, key=lambda x: x["threshold"])
        return top["color"]
    return "#888888"


def get_date_format_labels(lang, now):
    """言語に応じた日付フォーマットのラベル一覧を返す"""
    if lang == "ja":
        w_jp = ["月","火","水","木","金","土","日"][now.weekday()]
        return [
            f"{now.month}/{now.day}",
            f"{now.month}/{now.day}({w_jp})",
            f"{now.month}月{now.day}日{w_jp}曜日",
            f"{now.year}/{now.month}/{now.day}",
        ]
    else:
        w_en_short = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][now.weekday()]
        mon_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][now.month-1]
        return [
            f"{now.month}/{now.day}",
            f"{w_en_short} {now.month}/{now.day}",
            f"{w_en_short}, {mon_en} {now.day}",
            f"{now.month}/{now.day}/{now.year}",
        ]

def format_date_string(lang, idx, now):
    """描画用の日付文字列を生成"""
    labels = get_date_format_labels(lang, now)
    return labels[idx] if 0 <= idx < len(labels) else labels[0]


def smart_move(dialog, parent_widget):
    """
    ダイアログを時計ウィジェットに重ならず、かつ画面内に収まる位置へ移動する。
    優先順位: 右 → 左 → 下 → 上 → クランプ
    """
    screen = QApplication.primaryScreen().availableGeometry()
    pw = parent_widget.geometry()
    dw = dialog.width()
    dh = dialog.height()

    candidates = [
        (pw.right() + 10, pw.top()),
        (pw.left() - dw - 10, pw.top()),
        (pw.left(), pw.bottom() + 10),
        (pw.left(), pw.top() - dh - 10),
    ]

    for x, y in candidates:
        y = max(screen.top(), min(y, screen.bottom() - dh))
        x = max(screen.left(), min(x, screen.right() - dw))
        from PySide6.QtCore import QRect
        dlg_rect = QRect(x, y, dw, dh)
        if not dlg_rect.intersects(pw):
            dialog.move(x, y)
            return

    x = max(screen.left(), min(pw.right() + 10, screen.right() - dw))
    y = max(screen.top(), min(pw.top(), screen.bottom() - dh))
    dialog.move(x, y)


# ============================================================
# 色段階設定ダイアログ
# ============================================================
class ColorStagesDialog(QDialog):
    """
    各モード（H/M/S）の色段階を設定するダイアログ。
    stagesは {"threshold": 秒数, "color": "#rrggbb"} のリスト。
    閾値の単位は mode によって変える（H=時間, M=分, S=秒）。
    """
    def __init__(self, parent, mode, stages):
        super().__init__(parent)
        self.p = parent
        self.mode = mode  # "h", "m", "s"
        # ディープコピー
        self.stages = [dict(s) for s in stages]
        lang = self.p.settings.get("language", "ja")
        self.T = LANG[lang]
        self.setWindowTitle(self.T["color_stages_title"] + f" ({mode.upper()})")
        self.resize(420, 400)
        self._build_ui()
        self.adjustSize()
        smart_move(self, self.p)

    def _unit_label(self):
        if self.mode == "h":
            return self.T["threshold_unit_h"]
        elif self.mode == "m":
            return self.T["threshold_unit_m"]
        else:
            return self.T["threshold_unit_s"]

    def _to_display(self, sec):
        """秒 → 表示単位に変換"""
        if self.mode == "h":
            return sec / 3600.0
        elif self.mode == "m":
            return sec / 60.0
        else:
            return float(sec)

    def _to_seconds(self, val):
        """表示単位 → 秒に変換"""
        if self.mode == "h":
            return val * 3600
        elif self.mode == "m":
            return val * 60
        else:
            return val

    def _mode_range_label(self):
        lang = self.p.settings.get("language", "ja")
        if self.mode == "h":
            return "残り時間（1時間以上）" if lang == "ja" else "Remaining Time (1h+)"
        elif self.mode == "m":
            return "残り時間（1分～60分）" if lang == "ja" else "Remaining Time (1min-60min)"
        else:
            return "残り時間（1秒～60秒）" if lang == "ja" else "Remaining Time (1sec-60sec)"

    def _build_ui(self):
        layout = QVBoxLayout(self)

        note = QLabel(self.T["stage_note"])
        note.setWordWrap(True)
        note.setStyleSheet("color: #aaa; font-size: 10px;")
        layout.addWidget(note)

        # ヘッダー行
        h_head = QHBoxLayout()
        cb_dummy = QCheckBox(); cb_dummy.setFixedWidth(20); cb_dummy.setEnabled(False)
        h_head.addWidget(cb_dummy)
        lbl_thr = QLabel(f"{self._mode_range_label()} ({self._unit_label()})")
        lbl_thr.setMinimumWidth(180)
        lbl_col = QLabel(self.T["col_color"])
        lbl_col.setFixedWidth(80)
        h_head.addWidget(lbl_thr)
        h_head.addWidget(lbl_col)
        h_head.addStretch()
        layout.addLayout(h_head)

        # スクロールエリア（段階リスト）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rows_widget = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_widget)
        self.rows_layout.setSpacing(4)
        scroll.setWidget(self.rows_widget)
        layout.addWidget(scroll)

        self.row_checkboxes = []  # 各行のチェックボックスを保持
        self._refresh_rows()

        # 追加・削除ボタン
        h_btn = QHBoxLayout()
        btn_add = QPushButton(self.T["btn_add_stage"])
        btn_add.clicked.connect(self._add_stage)
        btn_del = QPushButton(self.T["btn_del_stage"])
        btn_del.clicked.connect(self._del_stage)
        h_btn.addWidget(btn_add)
        h_btn.addWidget(btn_del)
        layout.addLayout(h_btn)

        btn_close = QPushButton(self.T["btn_close"])
        btn_close.clicked.connect(self._save_and_close)
        layout.addWidget(btn_close)

    def _refresh_rows(self):
        """段階リストの行を全再描画"""
        # 降順ソート
        self.stages.sort(key=lambda x: x["threshold"], reverse=True)

        # 既存ウィジェットを削除
        while self.rows_layout.count():
            item = self.rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.row_checkboxes = []

        for i, stage in enumerate(self.stages):
            row = QWidget()
            h = QHBoxLayout(row)
            h.setContentsMargins(0, 0, 0, 0)

            # チェックボックス（削除対象選択用）
            cb = QCheckBox()
            cb.setFixedWidth(20)
            h.addWidget(cb)
            self.row_checkboxes.append(cb)

            # 閾値スピンボックス
            spin = QDoubleSpinBox()
            spin.setDecimals(1 if self.mode == "h" else 0)
            spin.setRange(0.1 if self.mode == "h" else 1, 99999)
            spin.setValue(self._to_display(stage["threshold"]))
            spin.setFixedWidth(120)
            spin.setSuffix(f" {self._unit_label()}")

            def make_threshold_handler(idx, sp):
                def handler(val):
                    self.stages[idx]["threshold"] = int(self._to_seconds(val))
                return handler
            spin.valueChanged.connect(make_threshold_handler(i, spin))
            h.addWidget(spin)

            # 色ボタン
            btn_c = QPushButton()
            btn_c.setFixedSize(60, 24)
            btn_c.setStyleSheet(f"background-color: {stage['color']}; border: 1px solid #555;")

            def make_color_handler(idx, btn):
                def handler():
                    c = QColorDialog.getColor(QColor(self.stages[idx]["color"]), self)
                    if c.isValid():
                        self.stages[idx]["color"] = c.name()
                        btn.setStyleSheet(f"background-color: {c.name()}; border: 1px solid #555;")
                return handler
            btn_c.clicked.connect(make_color_handler(i, btn_c))
            h.addWidget(btn_c)
            h.addStretch()

            self.rows_layout.addWidget(row)

        self.rows_layout.addStretch()

    def _add_stage(self):
        """段階を追加（現在の最小閾値の半分あたりに追加）"""
        if self.stages:
            min_thr = min(s["threshold"] for s in self.stages)
            new_thr = max(1, min_thr // 2)
        else:
            # デフォルト
            if self.mode == "h":
                new_thr = 3600
            elif self.mode == "m":
                new_thr = 300
            else:
                new_thr = 30
        self.stages.append({"threshold": new_thr, "color": "#888888"})
        self._refresh_rows()

    def _del_stage(self):
        """チェックされた段階を削除"""
        if not self.stages:
            return
        checked_indices = [i for i, cb in enumerate(self.row_checkboxes) if cb.isChecked()]
        if not checked_indices:
            return
        # 削除後に最低1段階残るかチェック
        if len(self.stages) - len(checked_indices) < 1:
            lang = self.p.settings.get("language", "ja")
            QMessageBox.warning(self, "", "最低1段階は必要です" if lang == "ja" else "At least one stage is required.")
            return
        # 降順で削除（インデックスがずれないように後ろから）
        for i in sorted(checked_indices, reverse=True):
            self.stages.pop(i)
        self._refresh_rows()

    def _save_and_close(self):
        """スピンの値を確定してからsortしてsettingsへ保存"""
        # スピンボックスの値はvalueChangedで都度更新されているが、
        # フォーカス中の場合に備えて全スピンをコミット
        self.stages.sort(key=lambda x: x["threshold"], reverse=True)
        key = f"wedge_stages_{self.mode}"
        self.p.settings[key] = self.stages
        self.p.save_settings()
        self.p.update()
        self.accept()


class SeqStepListWidget(QListWidget):
    """シーケンスステップのD&Dリスト"""
    def __init__(self, dialog):
        super().__init__(dialog)
        self.dialog = dialog
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.dialog._seq_step_delete()
        elif (event.key() == Qt.Key_V and
              event.modifiers() & Qt.ControlModifier and
              len(self.dialog.p.current_seq_steps) == 0):
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            if text.strip():
                self.dialog._paste_schedule_text(text)
        else:
            super().keyPressEvent(event)

    def dropEvent(self, event):
        # D&D前の順序を記録してから親クラスのdropEventを呼ぶ
        old_steps = [dict(s) for s in self.dialog.p.current_seq_steps]
        super().dropEvent(event)
        # リスト表示の順にstepsを並び替え
        new_steps = []
        for i in range(self.count()):
            label = self.item(i).text()
            match = next((s for s in old_steps
                          if self.dialog._step_label(s) == label), None)
            if match:
                new_steps.append(match)
                old_steps.remove(match)
        self.dialog.p.current_seq_steps = new_steps


class FavListWidget(QListWidget):
    """ドラッグ＆ドロップで並び替えできるお気に入りリスト"""
    def __init__(self, dialog):
        super().__init__(dialog)
        self.dialog = dialog
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.dialog.fav_delete()
        else:
            super().keyPressEvent(event)

    def dropEvent(self, event):
        # D&D前の順序とラベルを保存
        old_favs = list(self.dialog.p.settings.get("favorites", []))
        old_labels = [self.dialog.p._fav_display_label(f) for f in old_favs]
        super().dropEvent(event)
        # リスト表示の順にfavsを並び替え（重複ラベルにも対応）
        new_order = []
        used = [False] * len(old_favs)
        for i in range(self.count()):
            label = self.item(i).text()
            for j, (lbl, fav) in enumerate(zip(old_labels, old_favs)):
                if not used[j] and lbl == label:
                    new_order.append(fav)
                    used[j] = True
                    break
        self.dialog.p.settings["favorites"] = new_order
        self.dialog.p.save_settings()


class TimerInputDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        lang = self.p.settings.get("language", "ja")
        self.T = LANG[lang]
        self.setWindowTitle(self.T["timer_dialog_title"])
        self.resize(550, 520)
        self.p.sort_all_history()
        self._loaded_seq_snapshot = None  # 読み込んだシーケンスのスナップショット
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # エリアカラー定数
        FAV_COLOR  = "#1a3a2a"   # お気に入りエリア：深緑
        FAV_BORDER = "#2d6e4e"   # お気に入りボーダー
        FAV_BTN    = "#1e5c3a"   # お気に入りボタン背景
        SEQ_COLOR  = "#2a1a3a"   # シーケンスエリア：深紫
        SEQ_BORDER = "#5a3a7a"   # シーケンスボーダー
        SEQ_BTN    = "#4a2a6a"   # シーケンスボタン背景
        BTN_TEXT   = "color: white; font-weight: bold;"

        v_dur = QVBoxLayout()
        lbl_dur = QLabel(self.T["timer_duration_label"])
        lbl_dur.setStyleSheet("font-weight: bold; color: #ccc;")
        v_dur.addWidget(lbl_dur)
        h_dur = QHBoxLayout()
        self.cb_dur = QComboBox(); self.cb_dur.setEditable(True)
        self.cb_dur.addItems(self.p.settings.get("history_duration", []))
        self.cb_dur.setEditText(self.p.settings.get("last_duration_val", "00:00:10"))
        h_dur.addWidget(self.cb_dur, 1)
        for n_key, func in [("btn_remember", self.save_dur), ("btn_delete", lambda: self.del_history(self.cb_dur, "history_duration"))]:
            btn = QPushButton(self.T[n_key]); btn.clicked.connect(func); h_dur.addWidget(btn)
        btn_fav_dur = QPushButton(self.T["btn_add_fav"]); btn_fav_dur.clicked.connect(self.add_fav_duration)
        btn_fav_dur.setStyleSheet(f"background-color: {FAV_BTN}; {BTN_TEXT}"); h_dur.addWidget(btn_fav_dur)
        btn_start_dur = QPushButton(self.T["btn_start"])
        btn_start_dur.setStyleSheet("background-color: #665544; color: white; font-weight: bold;")
        btn_start_dur.clicked.connect(self.start_by_duration); h_dur.addWidget(btn_start_dur)
        v_dur.addLayout(h_dur); layout.addLayout(v_dur)

        layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        v_time = QVBoxLayout()
        lbl_time = QLabel(self.T["timer_time_label"])
        lbl_time.setStyleSheet("font-weight: bold; color: #ccc;")
        v_time.addWidget(lbl_time)
        h_time = QHBoxLayout()
        self.cb_time = QComboBox(); self.cb_time.setEditable(True)
        self.cb_time.addItems(self.p.settings.get("history_time", []))
        self.cb_time.setEditText(self.p.settings.get("last_time_val", "15:00:00"))
        h_time.addWidget(self.cb_time, 1)
        for n_key, func in [("btn_remember", self.save_time), ("btn_delete", lambda: self.del_history(self.cb_time, "history_time"))]:
            btn = QPushButton(self.T[n_key]); btn.clicked.connect(func); h_time.addWidget(btn)
        btn_fav_time = QPushButton(self.T["btn_add_fav"]); btn_fav_time.clicked.connect(self.add_fav_time)
        btn_fav_time.setStyleSheet(f"background-color: {FAV_BTN}; {BTN_TEXT}"); h_time.addWidget(btn_fav_time)
        btn_start_time = QPushButton(self.T["btn_start"])
        btn_start_time.setStyleSheet("background-color: #665544; color: white; font-weight: bold;")
        btn_start_time.clicked.connect(self.start_by_time); h_time.addWidget(btn_start_time)
        v_time.addLayout(h_time); layout.addLayout(v_time)

        layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        # ============ お気に入りエリア（色付き枠） ============
        fav_frame = QFrame()
        fav_frame.setObjectName("favFrame")
        fav_frame.setStyleSheet(f"QFrame#favFrame {{ background-color: {FAV_COLOR}; border: 2px solid {FAV_BORDER}; border-radius: 4px; }}")
        fav_layout = QVBoxLayout(fav_frame)
        fav_layout.setContentsMargins(8, 8, 8, 8)

        lbl_fav = QLabel(self.T["fav_label"])
        lbl_fav.setStyleSheet(f"font-weight: bold; color: #ccc; background: transparent; border: none;")
        fav_layout.addWidget(lbl_fav)
        self.fav_list = FavListWidget(self); self.fav_list.setFixedHeight(120)
        self.fav_list.setStyleSheet("border: none;")
        self.refresh_fav_list(); fav_layout.addWidget(self.fav_list)
        h_fav_btn = QHBoxLayout()
        btn_up = QPushButton(self.T["btn_up"]); btn_up.clicked.connect(self.fav_move_up); h_fav_btn.addWidget(btn_up)
        btn_down = QPushButton(self.T["btn_down"]); btn_down.clicked.connect(self.fav_move_down); h_fav_btn.addWidget(btn_down)
        btn_del_fav = QPushButton(self.T["btn_del_fav"]); btn_del_fav.clicked.connect(self.fav_delete); h_fav_btn.addWidget(btn_del_fav)
        fav_layout.addLayout(h_fav_btn)
        layout.addWidget(fav_frame)

        layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        # ============ シーケンスタイマーエリア（色付き枠） ============
        seq_frame = QFrame()
        seq_frame.setObjectName("seqFrame")
        seq_frame.setStyleSheet(f"QFrame#seqFrame {{ background-color: {SEQ_COLOR}; border: 2px solid {SEQ_BORDER}; border-radius: 4px; }}")
        seq_layout = QVBoxLayout(seq_frame)
        seq_layout.setContentsMargins(8, 8, 8, 8)

        lbl_seq = QLabel(self.T["seq_label"])
        lbl_seq.setStyleSheet("font-weight: bold; color: #ccc; background: transparent; border: none;")
        lbl_seq.setWordWrap(True)
        seq_layout.addWidget(lbl_seq)

        # 保存済みシーケンス選択
        h_saved = QHBoxLayout()
        h_saved.addWidget(QLabel(self.T["seq_saved_label"]))
        self.cb_seq_saved = QComboBox()
        self.cb_seq_saved.setMinimumWidth(180)
        self._refresh_seq_saved_combo()
        self.cb_seq_saved.currentIndexChanged.connect(self._on_seq_saved_changed)
        h_saved.addWidget(self.cb_seq_saved, 1)
        btn_seq_load = QPushButton(self.T["btn_seq_load"])
        btn_seq_load.clicked.connect(self._seq_load)
        h_saved.addWidget(btn_seq_load)
        btn_seq_del_saved = QPushButton(self.T["btn_seq_delete_saved"])
        btn_seq_del_saved.clicked.connect(self._seq_delete_saved)
        h_saved.addWidget(btn_seq_del_saved)
        seq_layout.addLayout(h_saved)

        # シーケンス名 + 保存ボタン
        h_name = QHBoxLayout()
        h_name.addWidget(QLabel(self.T["seq_name_label"]))
        from PySide6.QtWidgets import QLineEdit
        self.seq_name_edit = QLineEdit()
        self.seq_name_edit.setMinimumWidth(200)
        self.seq_name_edit.setPlaceholderText(self.T["seq_name_placeholder"])
        self.seq_name_edit.textChanged.connect(self._on_seq_name_changed)
        h_name.addWidget(self.seq_name_edit, 1)
        self.btn_seq_save = QPushButton(self.T["btn_seq_save"])
        self.btn_seq_save.clicked.connect(self._seq_save)
        h_name.addWidget(self.btn_seq_save)
        seq_layout.addLayout(h_name)

        # ステップ追加入力欄
        h_step_input = QHBoxLayout()
        self.step_type_combo = QComboBox()
        self.step_type_combo.addItem(self.T["seq_type_duration"], "duration")
        self.step_type_combo.addItem(self.T["seq_type_time"], "time")
        self.step_type_combo.setFixedWidth(110)
        h_step_input.addWidget(self.step_type_combo)
        self.step_input_edit = QLineEdit("00:00:00")
        self.step_input_edit.setFixedWidth(100)
        self.step_input_edit.returnPressed.connect(self._step_input_add)
        h_step_input.addWidget(self.step_input_edit)
        btn_step_add = QPushButton(self.T["btn_step_add"])
        btn_step_add.clicked.connect(self._step_input_add)
        h_step_input.addWidget(btn_step_add)
        h_step_input.addStretch()
        seq_layout.addLayout(h_step_input)

        # ステップリスト
        lbl_steps = QLabel(self.T["seq_steps_label"])
        lbl_steps.setStyleSheet("color: #aaa; font-size: 10px; background: transparent; border: none;")
        seq_layout.addWidget(lbl_steps)
        self.seq_list = SeqStepListWidget(self)
        self.seq_list.setFixedHeight(130)
        self.seq_list.setStyleSheet("border: none;")
        self._refreshing_list = False
        self._refresh_seq_list()
        self.seq_list.itemChanged.connect(self._on_item_changed)
        seq_layout.addWidget(self.seq_list)

        # ステップ操作ボタン
        h_seq_step = QHBoxLayout()
        btn_seq_up = QPushButton(self.T["btn_up"])
        btn_seq_up.clicked.connect(self._seq_step_up)
        h_seq_step.addWidget(btn_seq_up)
        btn_seq_down = QPushButton(self.T["btn_down"])
        btn_seq_down.clicked.connect(self._seq_step_down)
        h_seq_step.addWidget(btn_seq_down)
        btn_seq_del = QPushButton(self.T["btn_seq_del"])
        btn_seq_del.clicked.connect(self._seq_step_delete)
        h_seq_step.addWidget(btn_seq_del)
        btn_seq_clear = QPushButton(self.T["btn_seq_clear"])
        btn_seq_clear.clicked.connect(self._seq_step_clear)
        h_seq_step.addWidget(btn_seq_clear)
        self.btn_seq_add_fav = QPushButton(self.T["btn_seq_add_fav"])
        self.btn_seq_add_fav.setEnabled(False)
        self.btn_seq_add_fav.clicked.connect(self._seq_add_to_fav)
        self.btn_seq_add_fav.setStyleSheet(f"background-color: {FAV_BTN}; {BTN_TEXT}")
        h_seq_step.addWidget(self.btn_seq_add_fav)
        seq_layout.addLayout(h_seq_step)

        # 実行ボタン
        h_seq_ctrl = QHBoxLayout()
        self.btn_seq_start = QPushButton(self.T["btn_seq_start"])
        self.btn_seq_start.setEnabled(False)  # 初期はグレーアウト（スタイルは_refresh_seq_listで設定）
        self.btn_seq_start.clicked.connect(self._seq_start)
        h_seq_ctrl.addWidget(self.btn_seq_start)
        self.btn_seq_start_from = QPushButton(self.T["btn_seq_start_from"])
        self.btn_seq_start_from.setEnabled(False)  # 初期はグレーアウト
        self.btn_seq_start_from.clicked.connect(self._seq_start_from)
        h_seq_ctrl.addWidget(self.btn_seq_start_from)
        seq_layout.addLayout(h_seq_ctrl)
        layout.addWidget(seq_frame)

        # ステップ選択変化でグレーアウト制御
        self.seq_list.currentRowChanged.connect(self._on_seq_list_row_changed)
        # btn_seq_start生成後に再度グレーアウト判定
        self._refresh_seq_list()

        layout.addStretch()
        btn_close = QPushButton(self.T["btn_close"]); btn_close.clicked.connect(self.reject); layout.addWidget(btn_close)

        self.adjustSize()
        smart_move(self, self.p)

    def format_duration(self, text):
        s = text.translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        parts = re.findall(r'\d+', s); h, m, sec = 0, 0, 0
        if len(parts) >= 3: h, m, sec = map(int, parts[:3])
        elif len(parts) == 2: m, sec = map(int, parts)
        elif len(parts) == 1: m = int(parts[0])
        return f"{h:02d}:{m:02d}:{sec:02d}"

    def save_dur(self):
        val = self.format_duration(self.cb_dur.currentText())
        self.p.update_history("history_duration", val)
        self.cb_dur.clear(); self.cb_dur.addItems(self.p.settings["history_duration"]); self.cb_dur.setEditText(val)

    def save_time(self):
        val = self.cb_time.currentText().translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        self.p.update_history("history_time", val)
        self.cb_time.clear(); self.cb_time.addItems(self.p.settings["history_time"]); self.cb_time.setEditText(val)

    def del_history(self, cb, key):
        val = cb.currentText()
        if val in self.p.settings[key]:
            self.p.settings[key].remove(val); self.p.save_settings()
            cb.clear(); cb.addItems(self.p.settings[key])

    def add_fav_duration(self):
        val = self.format_duration(self.cb_dur.currentText())
        label = f"{self.T['fav_prefix_duration']}{val}"
        self.p.settings.setdefault("favorites", []).append({"type": "duration", "value": val, "label": label})
        self.p.save_settings(); self.refresh_fav_list()

    def add_fav_time(self):
        text = self.cb_time.currentText().translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        parts = re.findall(r'\d+', text)
        if not parts: return
        h = int(parts[0]); m = int(parts[1]) if len(parts) > 1 else 0; s = int(parts[2]) if len(parts) > 2 else 0
        val = f"{h:02d}:{m:02d}:{s:02d}"
        label = f"{self.T['fav_prefix_time']}{val}"
        self.p.settings.setdefault("favorites", []).append({"type": "time", "value": val, "label": label})
        self.p.save_settings(); self.refresh_fav_list()

    def refresh_fav_list(self):
        self.fav_list.clear()
        for fav in self.p.settings.get("favorites", []):
            self.fav_list.addItem(QListWidgetItem(self.p._fav_display_label(fav)))

    def fav_move_up(self):
        row = self.fav_list.currentRow()
        if row <= 0: return
        favs = self.p.settings.get("favorites", []); favs.insert(row - 1, favs.pop(row))
        self.p.save_settings(); self.refresh_fav_list(); self.fav_list.setCurrentRow(row - 1)

    def fav_move_down(self):
        row = self.fav_list.currentRow(); favs = self.p.settings.get("favorites", [])
        if row < 0 or row >= len(favs) - 1: return
        favs.insert(row + 1, favs.pop(row))
        self.p.save_settings(); self.refresh_fav_list(); self.fav_list.setCurrentRow(row + 1)

    def fav_delete(self):
        row = self.fav_list.currentRow(); favs = self.p.settings.get("favorites", [])
        if row < 0 or row >= len(favs): return
        favs.pop(row); self.p.save_settings(); self.refresh_fav_list()
        new_count = len(favs)
        if new_count == 0: return
        new_row = row if row < new_count else new_count - 1
        self.fav_list.setCurrentRow(new_row)

    def start_by_duration(self):
        full_val = self.format_duration(self.cb_dur.currentText()); h, m, s = map(int, full_val.split(":"))
        self.p.settings["last_duration_val"] = full_val
        self.p.set_timer_direct(datetime.now().replace(microsecond=0) + timedelta(hours=h, minutes=m, seconds=s))
        self.accept()

    def start_by_time(self):
        text = self.cb_time.currentText().translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        parts = re.findall(r'\d+', text)
        if parts:
            h = int(parts[0]); m = int(parts[1]) if len(parts) > 1 else 0; s = int(parts[2]) if len(parts) > 2 else 0
            now = datetime.now().replace(microsecond=0)
            target = now.replace(hour=h % 24, minute=m % 60, second=s % 60, microsecond=0)
            if target <= now: target += timedelta(days=1)
            self.p.settings["last_time_val"] = text; self.p.set_timer_direct(target); self.accept()

    # ---- シーケンス関連 ----

    def _refresh_seq_saved_combo(self):
        self.cb_seq_saved.clear()
        self.cb_seq_saved.addItem("--- 新規 ---", None)
        for seq in self.p.settings.get("sequences", []):
            self.cb_seq_saved.addItem(seq["name"], seq)

    def _on_seq_saved_changed(self, idx):
        pass  # 読み込みはbtnで行う

    def _seq_load(self):
        data = self.cb_seq_saved.currentData()
        if data is None: return
        self.p.current_seq_steps = [dict(s) for s in data.get("steps", [])]
        self._loaded_seq_snapshot = [dict(s) for s in data.get("steps", [])]
        self.seq_name_edit.setText(data["name"])
        self._refresh_seq_list()

    def _seq_delete_saved(self):
        data = self.cb_seq_saved.currentData()
        if data is None: return
        lang = self.p.settings.get("language", "ja")
        T = LANG[lang]
        # お気に入りに登録されているか確認
        favs = self.p.settings.get("favorites", [])
        in_fav = any(f.get("type") == "sequence" and f.get("seq_name") == data["name"] for f in favs)
        if in_fav:
            dlg = QMessageBox(self)
            dlg.setText(T["seq_delete_fav_confirm"])
            btn_ok = dlg.addButton(T["seq_delete_ok"], QMessageBox.AcceptRole)
            dlg.addButton(T["seq_delete_cancel"], QMessageBox.RejectRole)
            dlg.exec()
            if dlg.clickedButton() != btn_ok:
                return
            # お気に入りからも即時削除
            self.p.settings["favorites"] = [
                f for f in favs
                if not (f.get("type") == "sequence" and f.get("seq_name") == data["name"])
            ]
            self.refresh_fav_list()
        seqs = self.p.settings.get("sequences", [])
        self.p.settings["sequences"] = [s for s in seqs if s["name"] != data["name"]]
        self.p.save_settings()
        self._refresh_seq_saved_combo()
        self._update_seq_fav_btn()

    def _refresh_seq_list(self):
        self._refreshing_list = True
        self.seq_list.clear()
        for step in self.p.current_seq_steps:
            label = self._step_label(step)
            item = QListWidgetItem(label)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.seq_list.addItem(item)
        self._refreshing_list = False
        self._on_seq_list_row_changed(self.seq_list.currentRow())
        self._update_seq_fav_btn()
        # シーケンス開始ボタン：ステップが1つ以上あればアクティブ
        if hasattr(self, 'btn_seq_start'):
            has_steps = len(self.p.current_seq_steps) > 0
            self.btn_seq_start.setEnabled(has_steps)
            self.btn_seq_start.setStyleSheet(
                "background-color: #665544; color: white; font-weight: bold;" if has_steps else ""
            )
    def _on_seq_list_row_changed(self, row):
        if not hasattr(self, 'btn_seq_start_from'): return
        enabled = row >= 1
        self.btn_seq_start_from.setEnabled(enabled)
        if enabled:
            self.btn_seq_start_from.setStyleSheet("background-color: #665544; color: white; font-weight: bold;")
        else:
            self.btn_seq_start_from.setStyleSheet("")
        self._update_seq_fav_btn()

    def _on_seq_name_changed(self, text):
        """名前変化時：保存ボタンとお気に入り追加ボタンを更新"""
        if not hasattr(self, 'btn_seq_save'): return
        name = text.strip()
        self.btn_seq_save.setEnabled(bool(name))
        self._update_seq_fav_btn()

    def _update_seq_fav_btn(self):
        """お気に入り追加ボタンのアクティブ状態を更新する。
        条件: 名前が保存済みと一致 AND 現在のステップが保存済みと完全一致"""
        if not hasattr(self, 'btn_seq_add_fav'): return
        name = self.seq_name_edit.text().strip() if hasattr(self, 'seq_name_edit') else ""
        existing = {s["name"]: s["steps"] for s in self.p.settings.get("sequences", [])}
        if name not in existing:
            self.btn_seq_add_fav.setEnabled(False)
            return
        # 保存済みステップと現在のステップを比較
        saved_steps = existing[name]
        current_steps = self.p.current_seq_steps
        steps_match = (
            len(saved_steps) == len(current_steps) and
            all(a["type"] == b["type"] and a["value"] == b["value"]
                for a, b in zip(saved_steps, current_steps))
        )
        self.btn_seq_add_fav.setEnabled(steps_match)

    def _seq_add_to_fav(self):
        """現在のシーケンス名をお気に入りに追加"""
        name = self.seq_name_edit.text().strip()
        existing_names = [s["name"] for s in self.p.settings.get("sequences", [])]
        if name not in existing_names: return
        favs = self.p.settings.setdefault("favorites", [])
        if any(f.get("seq_name") == name for f in favs): return
        favs.append({"type": "sequence", "seq_name": name, "label": f"seq:{name}"})
        self.p.save_settings()
        self.refresh_fav_list()

    def _seq_step_clear(self):
        """ステップ一覧をすべてクリア"""
        self.p.current_seq_steps = []
        self._refresh_seq_list()

    def _step_label(self, step):
        if step["type"] == "duration":
            return f"[{self.T['seq_type_duration']}] {step['value']}"
        else:
            return f"[{self.T['seq_type_time']}] {step['value']}"

    def _seq_add_duration(self):
        val = self.format_duration(self.cb_dur.currentText())
        self.p.current_seq_steps.append({"type": "duration", "value": val})
        self._refresh_seq_list()
        self.seq_list.setCurrentRow(len(self.p.current_seq_steps) - 1)

    def _seq_add_time(self):
        text = self.cb_time.currentText().translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        parts = re.findall(r'\d+', text)
        if not parts: return
        h = int(parts[0]); m = int(parts[1]) if len(parts) > 1 else 0; s = int(parts[2]) if len(parts) > 2 else 0
        val = f"{h:02d}:{m:02d}:{s:02d}"
        self.p.current_seq_steps.append({"type": "time", "value": val})
        self._refresh_seq_list()
        self.seq_list.setCurrentRow(len(self.p.current_seq_steps) - 1)

    def _seq_step_up(self):
        row = self.seq_list.currentRow()
        if row <= 0: return
        steps = self.p.current_seq_steps
        steps.insert(row - 1, steps.pop(row))
        self._refresh_seq_list()
        self.seq_list.setCurrentRow(row - 1)

    def _seq_step_down(self):
        row = self.seq_list.currentRow()
        steps = self.p.current_seq_steps
        if row < 0 or row >= len(steps) - 1: return
        steps.insert(row + 1, steps.pop(row))
        self._refresh_seq_list()
        self.seq_list.setCurrentRow(row + 1)

    def _seq_step_delete(self):
        row = self.seq_list.currentRow()
        if row < 0 or row >= len(self.p.current_seq_steps): return
        self.p.current_seq_steps.pop(row)
        self._refresh_seq_list()
        new_count = len(self.p.current_seq_steps)
        if new_count > 0:
            self.seq_list.setCurrentRow(min(row, new_count - 1))

    def _seq_save(self):
        name = self.seq_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "", self.T["seq_err_no_name"]); return
        if not self.p.current_seq_steps:
            QMessageBox.warning(self, "", self.T["seq_err_no_steps"]); return
        seqs = self.p.settings.setdefault("sequences", [])
        for i, s in enumerate(seqs):
            if s["name"] == name:
                lang = self.p.settings.get("language", "ja")
                msg = f"「{name}」は既に保存されています。上書きしますか？" if lang == "ja" else f'"{name}" already exists. Overwrite?'
                btn_yes_label = "上書き" if lang == "ja" else "Overwrite"
                btn_no_label = "キャンセル" if lang == "ja" else "Cancel"
                dlg = QMessageBox(self)
                dlg.setText(msg)
                b_yes = dlg.addButton(btn_yes_label, QMessageBox.AcceptRole)
                dlg.addButton(btn_no_label, QMessageBox.RejectRole)
                dlg.exec()
                if dlg.clickedButton() != b_yes:
                    return
                seqs[i] = {"name": name, "steps": [dict(st) for st in self.p.current_seq_steps]}
                self.p.save_settings()
                self._refresh_seq_saved_combo()
                self._on_seq_name_changed(name)
                return
        seqs.append({"name": name, "steps": [dict(st) for st in self.p.current_seq_steps]})
        self.p.save_settings()
        self._refresh_seq_saved_combo()
        self._on_seq_name_changed(name)

    def _seq_start(self):
        if not self.p.current_seq_steps:
            QMessageBox.warning(self, "", self.T["seq_err_no_steps"]); return
        self.p.start_sequence(self.p.current_seq_steps, 0)
        self.accept()

    def _seq_start_from(self):
        row = self.seq_list.currentRow()
        if row < 1: return
        self.p.start_sequence(self.p.current_seq_steps, row)
        self.accept()

    def _step_input_add(self):
        """ステップ追加入力欄からステップを追加"""
        text = self.step_input_edit.text().strip()
        text = text.translate(str.maketrans('０１２３４５６７８９：', '0123456789:'))
        parts = re.findall(r'\d+', text)
        h, m, s = 0, 0, 0
        if len(parts) >= 3:
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        elif len(parts) == 2:
            m, s = int(parts[0]), int(parts[1])
        elif len(parts) == 1:
            m = int(parts[0])
        val = f"{h:02d}:{m:02d}:{s:02d}"
        step_type = self.step_type_combo.currentData()
        self.p.current_seq_steps.append({"type": step_type, "value": val})
        self._refresh_seq_list()
        self.seq_list.setCurrentRow(len(self.p.current_seq_steps) - 1)

    def _parse_step_text(self, text):
        """'[種別] HH:MM:SS' 形式を解析してstep dictを返す。無効な場合はNone"""
        m = re.match(r'^\[(.+)\]\s+(\d{1,2}:\d{2}:\d{2})$', text.strip())
        if not m:
            return None
        type_label = m.group(1)
        value = m.group(2)
        parts = value.split(':')
        h, mi, s = int(parts[0]), int(parts[1]), int(parts[2])
        if mi > 59 or s > 59:
            return None
        value_norm = f"{h:02d}:{mi:02d}:{s:02d}"
        for lang_key in LANG:
            if type_label == LANG[lang_key]["seq_type_duration"]:
                return {"type": "duration", "value": value_norm}
            if type_label == LANG[lang_key]["seq_type_time"]:
                return {"type": "time", "value": value_norm}
        return None

    def _on_item_changed(self, item):
        """アイテムが編集されたときに形式を検証してstepsを更新"""
        if self._refreshing_list:
            return
        row = self.seq_list.row(item)
        if row < 0 or row >= len(self.p.current_seq_steps):
            return
        text = item.text()
        result = self._parse_step_text(text)
        if result is None:
            item.setBackground(QColor("#5a1010"))
            lang = self.p.settings.get("language", "ja")
            item.setToolTip(LANG[lang]["step_format_error"])
        else:
            item.setBackground(QColor(0, 0, 0, 0))
            item.setToolTip("")
            self.p.current_seq_steps[row] = result
            self._update_seq_fav_btn()

    def _parse_schedule_time_str(self, s):
        """'900', '1030', '12' → (h, m) に変換。無効な場合はNone"""
        s = s.strip()
        if not s.isdigit():
            return None
        n = len(s)
        if n <= 2:
            return (int(s), 0)
        elif n == 3:
            return (int(s[0]), int(s[1:]))
        elif n == 4:
            return (int(s[:2]), int(s[2:]))
        return None

    def _paste_schedule_text(self, text):
        """スケジュールテキストを解析して時刻ステップとして追加"""
        steps = []
        prev_abs = -1
        pm_offset = 0
        for line in text.splitlines():
            m = re.search(r'(\d+)-(\d+)', line)
            if not m:
                continue
            end_str = m.group(2)
            parsed = self._parse_schedule_time_str(end_str)
            if parsed is None:
                continue
            h, mi = parsed
            raw_minutes = h * 60 + mi
            if prev_abs >= 0 and raw_minutes + pm_offset < prev_abs:
                pm_offset += 720
            abs_minutes = raw_minutes + pm_offset
            abs_minutes = min(abs_minutes, 23 * 60 + 59)
            actual_h = abs_minutes // 60
            actual_m = abs_minutes % 60
            steps.append({"type": "time", "value": f"{actual_h:02d}:{actual_m:02d}:00"})
            prev_abs = abs_minutes
        if steps:
            self.p.current_seq_steps = steps
            self._refresh_seq_list()


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        lang = self.p.settings.get("language", "ja")
        self.T = LANG[lang]
        self.setWindowTitle(self.T["settings_dialog_title"])
        self.resize(750, 850)

        main_layout = QVBoxLayout(self)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        content = QWidget(); layout = QVBoxLayout(content)

        # グループ枠カラー定数（タイマー設定の緑・紫・茶と被らない色）
        def style_group(gb, bg, border):
            gb.setStyleSheet(
                f"QGroupBox {{ background-color: #2a2a2a; border: 2px solid #555555; border-radius: 4px; margin-top: 8px; }}"
                f"QGroupBox::title {{ subcontrol-origin: margin; left: 8px; color: #ddd; font-weight: bold; }}"
            )

        # 全体設定
        g_gen = QGroupBox(self.T["group_general"]); gl = QVBoxLayout(g_gen)
        style_group(g_gen, "#1a2a3a", "#3a6a9a")  # 青系
        cb_top = QCheckBox(self.T["cb_always_on_top"], checked=self.p.settings["always_on_top"])
        cb_top.toggled.connect(self.p.toggle_ontop); gl.addWidget(cb_top)
        cb_smooth = QCheckBox(self.T["cb_smooth_second"], checked=self.p.settings["smooth_second"])
        cb_smooth.toggled.connect(self.p.toggle_smooth); gl.addWidget(cb_smooth)
        cb_pos = QCheckBox(self.T["cb_save_window_pos"], checked=self.p.settings.get("save_window_pos", True))
        cb_pos.toggled.connect(lambda v: self.p.update_setting("save_window_pos", v)); gl.addWidget(cb_pos)
        self.add_slider(gl, self.T["slider_opacity"], 10, 100, int(self.p.settings['opacity']*100),
                        lambda v: self.p.update_setting('opacity', v/100.0, is_opacity=True), "%")
        self.add_slider(gl, self.T["slider_diameter"], 50, 600, self.p.settings['diameter'],
                        self.p.set_diameter_live, "px")
        layout.addWidget(g_gen)

        # 文字盤の設定
        g_dial = QGroupBox(self.T["group_dial"]); dl_main = QVBoxLayout(g_dial)
        style_group(g_dial, "#1a3a3a", "#2a8a8a")  # シアン系
        rh_num = QHBoxLayout()
        rh_num.addWidget(QLabel(self.T["lbl_numbers"], font=QFont("", 9, QFont.Bold)))
        btn_nc = QPushButton(self.T["btn_color"]); btn_nc.clicked.connect(lambda: self.p.pick_color("color_text")); rh_num.addWidget(btn_nc)
        btn_nf = QPushButton(self.T["btn_font"]); btn_nf.clicked.connect(lambda: self.p.pick_font("font_main")); rh_num.addWidget(btn_nf)
        dl_main.addLayout(rh_num)
        self.add_slider(dl_main, self.T["slider_num_radius"], 10, 120, self.p.settings['number_radius'],
                        lambda v: self.p.update_setting('number_radius', v), "px")
        dl_main.addSpacing(10)

        mark_labels = {"mark5": self.T["lbl_mark5"], "mark1": self.T["lbl_mark1"]}
        for k, name in mark_labels.items():
            rh_m = QHBoxLayout()
            rh_m.addWidget(QLabel(name, font=QFont("", 9, QFont.Bold)))
            btn_mc = QPushButton(self.T["btn_color"]); btn_mc.clicked.connect(lambda *a, key=k: self.p.set_mark_color(key)); rh_m.addWidget(btn_mc)
            dl_main.addLayout(rh_m)
            self.add_slider(dl_main, self.T["slider_mark_width"], 1, 100, int(self.p.settings[k]["width"]*10),
                            lambda v, key=k: self.p.update_mark_setting(key, "width", v/10.0), is_float=True, unit="px")
            self.add_slider(dl_main, self.T["slider_mark_len"], 1, 50, self.p.settings[k]["len"],
                            lambda v, key=k: self.p.update_mark_setting(key, "len", v), "%")
            dl_main.addSpacing(10)

        rh_d = QHBoxLayout()
        rh_d.addWidget(QLabel(self.T["lbl_date"], font=QFont("", 9, QFont.Bold)))
        btn_dc = QPushButton(self.T["btn_color"]); btn_dc.clicked.connect(lambda: self.p.pick_color("color_date")); rh_d.addWidget(btn_dc)
        btn_df = QPushButton(self.T["btn_font"]); btn_df.clicked.connect(lambda: self.p.pick_font("font_date")); rh_d.addWidget(btn_df)
        dl_main.addLayout(rh_d)
        cb_show = QCheckBox(self.T["cb_date_show"], checked=self.p.settings["date_show"])
        cb_show.toggled.connect(lambda v: self.p.update_setting('date_show', v)); dl_main.addWidget(cb_show)
        self.add_slider(dl_main, self.T["slider_date_opacity"], 10, 100, int(self.p.settings['date_opacity']*100),
                        lambda v: self.p.update_setting('date_opacity', v/100.0), "%")
        self.add_slider(dl_main, self.T["slider_date_radius"], -120, 120, self.p.settings['date_radius'],
                        lambda v: self.p.update_setting('date_radius', v), "px")

        dh_fmt = QHBoxLayout()
        lbl_f = QLabel(self.T["lbl_date_format"]); lbl_f.setFixedWidth(100); dh_fmt.addWidget(lbl_f)
        dh_fmt.addSpacing(25)
        self.cb_fmt = QComboBox()
        now = datetime.now()
        self.cb_fmt.addItems(get_date_format_labels(lang, now))
        self.cb_fmt.setCurrentIndex(self.p.settings.get("date_format_idx", 0))
        self.cb_fmt.setFixedWidth(180)
        self.cb_fmt.currentIndexChanged.connect(self.p.set_date_format)
        dh_fmt.addWidget(self.cb_fmt); dh_fmt.addStretch()
        dl_main.addLayout(dh_fmt)
        layout.addWidget(g_dial)

        # 針の設定
        g_hands = QGroupBox(self.T["group_hands"]); vh = QVBoxLayout(g_hands)
        style_group(g_hands, "#3a2a1a", "#9a6a2a")  # オレンジ系
        hand_configs = [
            ("h", self.T["lbl_hour_hand"], "color_hour_hand"),
            ("m", self.T["lbl_minute_hand"], "color_minute_hand"),
            ("s", self.T["lbl_second_hand"], "color_second_hand"),
        ]
        for prefix, name, c_key in hand_configs:
            row = QVBoxLayout(); rh = QHBoxLayout()
            rh.addWidget(QLabel(name, font=QFont("", 9, QFont.Bold)))
            btn_c = QPushButton(self.T["btn_color"]); btn_c.clicked.connect(lambda *a, k=c_key: self.p.pick_color(k)); rh.addWidget(btn_c)
            row.addLayout(rh)
            self.add_slider(row, self.T["slider_hand_len"], 10, 100, self.p.settings[prefix+'_hand_len'],
                            lambda v, p=prefix: self.p.update_hand_len(p, v), "%")
            self.add_slider(row, self.T["slider_hand_width"], 1, 15, self.p.settings[prefix+'_hand_width'],
                            lambda v, p=prefix: self.p.update_setting(p+'_hand_width', v), "px")
            vh.addLayout(row)
        layout.addWidget(g_hands)

        # タイマー表示
        g_timer_main = QGroupBox(self.T["group_timer"]); tl_main = QVBoxLayout(g_timer_main)
        style_group(g_timer_main, "#3a1a1a", "#9a2a2a")  # 赤系
        modes = [
            ("h", self.T["lbl_mode_h"], "radius_h"),
            ("m", self.T["lbl_mode_m"], "radius_m"),
            ("s", self.T["lbl_mode_s"], "radius_s"),
        ]
        for mid, mname, rkey in modes:
            rh = QHBoxLayout()
            rh.addWidget(QLabel(mname, font=QFont("", 9, QFont.Bold)))
            # 色設定ボタン（色段階ダイアログを開く）
            btn_cs = QPushButton(self.T["btn_color_settings"])
            btn_cs.clicked.connect(lambda *a, m=mid: self._open_color_stages(m))
            rh.addWidget(btn_cs)
            tl_main.addLayout(rh)
            self.add_slider(tl_main, self.T["slider_radius"], 10, 100, self.p.settings[rkey],
                            lambda v, k=rkey: self.p.update_setting(k, v), "%")
            tl_main.addSpacing(10)

        rh_r = QHBoxLayout()
        rh_r.addWidget(QLabel(self.T["lbl_ring"], font=QFont("", 9, QFont.Bold)))
        btn_rc = QPushButton(self.T["btn_color"]); btn_rc.clicked.connect(lambda: self.p.pick_color("color_ring")); rh_r.addWidget(btn_rc)
        tl_main.addLayout(rh_r)
        self.add_slider(tl_main, self.T["slider_ring_width"], 1, 25, self.p.settings['ring_width'],
                        lambda v: self.p.update_setting('ring_width', v), "%")
        tl_main.addSpacing(10)

        rh_flash = QHBoxLayout()
        rh_flash.addWidget(QLabel(self.T["lbl_flash"], font=QFont("", 9, QFont.Bold)))
        btn_fc = QPushButton(self.T["btn_color"]); btn_fc.clicked.connect(lambda: self.p.pick_color("color_finish")); rh_flash.addWidget(btn_fc)
        tl_main.addLayout(rh_flash)
        self.add_slider(tl_main, self.T["slider_flash_interval"], 1, 30, int(self.p.settings['finish_flash_interval']*10),
                        lambda v: self.p.update_setting('finish_flash_interval', v/10.0), is_float=True, unit="秒" if lang == "ja" else "sec")
        layout.addWidget(g_timer_main)

        # バージョン情報
        layout.addSpacing(10)
        ver_frame = QFrame(); ver_frame.setFrameShape(QFrame.HLine); ver_frame.setFrameShadow(QFrame.Sunken)
        layout.addWidget(ver_frame)
        lbl_ver = QLabel("SectorTimerClock v1.25")
        lbl_ver.setAlignment(Qt.AlignCenter)
        lbl_ver.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(lbl_ver)
        lbl_link = QLabel('<a href="https://github.com/adEGeD3Lf/SectorTimerClock/releases" style="color:#6699cc;">https://github.com/adEGeD3Lf/SectorTimerClock/releases</a>')
        lbl_link.setAlignment(Qt.AlignCenter)
        lbl_link.setOpenExternalLinks(True)
        lbl_link.setStyleSheet("font-size: 10px;")
        layout.addWidget(lbl_link)
        layout.addSpacing(5)

        scroll.setWidget(content)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)
        b_close = QPushButton(self.T["btn_close"]); b_close.clicked.connect(self.close)
        main_layout.addWidget(b_close)

        content.adjustSize()
        content_w = content.sizeHint().width()
        from PySide6.QtWidgets import QStyle
        scrollbar_w = self.style().pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)
        margin = 30
        self.resize(content_w + scrollbar_w + margin, 850)
        smart_move(self, self.p)

    def _open_color_stages(self, mode):
        key = f"wedge_stages_{mode}"
        stages = self.p.settings.get(key, DEFAULT_COLOR_STAGES[key])
        dlg = ColorStagesDialog(self.p, mode, stages)
        dlg.exec()

    def add_slider(self, layout, label, min_v, max_v, init_v, func, unit="", is_float=False):
        row_layout = QHBoxLayout()
        lbl = QLabel(label); lbl.setFixedWidth(120); row_layout.addWidget(lbl)
        row_layout.addSpacing(10)
        s = QSlider(Qt.Horizontal); s.setRange(min_v, max_v); s.setValue(init_v); s.setMinimumWidth(150)
        val_lbl = QLabel(); val_lbl.setFixedWidth(60)
        def update_val(v):
            real_v = v/10.0 if is_float else v
            func(v); val_lbl.setText(f"{real_v}{unit}")
        update_val(init_v); s.valueChanged.connect(update_val)
        row_layout.addWidget(s); row_layout.addWidget(val_lbl)
        layout.addLayout(row_layout)


class SectorTimerClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = {
            "diameter": 127, "opacity": 0.7, "always_on_top": True, "smooth_second": False,
            "color_bg": "#0d0d0d", "color_text": "#dcdcdc", "color_date": "#dcdcdc",
            "color_hour_hand": "#8080ff", "color_minute_hand": "#ff8080", "color_second_hand": "#ffffff",
            "color_finish": "#ff0000",
            "color_ring": "#996633", "ring_width": 5, "date_format_idx": 1, "date_opacity": 1.0, "date_show": True,
            "h_hand_len": 70, "h_hand_width": 9, "m_hand_len": 95, "m_hand_width": 6, "s_hand_len": 95, "s_hand_width": 2,
            "radius_h": 70, "radius_m": 95, "radius_s": 95, "finish_flash_interval": 1.0,
            "font_main": ["Arial", 20, True], "font_date": ["Arial", 20, True],
            "number_radius": 79, "date_radius": -20, "hand_opacity": 1.0,
            "mark5": {"color": "#ffffff", "width": 3.0, "len": 5},
            "mark1": {"color": "#ffffff", "width": 1.5, "len": 4},
            "history_duration": ["00:00:10", "00:03:00", "00:05:00", "00:25:00", "00:60:00", "01:30:00"],
            "history_time": ["12:00:00", "15:00:00", "17:30:00"],
            "last_duration_val": "00:01:00", "last_time_val": "15:00:00",
            "favorites": [
                {"type": "time",     "value": "12:00:00", "label": "時刻12:00:00"},
                {"type": "duration", "value": "00:05:00", "label": "残り00:05:00"},
                {"type": "duration", "value": "00:25:00", "label": "残り00:25:00"},
                {"type": "sequence", "seq_name": "pomodoro", "label": "シーケンスpomodoro"},
            ],
            "window_pos": None, "save_window_pos": True,
            "language": "ja",
            "sequences": [
                {
                    "name": "pomodoro",
                    "steps": [
                        {"type": "duration", "value": "00:25:00"},
                        {"type": "duration", "value": "00:05:00"},
                        {"type": "duration", "value": "00:25:00"},
                        {"type": "duration", "value": "00:05:00"},
                        {"type": "duration", "value": "00:25:00"},
                        {"type": "duration", "value": "00:05:00"},
                        {"type": "duration", "value": "00:25:00"},
                    ],
                },
                {
                    "name": "every90min",
                    "steps": [
                        {"type": "time", "value": "09:00:00"},
                        {"type": "time", "value": "10:30:00"},
                        {"type": "time", "value": "12:00:00"},
                        {"type": "time", "value": "13:00:00"},
                        {"type": "time", "value": "14:30:00"},
                        {"type": "time", "value": "16:00:00"},
                        {"type": "time", "value": "17:30:00"},
                    ],
                },
            ],
            "wedge_stages_h": [
                {"threshold": 7200, "color": "#0056d8"},
                {"threshold": 3600, "color": "#007ec7"},
            ],
            "wedge_stages_m": [
                {"threshold": 3600, "color": "#005555"},
                {"threshold": 2700, "color": "#005a00"},
                {"threshold": 1800, "color": "#486400"},
                {"threshold": 900,  "color": "#969600"},
                {"threshold": 300,  "color": "#c86700"},
            ],
            "wedge_stages_s": [
                {"threshold": 60, "color": "#820000"},
                {"threshold": 10, "color": "#960096"},
            ],
        }
        self.load_settings()
        self._cleanup_orphan_seq_favs()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.update_window_flags()
        self.setFixedSize(self.settings["diameter"], self.settings["diameter"])
        self.restore_position()
        self.target_time = None; self.timer_finished = False; self.drag_pos = QPoint()
        # シーケンスタイマー状態
        self.seq_remaining = []      # 残りステップ（リスト）
        self.seq_flashing = False    # シーケンス中のステップ終了点滅フラグ
        self.current_seq_steps = []  # ダイアログ編集用の現在のステップ一覧
        self.timer = QTimer(self); self.timer.timeout.connect(self.update); self.timer.start(50)

    def T(self, key):
        lang = self.settings.get("language", "ja")
        return LANG[lang].get(key, key)

    def _fav_display_label(self, fav):
        """言語に応じたお気に入りの表示ラベルを生成"""
        if fav["type"] == "duration":
            return f"{self.T('fav_prefix_duration')}{fav['value']}"
        elif fav["type"] == "time":
            return f"{self.T('fav_prefix_time')}{fav['value']}"
        elif fav["type"] == "sequence":
            return f"{self.T('fav_prefix_seq')}{fav['seq_name']}"
        return fav.get("label", "")

    def _cleanup_orphan_seq_favs(self):
        """保存済みシーケンスに存在しないシーケンスがお気に入りにあれば削除し通知する"""
        saved_names = {s["name"] for s in self.settings.get("sequences", [])}
        favs = self.settings.get("favorites", [])
        orphans = [f for f in favs if f.get("type") == "sequence" and f.get("seq_name") not in saved_names]
        if not orphans: return
        self.settings["favorites"] = [f for f in favs if f not in orphans]
        self.save_settings()
        lang = self.settings.get("language", "ja")
        QMessageBox.information(None, "", LANG[lang]["orphan_seq_msg"])

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                default_favs = self.settings["favorites"]
                self.settings.update(loaded)
                if "favorites" not in loaded:
                    self.settings["favorites"] = default_favs
                # 旧設定からの移行: color_wedge_* が残っていても wedge_stages_* が無ければデフォルト補完
                for mode in ("h", "m", "s"):
                    key = f"wedge_stages_{mode}"
                    if key not in self.settings:
                        self.settings[key] = [dict(s) for s in DEFAULT_COLOR_STAGES[key]]
            except Exception as e:
                print(f"[SectorTimerClock] load_settings failed: {e}")

    def restore_position(self):
        if not self.settings.get("save_window_pos", True): return
        pos = self.settings.get("window_pos")
        if pos:
            p = QPoint(pos[0], pos[1]); d = self.settings["diameter"]
            on_screen = any(s.availableGeometry().contains(p) for s in QApplication.screens())
            if on_screen:
                self.move(p)
            else:
                r = QApplication.primaryScreen().availableGeometry()
                self.move(r.center().x() - d // 2, r.center().y() - d // 2)

    def save_settings(self):
        tmp = SETTINGS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)
        os.replace(tmp, SETTINGS_FILE)

    def update_setting(self, k, v, is_opacity=False):
        self.settings[k] = v; self.save_settings(); self.update()

    def update_mark_setting(self, k1, k2, v):
        self.settings[k1][k2] = v; self.save_settings(); self.update()

    def update_hand_len(self, p, v):
        if p == 'h' and v >= self.settings['m_hand_len']: v = self.settings['m_hand_len'] - 1
        if p == 'm' and v <= self.settings['h_hand_len']: v = self.settings['h_hand_len'] + 1
        self.settings[p+'_hand_len'] = v; self.save_settings(); self.update()

    def set_diameter_live(self, v):
        self.settings["diameter"] = v; self.setFixedSize(v, v); self.save_settings()

    def _confirm_interrupt_sequence(self):
        """シーケンス実行中なら中断確認ダイアログを出す。中断OKならTrue、キャンセルならFalse"""
        if not self.seq_remaining and not self.seq_flashing:
            return True  # シーケンス未実行なので確認不要
        dlg = QMessageBox(self)
        dlg.setWindowTitle("")
        dlg.setText(self.T("seq_interrupt_msg"))
        btn_ok = dlg.addButton(self.T("seq_interrupt_ok"), QMessageBox.AcceptRole)
        dlg.addButton(self.T("seq_interrupt_cancel"), QMessageBox.RejectRole)
        dlg.exec()
        if dlg.clickedButton() == btn_ok:
            self.seq_remaining = []; self.seq_flashing = False
            return True
        return False

    def set_timer_direct(self, target):
        if not self._confirm_interrupt_sequence(): return
        self.target_time = target; self.timer_finished = False; self.save_settings(); self.update()

    def reset_timer(self):
        self.target_time = None; self.timer_finished = False
        self.seq_remaining = []; self.seq_flashing = False
        self.update()

    def start_sequence(self, steps, start_idx=0):
        """シーケンスをstart_idxから開始する"""
        if not self._confirm_interrupt_sequence(): return
        remaining = steps[start_idx:]
        if not remaining: return
        self.seq_remaining = [dict(s) for s in remaining[1:]]
        self._activate_step(remaining[0])

    def _activate_step(self, step):
        """ステップを実際のtarget_timeに変換してセット"""
        now = datetime.now().replace(microsecond=0)
        if step["type"] == "duration":
            parts = list(map(int, step["value"].split(":")))
            h, m, s = parts[0], parts[1], parts[2]
            target = now + timedelta(hours=h, minutes=m, seconds=s)
        else:
            parts = list(map(int, step["value"].split(":")))
            h, m, s = parts[0], parts[1], parts[2]
            target = now.replace(hour=h % 24, minute=m % 60, second=s % 60, microsecond=0)
            if target <= now: target += timedelta(days=1)
        self.target_time = target
        self.timer_finished = False
        self.seq_flashing = False
        self.update()

    def toggle_date_pos(self):
        r = self.settings["date_radius"]
        self.settings["date_radius"] = -r if r != 0 else 20
        self.save_settings(); self.update()

    def sort_all_history(self):
        def to_sec(s):
            p = list(map(int, re.findall(r'\d+', s)))
            return p[0]*3600 + p[1]*60 + p[2] if len(p) == 3 else p[0]*60
        self.settings["history_duration"] = sorted(list(set(self.settings["history_duration"])), key=to_sec)[:20]
        self.settings["history_time"] = sorted(list(set(self.settings["history_time"])), key=to_sec)[:20]

    def update_history(self, key, val):
        self.settings[key].append(val); self.sort_all_history(); self.save_settings()

    def update_window_flags(self):
        flags = Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint | Qt.Tool
        if self.settings["always_on_top"]: flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags); self.show()

    def toggle_smooth(self, c):
        self.settings["smooth_second"] = c; self.save_settings()

    def toggle_ontop(self, c):
        self.settings["always_on_top"] = c; self.update_window_flags(); self.save_settings()

    def set_date_format(self, i):
        self.settings["date_format_idx"] = i; self.save_settings()

    def set_language(self, lang):
        self.settings["language"] = lang; self.save_settings()

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        side = self.settings["diameter"]; p.translate(side/2, side/2); p.scale(side/200.0, side/200.0)
        p.setOpacity(self.settings.get("opacity", 1.0))
        p.setPen(Qt.NoPen); p.setBrush(QColor(self.settings["color_bg"])); p.drawEllipse(-100, -100, 200, 200)
        if self.target_time and not self.timer_finished:
            rw = self.settings["ring_width"]; p.setPen(QPen(QColor(self.settings["color_ring"]), rw))
            p.setBrush(Qt.NoBrush); p.drawEllipse(-100 + rw/2, -100 + rw/2, 200 - rw, 200 - rw); p.setPen(Qt.NoPen)
        self.draw_timer_logic(p); self.draw_marks(p); self.draw_numbers(p); self.draw_hands(p); self.draw_date(p)

    def draw_timer_logic(self, p):
        if not self.target_time: return
        now = datetime.now(); ref_now = now if self.settings["smooth_second"] else now.replace(microsecond=0)
        rem = (self.target_time - ref_now).total_seconds()

        if rem <= 0 and not self.timer_finished and not self.seq_flashing:
            # ステップ終了
            if self.seq_remaining:
                # 次ステップを裏でセット → seq_flashingを立てて点滅開始
                next_step = self.seq_remaining.pop(0)
                self._activate_step(next_step)   # target_time を次ステップに更新
                self.seq_flashing = True          # 点滅フラグON（_activate_stepのFalseを上書き）
                rem = (self.target_time - ref_now).total_seconds()
            else:
                self.timer_finished = True

        # シーケンス中の点滅（裏で次タイマーは動いている）
        if self.seq_flashing:
            interval = self.settings.get('finish_flash_interval', 1.0)
            t = now.timestamp() * (2 * math.pi / max(0.01, interval)); pulse = math.sin(t)
            p.setBrush(QColor(self.settings["color_finish"])); p.setOpacity(max(0, pulse))
            p.drawEllipse(-100, -100, 200, 200); p.setOpacity(1.0); return

        # 全ステップ終了後の点滅
        if self.timer_finished:
            interval = self.settings.get('finish_flash_interval', 1.0)
            t = now.timestamp() * (2 * math.pi / max(0.01, interval)); pulse = math.sin(t)
            p.setBrush(QColor(self.settings["color_finish"])); p.setOpacity(max(0, pulse))
            p.drawEllipse(-100, -100, 200, 200); p.setOpacity(1.0); return

        if rem <= 0: return

        if rem > 3600:
            r = self.settings["radius_h"]
            stages = self.settings.get("wedge_stages_h", DEFAULT_COLOR_STAGES["wedge_stages_h"])
            color = get_wedge_color(stages, rem)
            scale = 12*3600.0
            target_v = (self.target_time.hour%12)*3600 + self.target_time.minute*60 + self.target_time.second
        elif rem > 60:
            r = self.settings["radius_m"]
            stages = self.settings.get("wedge_stages_m", DEFAULT_COLOR_STAGES["wedge_stages_m"])
            color = get_wedge_color(stages, rem)
            scale = 3600.0
            target_v = self.target_time.minute*60 + self.target_time.second
        else:
            r = self.settings["radius_s"]
            stages = self.settings.get("wedge_stages_s", DEFAULT_COLOR_STAGES["wedge_stages_s"])
            color = get_wedge_color(stages, rem)
            scale = 60.0
            target_v = self.target_time.second

        p.setBrush(QColor(color))
        target_a = (90 - (target_v / scale * 360.0)) * 16
        span = (rem / scale * 360.0) * 16
        p.drawPie(QRectF(-r, -r, r*2, r*2), int(target_a), int(span))

    def draw_date(self, p):
        if not self.settings["date_show"]: return
        p.setOpacity(self.settings.get("opacity", 1.0) * self.settings["date_opacity"])
        now = datetime.now()
        lang = self.settings.get("language", "ja")
        idx = self.settings["date_format_idx"]
        fmt = format_date_string(lang, idx, now)
        p.setFont(QFont(self.settings["font_date"][0], self.settings["font_date"][1],
                        QFont.Bold if self.settings["font_date"][2] else QFont.Normal))
        p.setPen(QPen(QColor(self.settings["color_date"])))
        p.drawText(QRectF(-90, self.settings["date_radius"]-22, 180, 45), Qt.AlignCenter, fmt)
        p.setOpacity(1.0)

    def draw_marks(self, p):
        p.save()
        for i in range(60):
            c = self.settings["mark5"] if i % 5 == 0 else self.settings["mark1"]
            p.setPen(QPen(QColor(c["color"]), c["width"]))
            p.drawLine(100 - c["len"], 0, 100, 0); p.rotate(6.0)
        p.restore()

    def draw_numbers(self, p):
        f = self.settings["font_main"]
        font = QFont(f[0], f[1], QFont.Bold if f[2] else QFont.Normal)
        p.setFont(font); p.setPen(QColor(self.settings["color_text"]))
        r = self.settings["number_radius"]
        scale = self.settings["diameter"] / 200.0
        fm = p.fontMetrics()
        font_size = f[1]
        inward_offset = font_size * 0.15
        for i in range(1, 13):
            ang = math.radians(i * 30 - 90); tx, ty = math.cos(ang) * r, math.sin(ang) * r
            text = str(i)
            br = fm.boundingRect(text)
            w = br.width() / scale; h = br.height() / scale
            if i in (10, 11):
                tx -= math.cos(ang) * inward_offset
                ty -= math.sin(ang) * inward_offset
            p.drawText(QRectF(tx - w/2, ty - h/2, w, h), Qt.AlignCenter, text)

    def draw_hands(self, p):
        hand_opacity = self.settings.get("hand_opacity", 1.0) * self.settings.get("opacity", 1.0)
        t = datetime.now(); ref_t = t if self.settings["smooth_second"] else t.replace(microsecond=0)
        sec = ref_t.second + (ref_t.microsecond/1000000.0 if self.settings["smooth_second"] else 0)
        p.save(); p.setOpacity(hand_opacity); p.rotate(30.0*(ref_t.hour%12 + ref_t.minute/60.0 + ref_t.second/3600.0))
        p.setBrush(QColor(self.settings["color_hour_hand"])); p.setPen(Qt.NoPen)
        L, W = self.settings["h_hand_len"], self.settings["h_hand_width"]
        p.drawConvexPolygon(QPolygon([QPoint(-W//2, 8), QPoint(W//2, 8), QPoint(W//2, -L+10), QPoint(0, -L), QPoint(-W//2, -L+10)]))
        p.restore()
        p.save(); p.setOpacity(hand_opacity); p.rotate(6.0*(ref_t.minute + ref_t.second/60.0))
        p.setBrush(QColor(self.settings["color_minute_hand"])); p.setPen(Qt.NoPen)
        L, W = self.settings["m_hand_len"], self.settings["m_hand_width"]
        p.drawConvexPolygon(QPolygon([QPoint(-W//2, 8), QPoint(W//2, 8), QPoint(W//2, -L+10), QPoint(0, -L), QPoint(-W//2, -L+10)]))
        p.restore()
        p.save(); p.setOpacity(hand_opacity); p.rotate(6.0*sec)
        p.setPen(QPen(QColor(self.settings["color_second_hand"]), self.settings["s_hand_width"]))
        p.drawLine(0, 15, 0, -self.settings["s_hand_len"]); p.restore()

    def contextMenuEvent(self, event):
        m = QMenu(self)
        m.addAction(self.T("menu_timer_reset"), self.reset_timer)
        m.addAction(self.T("menu_timer_set"), lambda: TimerInputDialog(self).exec())

        for fav in self.settings.get("favorites", []):
            label = "\u3000" + self._fav_display_label(fav)
            m.addAction(label, lambda f=fav: self.start_favorite(f))

        m.addAction(self.T("menu_date_flip"), self.toggle_date_pos)

        lang_menu = QMenu(self.T("menu_language"), self)
        lang_menu.addAction(self.T("menu_lang_ja"), lambda: self.set_language("ja"))
        lang_menu.addAction(self.T("menu_lang_en"), lambda: self.set_language("en"))
        m.addMenu(lang_menu)

        m.addSeparator()
        m.addAction(self.T("menu_settings"), lambda: SettingsDialog(self).exec())
        m.addAction(self.T("menu_quit"), QApplication.quit)
        m.exec(event.globalPos())

    def start_favorite(self, fav):
        if fav["type"] == "duration":
            h, m, s = map(int, fav["value"].split(":"))
            self.set_timer_direct(datetime.now().replace(microsecond=0) + timedelta(hours=h, minutes=m, seconds=s))
        elif fav["type"] == "time":
            parts = list(map(int, fav["value"].split(":")))
            h, m, s = parts[0], parts[1], parts[2]
            now = datetime.now().replace(microsecond=0)
            target = now.replace(hour=h % 24, minute=m % 60, second=s % 60, microsecond=0)
            if target <= now: target += timedelta(days=1)
            self.set_timer_direct(target)
        elif fav["type"] == "sequence":
            seq_name = fav.get("seq_name", "")
            seq = next((s for s in self.settings.get("sequences", []) if s["name"] == seq_name), None)
            if seq:
                self.start_sequence(seq["steps"], 0)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.timer_finished:
                self.reset_timer()
            elif self.seq_flashing:
                # 点滅解除 → 裏で動いていた次タイマーの表示に切り替え
                self.seq_flashing = False
                self.update()
            else:
                self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton: self.reset_timer()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and not self.timer_finished and not self.seq_flashing:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and not self.timer_finished and not self.seq_flashing \
                and self.settings.get("save_window_pos", True):
            self.settings["window_pos"] = [self.x(), self.y()]; self.save_settings()

    def pick_color(self, k):
        c = QColorDialog.getColor(QColor(self.settings[k]), self)
        if c.isValid(): self.settings[k] = c.name(); self.update(); self.save_settings()

    def pick_font(self, k):
        cur = QFont(self.settings[k][0], self.settings[k][1]); ok, f = QFontDialog.getFont(cur, self)
        if ok: self.settings[k] = [f.family(), f.pointSize(), f.bold()]; self.update(); self.save_settings()

    def set_mark_color(self, k):
        c = QColorDialog.getColor(QColor(self.settings[k]["color"]), self)
        if c.isValid(): self.settings[k]["color"] = c.name(); self.update(); self.save_settings()


if __name__ == "__main__":
    app = QApplication(sys.argv); app.setStyle("Fusion")
    clock = SectorTimerClockApp(); sys.exit(app.exec())