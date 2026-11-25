#!/usr/bin/env bash
# gemini-key.sh: get the user's Gemini API key into their environment without it ever
# appearing in the chat, in a command, or in this skill folder.
#
#   bash gemini-key.sh status   say whether a key is set (never prints the key)
#   bash gemini-key.sh open     create the key file if needed and open it in a text editor
#   bash gemini-key.sh apply    after the user pasted and saved: make Claude Code see the key
#
# The key file is ~/.solnest/three-brain/.env (one line: GEMINI_API_KEY=...). It is outside
# the skill folder, so no update can touch it. The Gemini plugin reads GEMINI_API_KEY from
# the environment, so `apply` adds ONE line to the user's shell profile that loads the file
# (macOS, Linux), or saves it as a user environment variable (Windows). Claude Code has to
# be fully quit and reopened afterwards: it reads the environment when it starts.
set -u

DIR="${SOLNEST_HOME:-$HOME/.solnest}/three-brain"
FILE="$DIR/.env"
MARK="# Solnest Three-Brain: Gemini key"
WIN=0
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) WIN=1 ;; esac

# The value after GEMINI_API_KEY= in the key file, quotes and spaces stripped. Never echoed.
file_key() {
  [ -f "$FILE" ] || return 0
  sed -n 's/^[[:space:]]*\(export[[:space:]]\{1,\}\)\{0,1\}GEMINI_API_KEY[[:space:]]*=[[:space:]]*//p' "$FILE" \
    | head -1 | tr -d '\r"'"'"' '
}

profile() {
  case "${SHELL:-}" in
    */zsh) echo "$HOME/.zshrc" ;;
    */bash) if [ "$(uname -s)" = "Darwin" ]; then echo "$HOME/.bash_profile"; else echo "$HOME/.bashrc"; fi ;;
    *) echo "$HOME/.profile" ;;
  esac
}

cmd="${1:-status}"
case "$cmd" in
  status)
    if [ -n "${GEMINI_API_KEY:-}" ]; then
      echo "[ok] Gemini key: set in this session's environment"
    elif [ -n "$(file_key)" ]; then
      echo "[..] Gemini key: saved in the key file, but Claude Code does not see it yet. Run: apply, then fully quit and reopen Claude Code."
    else
      echo "[--] Gemini key: not set"
    fi
    ;;
  open)
    mkdir -p "$DIR"
    if [ ! -f "$FILE" ]; then
      printf '# Paste your Gemini API key right after the = sign, then save and close this file.\n# Get a free key at https://aistudio.google.com/apikey\nGEMINI_API_KEY=\n' > "$FILE"
      chmod 600 "$FILE" 2>/dev/null
    fi
    echo "[ok] key file  $FILE"
    if [ -n "${THREE_BRAIN_NO_OPEN:-}" ]; then
      :   # tests
    elif [ "$WIN" = 1 ]; then
      notepad.exe "$(cygpath -w "$FILE")" >/dev/null 2>&1 &
    elif [ "$(uname -s)" = "Darwin" ]; then
      open -t "$FILE"
    else
      (xdg-open "$FILE" >/dev/null 2>&1 &) || true
    fi
    ;;
  apply)
    key="$(file_key)"
    if [ -z "$key" ]; then
      echo "[!!] The key file has no key in it yet. Paste the key after GEMINI_API_KEY= and save the file, then run this again."
      exit 1
    fi
    case "$key" in
      *[!A-Za-z0-9_-]*) echo "[!!] That does not look like a Gemini key (it has characters a key never has). Check the file and run this again."; exit 1 ;;
    esac
    if [ "${#key}" -lt 20 ]; then
      echo "[!!] That looks too short to be a Gemini key. Check the file and run this again."
      exit 1
    fi
    key=""
    if [ "$WIN" = 1 ]; then
      # PowerShell reads the file itself, so the key is never on a command line.
      THREE_BRAIN_KEY_FILE="$(cygpath -w "$FILE")" powershell.exe -NoProfile -Command '
        $line = Get-Content $env:THREE_BRAIN_KEY_FILE | Where-Object { $_ -match "^\s*GEMINI_API_KEY\s*=" } | Select-Object -First 1
        $k = ($line -replace "^\s*GEMINI_API_KEY\s*=\s*", "").Trim().Trim([char]34).Trim([char]39)
        [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $k, "User")' \
        || { echo "[!!] Could not save the key as a Windows environment variable."; exit 1; }
      echo "[ok] Gemini key saved for this Windows user. Fully quit and reopen Claude Code so it sees it."
    else
      p="$(profile)"
      if [ -f "$p" ] && grep -qF "$MARK" "$p"; then
        echo "[ok] $p already loads the key file"
      else
        printf '\n%s (the key itself is in the file below, not here)\n[ -f "%s" ] && set -a && . "%s" && set +a\n' "$MARK" "$FILE" "$FILE" >> "$p" \
          || { echo "[!!] Could not write to $p."; exit 1; }
        echo "[ok] added one line to $p that loads the key file"
      fi
      echo "[ok] Gemini key is in place. Fully quit and reopen Claude Code so it sees it."
    fi
    ;;
  *)
    echo "usage: gemini-key.sh status | open | apply" >&2
    exit 2
    ;;
esac
