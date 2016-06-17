# Funktional
* Für Keyword sollten Übersetzungen vorhanden sein, so müssen nocht gesamte Datensätze übersetzt werden. Bei der Suche kann die Sprache gesetzt werden
* Für jede Sprache wird in Postgres ein tsvector erstellt, welcher das entsprechende Keywords Feld berücksichtigt. Nur der tsvector der gesetzten Metadatensprache berücksichtigt weitere Felder. 