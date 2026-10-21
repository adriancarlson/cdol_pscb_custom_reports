"""Execute shipped dose/report expressions against fictional SQLite rows.

SQLite substitutes for Oracle for these checks. Live Oracle and installed
PowerSchool authorization remain test-server acceptance steps.
"""
import re
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'WEB_ROOT/admin/reports_pscb_dev_pro/health'


class VariableDoseReportsTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.create_function('NVL', 2, lambda left, right: right if left is None else left)
        self.db.create_function('TO_CHAR', 1, lambda value: None if value is None else str(value))
        self.db.executescript('''
            CREATE TABLE u_student_med_inv_txn (
                id INTEGER, u_student_medication_id INTEGER, transaction_type TEXT,
                reversal_of_transaction_id INTEGER, event_date TEXT, event_time INTEGER,
                users_dcid INTEGER, notes TEXT, medication_name TEXT, dose_amount REAL,
                variable_dose INTEGER, dose_unit TEXT, inventory_unit TEXT, route TEXT,
                frequency TEXT, administration_quantity REAL, quantity_change REAL,
                correction_date TEXT, correction_time INTEGER, correction_users_dcid INTEGER,
                correction_reason TEXT
            );
            CREATE TABLE u_student_medication (id INTEGER, dose_amount REAL, variable_dose INTEGER);
        ''')

    def insert(self, **overrides):
        row = dict(id=1, u_student_medication_id=7, transaction_type='ADMINISTRATION',
                   event_date='2026-10-01', dose_amount=99, administration_quantity=4, quantity_change=-4)
        row.update(overrides)
        self.db.execute(f"INSERT INTO u_student_med_inv_txn ({','.join(row)}) VALUES ({','.join('?' for _ in row)})", tuple(row.values()))

    def effective_dose(self):
        source = (REPORTS / 'cdol_medication_administration.html').read_text()
        ctes = source[source.index('WITH correction_rows AS ('):source.index('SELECT\n                        students.dcid AS dcid')]
        expression = re.search(r"CASE WHEN NVL\(medication.variable_dose, 0\) = 1 OR effective.variable_dose = 1[\s\S]*?END AS dose_amount", source).group()
        return self.db.execute(ctes + f'''SELECT {expression}, effective.administration_quantity
            FROM effective_administrations effective JOIN u_student_medication medication
            ON medication.id = effective.u_student_medication_id''').fetchone()

    def test_current_variable_setting_overrides_legacy_numeric_display(self):
        self.insert()
        self.db.execute('INSERT INTO u_student_medication VALUES (7, NULL, 1)')
        self.assertEqual(self.effective_dose(), ('Varies ·', 4))

    def test_corrected_variable_snapshot_does_not_fall_back_to_original_99(self):
        self.insert()
        self.insert(id=2, transaction_type='ADMINISTRATION_CORRECTION', reversal_of_transaction_id=1,
                    variable_dose=1, dose_amount=None, quantity_change=0)
        self.db.execute('INSERT INTO u_student_medication VALUES (7, 99, 0)')
        self.assertEqual(self.effective_dose(), ('Varies ·', 4))

    def test_current_variable_setting_overrides_even_a_fixed_correction(self):
        self.insert(variable_dose=1, dose_amount=None)
        self.insert(id=2, transaction_type='ADMINISTRATION_CORRECTION', reversal_of_transaction_id=1,
                    variable_dose=0, dose_amount=5, quantity_change=0)
        self.db.execute('INSERT INTO u_student_medication VALUES (7, NULL, 1)')
        self.assertEqual(self.effective_dose(), ('Varies ·', 4))

    def test_inventory_and_missed_report_expressions(self):
        for name in ('cdol_medication_inventory.html', 'cdol_missed_daily_administration.html'):
            source = (REPORTS / name).read_text()
            expression = re.search(r"CASE WHEN NVL\(medication.variable_dose, 0\) = 1[\s\S]*?END AS dose_amount", source).group()
            self.db.execute('DELETE FROM u_student_medication')
            self.db.executemany('INSERT INTO u_student_medication VALUES (?, ?, ?)', [(1, None, 1), (2, 99, None), (3, 2.5, 0)])
            actual = self.db.execute(f'SELECT {expression} FROM u_student_medication medication ORDER BY id').fetchall()
            self.assertEqual(actual, [('Varies ·',), ('99.0',), ('2.5',)])
            if 'missed' in name:
                scoped = source[source.index('WITH scoped_medications'):source.index('medication_start AS')]
                self.assertIn('medication.variable_dose', scoped)


if __name__ == '__main__':
    unittest.main()
