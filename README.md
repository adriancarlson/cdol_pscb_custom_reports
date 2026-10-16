# CDOL PSCB Custom Reports

## Previous Grade School

Version `26.10.0.8` adds **Previous Grade School** under **Student Data Verification**
in the classic and enhanced menus, using `pscbdevpro2_init` like Missed Daily Administration.
It loads immediately with one row per active student in the current school (all active students
at District Office). Columns are Student Number, Student Name, Gender, Grade Level, and
Previous Grade School. Student names open Enrollment History.

Previous schools come from `reenrollments`, joined to `schools` by school number. Every
record for the student's current school is excluded, including past enrollment there.
Other schools appear once each, newest enrollment first, with calendar-year ranges derived
from entry date through exit date minus one day (PowerSchool exit dates are exclusive).
Overlapping year ranges are combined; separate year ranges are retained for return visits
and listed oldest first within each school.
Each date range is followed by ` | ` and the grades recorded on its enrollment records,
for example `School Name (2017-2020 | K-3; 2022-2023 | 5-6)`.
Consecutive recorded grades are compressed into ranges; missing grades are not inferred
from dates. Separate grade sequences use commas, and separate attendance ranges use semicolons.
Null grades display `Grade not recorded`; negative grades display PK and zero displays K.
No grade-level restriction is applied to prior schools, matching the requested enrollment
history source. Zero-length, reversed, and future-start enrollments are excluded.
Missing school names display the school number; students without eligible history remain
in the report with `No previous school recorded`. External schools absent from enrollment
history cannot be inferred. The grouped cell is plain text for filtering and exports.
The Previous Grade School dropdown lists individual school names alphabetically and matches
students who attended the selected school regardless of their other schools, years, or grades.
It always includes `No previous school recorded` at the bottom and can be cleared to show all rows.
That placeholder is italicized in report rows; exports retain its plain text.

Update the separate EUI menu-links plugin as described below to install the enhanced link.
Live PowerSchool validation is required for Oracle execution, framework tools, exports, and
comparison with Enrollment History; the authenticated example page could not be accessed locally.

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

The report now uses the previous school year's full-year Terms record:
`terms.yearid = ~(curyearid) - 1`, `terms.isyearrec = 1`, and
`terms.schoolid = students.schoolid`. With 2026-2027 selected, it reports the
2025-2026 term. Baptism dates include `FIRSTDAY` through the entire `LASTDAY`;
the dates are no longer fixed to August 1 and May 31. School context limits results
to that school; District Office uses each student's current school's term dates.
A school without a matching prior-year term contributes no rows. The school-level
report displays the configured date range or a missing-term message. `EXISTS` avoids
duplicating students if matching term records overlap. The supplied joins and
school/grade-descending/name ordering are retained. This adjustment is packaged as
`26.9.0.1`, following the current repository manifest version `26.9.0.0`.
No active-enrollment or NCEA-exclusion filter is added to the supplied criteria.

This query uses only `u_student_sacramental.student_baptism_date`. It cannot independently
identify reception into full communion or distinguish Catholic from other baptisms.
Confirm how those events are recorded before using the total for submission. First Communion
and Confirmation dates are not queried. Current student grade and school are shown.

Install the report plugin and update the separate EUI menu-links plugin as described above.
Live PowerSchool validation is still required for Oracle execution, PSCB tools, counts, and exports.

## Grandparents List

Version `26.10.0.7` adds **Grandparents List** directly below **Family Rep** in the classic
and enhanced Contacts menus.
The report has one row per active contact with a current `Grandmother` or `Grandfather`
relationship to an active student. Columns are Contact Name, Relationship, Address, Email(s),
Phones, and Student(s). Contact names link to the contact record. All emails and phones
are included in their respective cells. Emails are separated by commas; phones are
separated by ` | `, with phone types following each number in parentheses. Missing addresses, emails, or phones display `-None-`.
Current contact addresses include street, city, state, ZIP, and address type. Multiple
current addresses share the Address cell, with each address on a separate line; future and expired addresses
are excluded.

