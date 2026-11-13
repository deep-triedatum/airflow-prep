"""Bulk pause / unpause plugin (Airflow 3).

The v2 version queried the metadata DB from the webserver. In v3 the api-server
should not be used that way, so this page is plain HTML + JS that calls the
public REST API (/api/v2/dags). The browser's login cookie authenticates the
calls, so users can only touch DAGs their auth manager lets them edit.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from airflow.plugins_manager import AirflowPlugin

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Bulk Pause</title>
<style>
 body{font-family:system-ui,sans-serif;margin:1.5rem}
 table{border-collapse:collapse;width:100%;max-width:720px}
 th,td{text-align:left;padding:6px 10px;border-bottom:1px solid #ddd}
 button,input{font:inherit;padding:6px 12px;margin-right:6px}
 #msg{margin:10px 0;min-height:1.2em}
</style></head>
<body>
<h2>Bulk pause / unpause</h2>
<input id="q" placeholder="Filter DAG ids"> <button onclick="load()">Search</button>
<div id="msg"></div>
<table><thead><tr>
  <th><input type="checkbox" id="all" onclick="toggleAll(this)"></th><th>DAG</th><th>State</th>
</tr></thead><tbody id="rows"></tbody></table>
<p>
  <button onclick="apply(true)">Pause selected</button>
  <button onclick="apply(false)">Unpause selected</button>
</p>
<script>
const msg = t => document.getElementById("msg").textContent = t;
async function load() {
  const q = document.getElementById("q").value.trim();
  const url = "/api/v2/dags?limit=200&order_by=dag_id" + (q ? "&dag_id_pattern=" + encodeURIComponent(q) : "");
  const r = await fetch(url, {credentials: "same-origin"});
  if (!r.ok) { msg("Failed to load DAGs: HTTP " + r.status); return; }
  const data = await r.json();
  const tb = document.getElementById("rows"); tb.innerHTML = "";
  for (const d of data.dags) {
    const tr = document.createElement("tr");
    tr.innerHTML = '<td><input class="pick" type="checkbox"></td><td></td><td></td>';
    tr.children[0].firstChild.value = d.dag_id;
    tr.children[1].textContent = d.dag_id;
    tr.children[2].textContent = d.is_paused ? "Paused" : "Active";
    tb.appendChild(tr);
  }
  msg(data.dags.length + " DAG(s)");
}
function toggleAll(box) { document.querySelectorAll(".pick").forEach(c => c.checked = box.checked); }
async function apply(pause) {
  const ids = [...document.querySelectorAll(".pick:checked")].map(c => c.value);
  if (!ids.length) { msg("No DAGs selected."); return; }
  let ok = 0, failed = [];
  for (const id of ids) {
    const r = await fetch("/api/v2/dags/" + encodeURIComponent(id) + "?update_mask=is_paused", {
      method: "PATCH", credentials: "same-origin",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({is_paused: pause}),
    });
    r.ok ? ok++ : failed.push(id + " (" + r.status + ")");
  }
  msg((pause ? "Paused " : "Unpaused ") + ok + " DAG(s)." + (failed.length ? " Failed: " + failed.join(", ") : ""));
  load();
}
load();
</script></body></html>
"""

app = FastAPI(title="Bulk pause plugin")


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE


class BulkPausePlugin(AirflowPlugin):
    name = "bulk_pause_plugin"
    fastapi_apps = [{"app": app, "url_prefix": "/bulk-pause", "name": "Bulk pause"}]
    external_views = [
        {
            "name": "Bulk Pause",
            "href": "/bulk-pause/",
            "destination": "nav",
            "category": "My Plugins",
            "url_route": "bulk-pause",
        }
    ]
