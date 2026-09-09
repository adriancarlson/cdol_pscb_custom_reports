# CDOL PSCB Custom Reports

## Installing the custom EUI menu links

To display the custom report links in PowerSchool:

1. Download the latest version of **PSCB DEV Pro Reports - EUI Menu Links** from [PSCB Development](https://pscbdevelopment.com/powerschool-plugin/pscb-pro-eui-menu-links/).
2. Unzip the downloaded plugin.
3. Copy `cdol-custom-pscb-report-navigation.json` from this repository into the plugin's `pagecataloging` folder.
4. Rezip the plugin without incrementing its plugin version.
5. Reinstall the repackaged **PSCB DEV Pro Reports - EUI Menu Links** plugin in PowerSchool.

## Missed Daily Administration

Version `26.9.0.0` adds **Missed Daily Administration** under **Health Office > CDOL Medication**.
Version `26.9.0.1` runs the report immediately, removes the top filters, groups and shades rows by
student, sorts each student's missed dates newest first, and moves the Administration link to the student number.
The classic Health Office menu also includes the report. Both links are school-only, and opening
the report directly at District Office displays a school-selection message without running its queries.

The report follows the CDOL Health Log missed-administration counter: one row per unresolved daily
medication/date in the selected school and school year. It runs on page load without date or student-selection
parameters. It uses in-session weekdays, current and historical enrollment, dates strictly after first
inventory, and the school's daily cutoff. Effective Given and documented Not Given resolve a date;
corrections, entered-in-error records, and Not Given-to-Given conversions follow the existing student
Administration page. No remaining-inventory filter is applied. A missing cutoff displays a setup warning.

Student numbers open Medication Administration; student names are plain text. Copy, TSV, CSV, XLSX,
Print, table filtering, and current-selection tools use the PSCB framework described below.
Rows sort by student name, then student ID to keep students with identical names separate, then missed
date descending. Alternating row colors change by student number, not date. Multiple missed dates or
medications can produce several rows for one student; compare distinct students with the header count.

The report requires the CDOL Health Log daily-administration schema. The report plugin does not
install or modify that schema, the header counter, medication records, or school settings.
The EUI navigation JSON remains excluded from this plugin's ZIP; update the menu-links plugin using
the steps above to install the new enhanced-navigation entry.

Local SQL checks use fictional data and SQLite with Oracle date-function substitutes, not a live
Oracle or PowerSchool server. After installing, verify school/district visibility, cutoff warnings,
automatic loading, student grouping and shading, newest-first dates within each student, student-number
links, export tools, and agreement with student Administration pages.

## Health report frameworks

Version `26.9.0.3` retains PSCB framework 2 only for `cdol_missed_daily_administration.html`.
The other 13 health reports, including Medication Inventory List, Medication Inventory by Student,
and Medication Administration List, are restored to their pre-migration `26.9.0.1` report contents
and legacy PSCB framework. Their original filters, tables, formatting, links, and query logic are restored.

Missed Daily Administration continues to use `pscbdevpro2_init`, the same PSCB framework used by the
LanSchool reports. It runs immediately at the school level without a filter form, groups and shades
rows by student, sorts missed dates newest first within each student, and links the student number
to Medication Administration. The framework supplies per-column filters, sorting, Analyzer, Copy,
TSV, CSV, XLSX, Print, and Make Current Student Selection where permitted by PSCB settings.

Version `26.9.0.4` removes the added shared JavaScript and regression-test files. The missed-administration
report now contains only its required formatting and sorting code inline, with no added script-file dependency.
The installed PSCB Base Module must still provide its standard wildcard and Tabulator assets; those shared
PSCB files are not bundled here. No medication, health-log, or school-setting records are changed.

Before production use, test the installed reports in PowerSchool, including long notes, empty results,
report filters, student selection, exports, and the school-only missed-administration report. Local
JavaScript and fictional-data browser checks do not validate Oracle execution or PSCB permissions.

## NCEA baptisms and reception into full communion

Version `26.9.1` adds **NCEA - Baptisms and Reception into Full Communion** to the classic
and enhanced NCEA menus. It uses PSCB framework 2, matching the LanSchool reports, and
loads immediately with a distinct-student total and the supplied student detail columns.
The total covers the complete result, independent of table filters.

The selected PowerSchool year (`~(curyearid) + 1990` / `+ 1991`) supplies the August 1
inclusive and June 1 exclusive boundaries. Select 2025-2026 to report August 1, 2025,
through May 31, 2026. School context limits results to that school; District Office
includes all schools. The supplied joins and school/grade-descending/name ordering are retained.
No active-enrollment or NCEA-exclusion filter is added to the supplied criteria.

This query uses only `u_student_sacramental.student_baptism_date`. It cannot independently
identify reception into full communion or distinguish Catholic from other baptisms.
Confirm how those events are recorded before using the total for submission. First Communion
and Confirmation dates are not queried. Current student grade and school are shown.

Install the report plugin and update the separate EUI menu-links plugin as described above.
Live PowerSchool validation is still required for Oracle execution, PSCB tools, counts, and exports.
