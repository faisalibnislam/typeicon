#!/usr/bin/env bash
# Local PostgreSQL for development without Docker. Data lives in .data/pg (git-ignored).
# Usage: scripts/dev-db.sh start|stop|status|psql|reset
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PGBIN="${PGBIN:-$(brew --prefix postgresql@17 2>/dev/null)/bin}"
PGDATA="$ROOT/.data/pg"
PORT="${TYPEICON_PG_PORT:-54329}"
DB="${TYPEICON_PG_DB:-typeicon}"
export PATH="$PGBIN:$PATH"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

init() {
  if [ ! -f "$PGDATA/PG_VERSION" ]; then
    mkdir -p "$PGDATA"
    initdb -D "$PGDATA" -U typeicon --auth=trust --encoding=UTF8 --locale=C >/dev/null
    echo "listen_addresses = 'localhost'" >> "$PGDATA/postgresql.conf"
    echo "port = $PORT" >> "$PGDATA/postgresql.conf"
  fi
}

case "${1:-start}" in
  start)
    init
    if ! pg_ctl -D "$PGDATA" status >/dev/null 2>&1; then
      pg_ctl -D "$PGDATA" -l "$ROOT/.data/pg.log" -w start >/dev/null
    fi
    psql -h localhost -p "$PORT" -U typeicon -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB'" | grep -q 1 \
      || createdb -h localhost -p "$PORT" -U typeicon "$DB"
    psql -h localhost -p "$PORT" -U typeicon -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${DB}_test'" | grep -q 1 \
      || createdb -h localhost -p "$PORT" -U typeicon "${DB}_test"
    echo "postgres://typeicon@localhost:$PORT/$DB"
    ;;
  stop) pg_ctl -D "$PGDATA" -w stop ;;
  status) pg_ctl -D "$PGDATA" status ;;
  psql) exec psql -h localhost -p "$PORT" -U typeicon -d "$DB" ;;
  reset)
    pg_ctl -D "$PGDATA" -w stop >/dev/null 2>&1 || true
    rm -rf "$PGDATA"; "$0" start ;;
  *) echo "usage: $0 start|stop|status|psql|reset" >&2; exit 2 ;;
esac
