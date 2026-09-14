#!/usr/bin/env bash
# Backup MySQL Shiftbase via mysqldump + gzip + rotasi (default simpan 7).
# Kredensial via env (default throwaway lokal, JANGAN taruh password asli di sini).
# Pakai: ./shiftbase-backup.sh [DIR_BACKUP] [RETENSI]
set -euo pipefail
BACKUP_DIR="${1:-./backups}"
KEEP="${2:-7}"
DB_HOST="${SB_HOST:-127.0.0.1}"
DB_PORT="${SB_PORT:-3306}"
DB_USER="${SB_USER:-shift}"
DB_PASS="${SB_PASS:-shiftpass}"
DB_NAME="${SB_DB:-shiftbase}"
mkdir -p "$BACKUP_DIR"
TS=$(date +%Y%m%d-%H%M%S)
OUT="$BACKUP_DIR/shiftbase-$TS.sql.gz"
MYSQL_PWD="$DB_PASS" mysqldump -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" \
  --single-transaction --routines "$DB_NAME" 2>/dev/null | gzip > "$OUT"
ls -t "$BACKUP_DIR"/shiftbase-*.sql.gz | tail -n +$((KEEP + 1)) | xargs -r rm --
echo "OK: $OUT ($(du -h "$OUT" | cut -f1))"
