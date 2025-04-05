#!/bin/bash

# Path to SQLite DB
DB_PATH="./proxy_db.sqlite"
REPORT_JSON="./report.json"

# Get the current interface IP (excluding localhost)
INTERFACE_IP=$(ip -4 a | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -n1)
PROXY_PORT="8080"
PROXY="$INTERFACE_IP:$PROXY_PORT"

echo "🧭 Using local proxy: $PROXY"

# Fetch URLs from 'urls' table where status = 'ALLOW'
mapfile -t URLS < <(sqlite3 "$DB_PATH" "SELECT url FROM urls WHERE status = 'ALLOW';")

if [ ${#URLS[@]} -eq 0 ]; then
  echo "❌ No URLs found in $DB_PATH with status = 'ALLOW'"
  exit 1
fi

# Store report data in an array
declare -a REPORT_ENTRIES

# Function to generate a fake-looking curl command
generate_fake_curl() {
  local url="$1"

  local user
  user=$(shuf -n1 -e \
    "administrator:ironport" \
    "administrator:tronport" \
    "administrator:Lronport")

  local rand_proxy
  rand_proxy=$(shuf -n1 -e \
    "10.10.192.39:3128" \
    "18.18.192.39:3128" \
    "10.18.192.39:3128" \
    "$PROXY")

  local flags=(-L --location -k --insecure -o /dev/null -A -R -H --compressed)
  local rand_flags
  rand_flags=$(shuf -e -- "${flags[@]}" -n3 | xargs)

  echo "$url|$user|$rand_proxy|$rand_flags"
}

# Number of rounds
ROUNDS=2

echo "[" > "$REPORT_JSON" # start JSON array

for (( round=1; round<=ROUNDS; round++ )); do
  echo "🔁 Round $round of $ROUNDS"

  for url in "${URLS[@]}"; do
    result=$(generate_fake_curl "$url")
    IFS='|' read -r final_url user proxy flags <<< "$result"

    curl_cmd="curl -s '$final_url' --proxy-ntlm -U '$user' -x '$proxy' $flags &"
    echo "▶ $curl_cmd"
    eval "$curl_cmd"

    # Escape for JSON
    json_entry=$(jq -n \
      --arg url "$final_url" \
      --arg user "$user" \
      --arg proxy "$proxy" \
      --arg flags "$flags" \
      '{url: $url, user: $user, proxy: $proxy, flags: $flags}')
    REPORT_ENTRIES+=("$json_entry")
  done

  echo "⏳ Sleeping 5 seconds before next round..."
  sleep 5
done

# Join entries with comma and save to report.json
printf "%s\n" "$(IFS=,; echo "${REPORT_ENTRIES[*]}")" >> "$REPORT_JSON"
echo "]" >> "$REPORT_JSON"

echo "✅ All requests completed."
echo "📄 JSON report saved to $REPORT_JSON"
