#!/bin/bash
curl -s -o /dev/null http://127.0.0.1:8770/ || (cd /home/claude/table-fit. && setsid nohup python3 -m http.server 8770 >/dev/null 2>&1 < /dev/null &)
curl -s -o /dev/null http://127.0.0.1:8769/ || (cd /tmp/claude-0/-home-claude/a2941520-6d34-5dd8-9a2f-962af0aae42b/scratchpad && setsid nohup python3 -m http.server 8769 >/dev/null 2>&1 < /dev/null &)
sleep 1
