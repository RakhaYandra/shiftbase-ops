# FAQ — Shiftbase

**Login seed?** `admin/manager/staff` + `@shiftbase.local`, password `Admin123!`/`Manager123!`/`Staff123!`.

**Lembur dihitung dari apa?** `GREATEST(jam_kerja-8, 0)` per hari. Tepat 8 jam = 0 lembur (benar).

**Check-in 2x error?** 1 check-in/hari/pegawai (by design). Tombol jangan diklik 2x.

**Import CSV gagal?** Header harus persis `name,email,phone,position,hire_date`, maks 2MB. Lihat per-baris error di hasil.

**Masuk container api?** Tak bisa — distroless tanpa shell. Pakai log + adminer.

**Data hilang setelah down -v?** `-v` hapus volume! Restore dari backup harian.

**Template CSV?** `name,email,phone,position,hire_date` + 1 baris contoh di runbook.
