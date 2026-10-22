# Протоколирование команд: run "команда" -> пишет "$ команда", вывод, код возврата и время в $LOG
LOG=${LOG:-log.txt}
run() {
  echo "\$ $*" | tee -a "$LOG"
  local s=$(date +%s%N)
  bash -c "$*" 2>&1 | tee -a "$LOG"
  local rc=${PIPESTATUS[0]}
  local ms=$(( ($(date +%s%N) - s) / 1000000 ))
  echo "[код возврата $rc, время ${ms} мс]" | tee -a "$LOG"
  echo | tee -a "$LOG"
  return $rc
}
# wait_http URL -> печатает время до первого ответа 200, мс
wait_http() {
  local s=$(date +%s%N)
  for i in $(seq 1 300); do
    if curl -sf -o /dev/null "$1"; then echo $(( ($(date +%s%N) - s) / 1000000 )); return 0; fi
    sleep 0.1
  done
  echo "timeout"; return 1
}
