# Runbook — Shiftbase (API Go + MySQL + Web via Compose)

Cakupan: compose lifecycle, konfigurasi, backup/restore, migrate/seed,
rebuild, adminer, secret. Path relatif; contoh dari direktori `shiftbase/`.

## 1. Install & jalan pertama

```bash
cp .env.example .env            # isi JWT_SECRET prod yang kuat
docker compose up --build -d    # mysql :3306, api :8080, adminer :8082
go install github.com/pressly/goose/v3/cmd/goose@v3.28.0
goose -dir migrations mysql "shift:shiftpass@tcp(localhost:3306)/shiftbase?parseTime=true" up
mysql -h127.0.0.1 -ushift -pshiftpass shiftbase < seed/seed.sql
curl -s localhost:8080/healthz # {"status":"ok"}
```

Login seed: `admin / Admin123!`, `manager / Manager123!`, `staff / Staff123!`
(`@shiftbase.local`). Web: `../shiftbase-web` → `npm run dev` (`:5173`).

## 2. Operasi harian

| Tugas | Perintah |
|---|---|
| Status service | `docker compose ps` (mysql `healthy`) |
| Cek sehat | `curl -s localhost:8080/healthz` |
| Log API | `docker compose logs -f api` (catatan: distroless = TANPA shell; debug via log + adminer, bukan `exec sh`) |
| Backup | `../shiftbase-ops/scripts/shiftbase-backup.sh ./backups 7` |
| Restore | `./shiftbase-ops/scripts/shiftbase-restore.sh backups/shiftbase-<TS>.sql.gz` (konfirmasi dulu) |
| Migrate | `goose -dir migrations mysql "$DB_DSN" up` |
| Rebuild API | `docker compose up --build -d api` |
| DB GUI | adminer `localhost:8082` (server `mysql`, user `shift`) |

## 3. Checklist gagal login

1. `docker compose ps` — mysql healthy? api running?
2. `FRONTEND_URL` = origin browser persis (default `:5173`)?
3. Kredensial seed benar?
4. Secret dirotasi? → semua token hangus, login ulang.

## 4. Retensi & keamanan

* Backup harian mysqldump+gzip, simpan 7. Dump berisi data pribadi —
  JANGAN commit, JANGAN kirim mentah.
* `JWT_SECRET` prod ≥ 32 char acak. `.env` tak di-commit (sudah gitignore).
