# shiftbase-ops

Operasional [Shiftbase](https://github.com/RakhaYandra/shiftbase): runbook
compose, skrip backup/restore MySQL teruji roundtrip, troubleshooting matrix
15 entri terverifikasi (termasuk port bentrok asli + distroless tanpa shell),
10 tiket + XLSX, SLA mini, FAQ.

## Isi

```
RUNBOOK.md, TROUBLESHOOTING.md, SLA.md, FAQ.md
scripts/shiftbase-backup.sh (mysqldump+gzip+rotasi, kredensial env)
scripts/shiftbase-restore.sh (konfirmasi tulis-ulang)
tickets.yaml -> tools/build_tickets.py -> Shiftbase-Tickets.xlsx
```

## Bukti uji

* Roundtrip: backup → hapus employees → restore → 5 employees + 3 users
* Compose full stack Up di port override (api 200, adminer 200, mysql healthy)
* `exec sh` di api gagal sesuai desain distroless; check-in ganda 409; seed ganda 1062
