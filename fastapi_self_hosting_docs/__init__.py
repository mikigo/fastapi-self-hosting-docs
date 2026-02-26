import os

from fastapi import FastAPI as _FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles


def FastAPI(title="FastAPI Self Hosting Docs", **kwargs) -> _FastAPI:
    del kwargs["docs_url"]
    del kwargs["redoc_url"]
    app = _FastAPI(title=title, docs_url=None, redoc_url=None, **kwargs)
    static_dir_name = "fastapi-self-hosting-docs-static"
    app.mount(
        f"/{static_dir_name}",
        StaticFiles(
            directory=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), static_dir_name
            ),
            follow_symlink=True,
            check_dir=True,
        ),
        name=static_dir_name,
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"/{static_dir_name}/swagger-ui-bundle.js",
            swagger_css_url=f"/{static_dir_name}/swagger-ui.css",
            swagger_favicon_url=f"/{static_dir_name}/favicon.png",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=f"/{static_dir_name}/redoc.standalone.js",
            redoc_favicon_url=f"/{static_dir_name}/favicon.png",
        )

    return app