Associated students appear as a bulleted list of linked names followed by grade and
school abbreviation, ordered by grade descending, then name. School context and the
All Students/Current Selection filter apply to both grandparent eligibility and the
student list. Duplicate current relationship records do not duplicate grandparents
or students. A contact with both grandparent relationship types still appears once,
with both types in the Relationship cell. Students associated only through another
relationship are excluded.

Install the report plugin and update the separate EUI menu-links plugin using the steps
above. The root navigation JSON places Grandparents List after Family Rep but remains
excluded from the report plugin ZIP. Copy the updated `cdol-custom-pscb-report-navigation.json`
into the separate EUI menu-links plugin's `pagecataloging` folder and reinstall that plugin
to update the enhanced menu.

HTML entity terminators in embedded SQL use `CHR(59)` because literal semicolons terminate
PowerSchool `tlist_sql` queries, even inside quoted strings.

Local checks do not establish live Oracle execution; verify shared grandparents,
multiple phones/emails, effective dates, selection, student links, and exports in PowerSchool.

## Alumni List

Version `26.10.0.15` adds Alumni List after Grandparents List in both Contacts menus,
using PSCB framework 2. Select Number of Contacts (1–6, default 4) and submit to run.
The report has no date-window filter.
Historical enrollment combines STUDENTS and REENROLLMENTS. A qualifying enrollment
matches SCHOOLS.HIGH_GRADE and overlaps the interval from full-year TERMS.LASTDAY minus
14 calendar days through LASTDAY, inclusive. Entry is inclusive and exit is exclusive.
Only completed full-year terms qualify. Students active at that historical school today
are excluded; students now active at another school can qualify. School context filters
historical school, not the student's currently assigned school. Class Year is the calendar
year of the qualifying term end. The latest qualifying class is used per student; at
District Office this means the most recent qualifying school across the district, with
school number breaking ties. Earlier withdrawals are excluded; withdrawals within the
final window can qualify because dates alone do not establish graduation.

Columns are Student Number, Student Name, Class Year, Student Address, and the selected number of contact
groups (Name, Relationship, Address, Emails, Phones). School abbreviation is the last
column only at District Office. Rows sort by Class Year descending, student name, and ID.
Student addresses combine home and mailing, showing labels only when both exist and differ
(case and whitespace are ignored for comparison). One address appears without a label.
Addresses and contact details are currently recorded values, not historical snapshots.

Contacts must be active with a currently effective student relationship. They are ranked
by contact priority, null priorities last, then person ID; only the first selected number appear (up to six).
Students without contacts remain included and unused contact groups stay blank. All current
contact addresses appear on separate lines with types, emails use commas, and phones use
pipes with types in parentheses. The report uses JSON CLOB output and text-node formatters.
The separate EUI menu-links plugin must be repackaged with the root navigation JSON;
no pagecataloging entry is bundled in this report plugin.

Local checks do not verify Oracle or installed PSCB behavior. After installation, validate
highest-grade settings, term dates, historical enrollment boundaries, school/district scope,
contact priority, empty results, multiline cells, and exports against known students.

Alumni List version `26.10.0.15` retains the pre-run contact count, dropdown filters,
and compact columns. The custom top scrollbar and its DOM/resize observers have been
removed. The filter form now matches the repository's Public School Districts and Student Car
Information reports: POST to #, hidden showData/ac fields, the standard submitbutton,
and the framework wildcard outside the results condition. PowerSchool markup restores
selected options and emits the validated contact count directly in the results script.
There is no pre-framework script, DOM-dependent count initialization, custom submit handler,
or URL navigation override.
The SQL remains inside the Submit condition. Compact, resizable columns preserve explicit
address line breaks without automatic wrapping; long values display an ellipsis with the
full value in a hover tooltip. Exports retain full cell values. Source-map 404s alone do not identify report initialization failures.
