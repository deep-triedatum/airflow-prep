from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

from airflow.models.baseoperator import BaseOperatorLink
from airflow.plugins_manager import AirflowPlugin
from airflow.security import permissions
from airflow.www.auth import has_access

from airflow.providers.http.operators.http import HttpOperator


bp= Blueprint(
    name="hello_plugin",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/hello_plugin",
)


class HelloView(AppBuilderBaseView):
    default_view="index"
    
    @expose("/")
    @has_access([(permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE)])
    def index(self):
        return self.render_template("hello_plugin/hello.html", message="Hello from a plugin!")

class ApiDocsLink(BaseOperatorLink):
    name = "API Docs"                      
    operators = []                        

    def get_link(self, operator, *, ti_key):
        return "https://dummyjson.com/docs/users"
    
ApiDocsLink.operators = [HttpOperator]


class HelloUIPlugin(AirflowPlugin):
    name = "hello_ui_plugin"
    flask_blueprints = [bp]
    appbuilder_views = [
        {"name": "Hello Page", "category": "My Plugins", "view": HelloView()}
    ]
    appbuilder_menu_items = [
        {"name": "Airflow Docs", "category": "Docs", "href": "https://airflow.apache.org/docs/"}
    ]
    operator_extra_links = [ApiDocsLink()]