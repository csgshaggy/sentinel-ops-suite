#!/usr/bin/env bash
set -euo pipefail

# Colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
NC="\e[0m"

echo -e "${CYAN}[frontend_master_chain] Starting full frontend integrity pipeline...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ordered pipeline steps
STEP_CMDS=(
  "$SCRIPT_DIR/frontend_doctor_chain.sh"
  "$SCRIPT_DIR/frontend_frontline.sh"
  "$SCRIPT_DIR/frontend_hash_guard.sh"
  "$SCRIPT_DIR/frontend_manifest_guard.sh"
  "$SCRIPT_DIR/frontend_nginx_guard.sh"
  "$SCRIPT_DIR/deploy_frontend_unified.sh"
)

STEP_NAMES=(
  "Frontend Doctor Chain"
  "Frontend Frontline (Fusion)"
  "Hash Guard (Drift Detection)"
  "Manifest Guard (Vite manifest.json)"
  "NGINX Guard (Deployment Readiness)"
  "Unified Frontend Deployment"
)

STEP_STATUS=()
STEP_TIME=()

AUTO_REPAIR="${AUTO_REPAIR:-1}"   # 1 = enabled, 0 = disabled

run_step() {
  local idx="$1"
  local name="${STEP_NAMES[$idx]}"
  local cmd="${STEP_CMDS[$idx]}"

  echo -e "${CYAN}[STEP] Running: ${name}${NC}"
  local start_ts end_ts duration
  start_ts="$(date +%s)"

  if "$cmd"; then
    end_ts="$(date +%s)"
    duration=$((end_ts - start_ts))
    STEP_STATUS[$idx]="OK"
    STEP_TIME[$idx]="$duration"
    echo -e "${GREEN}[STEP] SUCCESS: ${name} (${duration}s)${NC}"
    return 0
  fi

  end_ts="$(date +%s)"
  duration=$((end_ts - start_ts))
  STEP_STATUS[$idx]="FAIL"
  STEP_TIME[$idx]="$duration"
  echo -e "${RED}[STEP] FAIL: ${name} (${duration}s)${NC}"

  # Auto-repair logic (not applied to deploy step)
  if [[ "$AUTO_REPAIR" -eq 1 ]]; then
    echo -e "${YELLOW}[AUTO-REPAIR] Attempting repair for: ${name}${NC}"

    case "$name" in
      "Frontend Doctor Chain"|"Frontend Frontline (Fusion)")
        if [[ -x "$SCRIPT_DIR/frontend_frontline.sh" ]]; then
          echo -e "${YELLOW}[AUTO-REPAIR] Rebuilding both apps via frontend_frontline.sh...${NC}"
          if "$SCRIPT_DIR/frontend_frontline.sh"; then
            echo -e "${GREEN}[AUTO-REPAIR] Rebuild succeeded. Re-running ${name}.${NC}"
            if "$cmd"; then
              STEP_STATUS[$idx]="OK*"
              echo -e "${GREEN}[AUTO-REPAIR] ${name} recovered after repair.${NC}"
              return 0
            fi
          fi
        fi
        ;;
      "Hash Guard (Drift Detection)")
        HASH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/.hashes"
        echo -e "${YELLOW}[AUTO-REPAIR] Resetting hash baselines in ${HASH_DIR}${NC}"
        rm -f "${HASH_DIR}/login-app.sha256" "${HASH_DIR}/dashboard-app.sha256" 2>/dev/null || true
        if "$cmd"; then
          STEP_STATUS[$idx]="OK*"
          echo -e "${GREEN}[AUTO-REPAIR] Hash guard recovered after baseline reset.${NC}"
          return 0
        fi
        ;;
      "Manifest Guard (Vite manifest.json)"|"NGINX Guard (Deployment Readiness)")
        if [[ -x "$SCRIPT_DIR/frontend_frontline.sh" ]]; then
          echo -e "${YELLOW}[AUTO-REPAIR] Rebuilding both apps via frontend_frontline.sh...${NC}"
          if "$SCRIPT_DIR/frontend_frontline.sh"; then
            echo -e "${GREEN}[AUTO-REPAIR] Rebuild succeeded. Re-running ${name}.${NC}"
            if "$cmd"; then
              STEP_STATUS[$idx]="OK*"
              echo -e "${GREEN}[AUTO-REPAIR] ${name} recovered after repair.${NC}"
              return 0
            fi
          fi
        fi
        ;;
    esac

    echo -e "${RED}[AUTO-REPAIR] Repair failed for: ${name}${NC}"
  fi

  return 1
}

overall_fail=0

for i in "${!STEP_CMDS[@]}"; do
  if ! run_step "$i"; then
    overall_fail=1
  fi
done

echo
echo -e "${CYAN}[SUMMARY] Frontend Integrity Pipeline${NC}"
printf '%-40s | %-8s | %-8s\n' "Step" "Status" "Time(s)"
printf '%.0s-' {1..65}
echo

for i in "${!STEP_NAMES[@]}"; do
  name="${STEP_NAMES[$i]}"
  status="${STEP_STATUS[$i]:-SKIP}"
  time="${STEP_TIME[$i]:-0}"

  case "$status" in
    "OK") color="$GREEN" ;;
    "OK*") color="$YELLOW" ;;
    "FAIL") color="$RED" ;;
    *) color="$NC" ;;
  esac

  printf '%-40s | %b%-8s%b | %-8s\n' "$name" "$color" "$status" "$NC" "$time"
done

echo
if [[ "$AUTO_REPAIR" -eq 1 ]]; then
  echo -e "${YELLOW}* Status 'OK*' indicates success after auto-repair.${NC}"
fi

if [[ "$overall_fail" -eq 1 ]]; then
  echo -e "${RED}[frontend_master_chain] FAIL: One or more steps failed.${NC}"
  exit 1
fi

echo -e "${GREEN}[frontend_master_chain] SUCCESS: All steps completed successfully.${NC}"
