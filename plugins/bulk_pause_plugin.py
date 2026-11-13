from flask import Blueprint, flash, redirect, url_for, request, g
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

# from airflow.auth.managers.models.resource_details import DagAccessEntity
 
from airflow.models.dag import DagModel
from airflow.plugins_manager import AirflowPlugin
from airflow.security import permissions
from airflow.utils.session import create_session
from airflow.www.auth import has_access
from airflow.www.extensions.init_auth_manager import get_auth_manager

bp = Blueprint(
    name="bulk_pause",
    import_name=__name__,
    template_folder="templates",
)

class BulkPauseView(AppBuilderBaseView):
    default_view = "index"
    route_base = "/bulk-pause"
    
    @expose("/")
    @has_access([(permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE)])
    def index(self):
        q = request.args.get("q", "").strip().lower()
        
        editable = get_auth_manager().get_permitted_dag_ids(methods=["PUT"], user=g.user)
        with create_session() as session:
            rows = (
                session.query(DagModel.dag_id, DagModel.is_paused)
                .filter(DagModel.is_active, DagModel.dag_id.in_(editable))
                .order_by(DagModel.dag_id)
                .all()
            )
        dags = [r for r in rows if q in r.dag_id.lower()]
        return self.render_template("bulk_pause/index.html", dags=dags, q=q)
        
    
    @expose("/apply", methods=["POST"])
    @has_access([(permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE)])
    def apply(self):
        selected = request.form.getlist("dag_ids")
        pause = request.form.get("action") == "pause"
        editable = get_auth_manager().get_permitted_dag_ids(methods=["PUT"], user=g.user)
        ids = [d for d in selected if d in editable]
        if not ids:
            flash("No DAGs selected.", "warning")
        else:
            with create_session() as session:
                session.query(DagModel).filter(DagModel.dag_id.in_(ids)).update(
                    {DagModel.is_paused: pause}, synchronize_session=False
                )
            flash(f"{'Paused' if pause else 'Unpaused'} {len(ids)} DAG(s).", "info")
        return redirect(url_for(f"{self.endpoint}.index"))
    

class BulkPausePlugin(AirflowPlugin):
    name= "bulk_pause_plugin"
    flask_blueprints = [bp]
    appbuilder_views = [
        {"name": "Bulk Pause", "category": "My Plugins", "view": BulkPauseView()}
    ]
