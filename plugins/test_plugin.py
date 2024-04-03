from airflow.plugins_manager import AirflowPlugin
from airflow.security import permissions
from airflow.www.auth import has_access
from airflow.models import dagbag


from flask import Blueprint
from flask_appbuilder import expose, BaseView as AppBuilderBaseView


bp = Blueprint(
    "test_plugin",
    __name__,
    template_folder="templates",  # registers airflow/plugins/templates as a Jinja template folder
    static_folder="static",
    static_url_path="/static/test_plugin",
)


# Creating a flask appbuilder BaseView
class TestAppBuilderBaseView(AppBuilderBaseView):
    default_view = "data"

    @expose("/")
    @has_access(
        [
            (permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE),
        ]
    )
    def data(self):
        return self.render_template("test_plugin_template/test.html", content="Hello galaxy!")


# Creating a flask appbuilder BaseView
class TestAppBuilderBaseNoMenuView(AppBuilderBaseView):
    default_view = "data"

    @expose("/")
    @has_access(
        [
            (permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE),
        ]
    )
    def data(self):
        return self.render_template("test_plugin_template/test.html", content="Hello galaxy!")


v_appbuilder_view = TestAppBuilderBaseView()
v_appbuilder_package = {
    "name": "Test View",
    "category": "Test Plugin",  
    "view": v_appbuilder_view,
}

v_appbuilder_nomenu_view = TestAppBuilderBaseNoMenuView()
v_appbuilder_nomenu_package = {"view": v_appbuilder_nomenu_view}


class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"
    hooks = []
    macros = []
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package, v_appbuilder_nomenu_package]
    appbuilder_menu_items = []