#!/usr/bin/env bash
# Restore MySQL Shiftbase dari backup .sql.gz. MINTA KONFIRMASI (tulis ulang DB!).
# Pakai: ./shiftbase-restore.sh <FILE_BACKUP> [--force]
set -euo pipefail
[ $# -ge 1 ] || { echo "pakai: $0 <file-backup> [--force]" >&2; exit 1; }
SRC="$1"
[ -f "$SRC" ] || { echo "ERR: $SRC tak ada" >&2; exit 1; }
DB_HOST="${SB_HOST:-127.0.0.1}"
DB_PORT="${SB_PORT:-3306}"
DB_USER="${SB_USER:-shift}"
DB_PASS="${SB_PASS:-shiftpass}"
DB_NAME="${SB_DB:-shiftbase}"
if [ "${2:-}" != "--force" ]; then
  echo "Akan MENULIS ULANG $DB_NAME@$DB_HOST:$DB_PORT dari $SRC"
  read -r -p "Lanjut? [ya/TIDAK] " ans
  [ "$ans" = "ya" ] || { echo "batal"; exit 1; }
fi
MYSQL_PWD="$DB_PASS" mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" "$DB_NAME" < <(gzip -dc "$SRC")
echo "OK: restore selesai (verifikasi: SELECT COUNT(*) FROM employees;)"
