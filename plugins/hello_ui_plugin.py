"""Hello UI plugin (Airflow 3).

v2 -> v3 mapping:
  appbuilder_views (Flask page)    -> fastapi_apps (serves the page) + external_views (nav entry, shown in an iframe)
  appbuilder_menu_items (link)     -> external_views
  operator_extra_links             -> operator_extra_links (BaseOperatorLink now comes from airflow.sdk)
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from airflow.plugins_manager import AirflowPlugin
from airflow.providers.http.operators.http import HttpOperator
from airflow.sdk import BaseOperatorLink

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Hello Plugin</title>
<style>body{font-family:system-ui,sans-serif;margin:2rem}</style></head>
<body><h2>{message}</h2><p>This page is served by a custom FastAPI plugin.</p></body></html>
"""

app = FastAPI(title="Hello plugin")


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE.replace("{message}", "Hello from a plugin!")


class ApiDocsLink(BaseOperatorLink):
    name = "API Docs"
    operators = [HttpOperator]

    def get_link(self, operator, *, ti_key):
        return "https://dummyjson.com/docs/users"


class HelloUIPlugin(AirflowPlugin):
    name = "hello_ui_plugin"
    fastapi_apps = [{"app": app, "url_prefix": "/hello-plugin", "name": "Hello plugin"}]
    external_views = [
        {
            "name": "Hello Page",
            "href": "/hello-plugin/",
            "destination": "nav",
            "category": "My Plugins",
            "url_route": "hello-page",
        },
        {
            "name": "Airflow Docs",
            "href": "https://airflow.apache.org/docs/",
            "destination": "nav",
            "category": "Docs",
            "url_route": "airflow-docs",
        },
    ]
    operator_extra_links = [ApiDocsLink()]
