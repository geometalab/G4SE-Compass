# Funktional
* F�r Keyword sollten �bersetzungen vorhanden sein, so m�ssen nocht gesamte Datens�tze �bersetzt werden. Bei der Suche kann die Sprache gesetzt werden
* F�r jede Sprache wird in Postgres ein tsvector erstellt, welcher das entsprechende Keywords Feld ber�cksichtigt. Nur der tsvector der gesetzten Metadatensprache ber�cksichtigt weitere Felder. 