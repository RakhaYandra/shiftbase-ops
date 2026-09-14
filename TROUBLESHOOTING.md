# Troubleshooting Matrix — Shiftbase

Tiap perintah **dijalankan beneran** (env: compose di port override
18093/18094/13309 agar tak bentrok live, atau MySQL scratch `:13308`).
Gejala → diagnosis → perintah → hasil sehat.

| # | Gejala | Diagnosis | Perintah | Sehat bila |
|---|---|---|---|---|
| 1 | `api` tak start / restart loop | Tergantung mysql belum healthy | `docker compose ps` (mysql `healthy`) + `docker compose logs -f api` | mysql healthy → api Up |
| 2 | `failed to bind host port 8080` | Port dipakai (insiden nyata: live lifeos) | `ss -ltnp \| grep 8080`; override `-f override.yml` (`!override` port) | Api Up di port lain |
| 3 | Login gagal browser | CORS origin ≠ FRONTEND_URL (default `:5173`) | Preflight `curl -D- -X OPTIONS` cek `Access-Control-Allow-Origin` | Origin browser terbalas |
| 4 | 401 massal | JWT_SECRET beda dengan saat token terbit | Samakan `JWT_SECRET` compose → `up -d api`, login ulang | Login 200 |
| 5 | `exec sh` gagal di api | Distroless TANPA shell (terverifikasi: `unable to start container process`) | Debug via `docker compose logs api` + adminer, JANGAN exec | Log terlihat |
| 6 | Migrasi gagal | DSN salah / mysql belum siap | `goose -dir migrations mysql "$DB_DSN" status`; tunggu healthy | version 5, 0 Pending |
| 7 | Seed error 1062 users | Seed 2x (terverifikasi: `Duplicate entry 'admin@...'`) | `SELECT COUNT(*) FROM users` = 3 → skip | Tak perlu aksi |
| 8 | CSV import 400 header | Header harus persis `name,email,phone,position,hire_date` | Cek baris 1 file | 200 + counts |
| 9 | CSV >2MB ditolak | Batas 2MB (by design) | `ls -la file.csv` | < 2MB atau pecah file |
| 10 | Check-in 409 | Sudah check-in hari ini (terverifikasi: `attendance_duplicate`) | `GET /v1/attendance?from=&to=` cek | 1 entri/hari/pegawai |
| 11 | Check-out 404 | Belum check-in (terverifikasi: `no_open_checkin`) | Check-in dulu | 200 checked_out |
| 12 | Overtime 0 padahal lembur | Lembur = >8 jam/hari (`GREATEST(jam-8,0)`) | Bandingkan durasi check_in→out | 8 jam pas = 0 (benar) |
| 13 | Staff lihat data orang lain | Salah paham: staff terkunci milik sendiri (by design) | Login staff → list attendance | Hanya milik sendiri |
| 14 | Data hilang setelah `down` | Volume terhapus (`down -v`) | `docker volume ls \| grep shiftbase`; backup dulu | Volume ada |
| 15 | Lupa kredensial seed | `admin/manager/staff @shiftbase.local` + `*123!` | Lihat `seed/seed.sql` komentar | Login 200 |

Aturan umum: `compose ps` + `logs` dulu, tebak kemudian.
Catat error persisnya untuk tiket.
