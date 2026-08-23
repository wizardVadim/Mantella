from fastapi import FastAPI
from fastapi.responses import FileResponse
import webbrowser
import gradio as gr
from src.config.config_loader import ConfigLoader
from src.http.routes.routeable import routeable
from src.ui.settings_ui_constructor import SettingsUIConstructor
import src.utils as utils
from src.localization.locales import SUPPORTED_LOCALES
from src.localization.translator import tr

logger = utils.get_logger()


class StartUI(routeable):
    BANNER = "docs/_static/img/mantella_banner.png"
    def __init__(self, config: ConfigLoader) -> None:
        super().__init__(config)
        self.__constructor = SettingsUIConstructor(config.ui_language)

    def create_main_block(self) -> gr.Blocks:
        with gr.Blocks(title="Mantella", fill_height=True, analytics_enabled=False, theme= self.__get_theme(), css=self.__load_css()) as main_block:

            ui_language_config = (self._config.definitions.get_config_value_definition("ui_language"))

            with gr.Row(elem_classes="ui-header"):
                gr.Markdown("## Mantella")

                language_selector = gr.Dropdown(
                    choices=[
                        (display_name, language_code)
                        for language_code, display_name in SUPPORTED_LOCALES.items()
                    ],
                    value=ui_language_config.value,
                    allow_custom_value=False,
                    label=tr("ui.header.language", ui_language_config.value),
                    container=False,
                    scale=0,
                    min_width=160,
                    elem_classes="ui-language-selector"
                )

            def change_ui_language(language: str):
                ui_language_config.value = language

                gr.Info(tr("ui.header.restart_required", language))

            language_selector.change(
                fn=change_ui_language,
                inputs=language_selector,
                outputs=None,
            )

            # with gr.Tab("Settings") as tabs:
            settings_page = self.__generate_settings_page()
            # with gr.Tab("Chat with NPCs", interactive=False):
            #     self.__generate_chat_page()
            # with gr.Tab("NPC editor", interactive=False):
            #     self.__generate_character_editor_page()

            with gr.Row(elem_classes="custom-footer"):
                gr.HTML(f"""
                    <div class="custom-footer">
                        <a href="https://art-from-the-machine.github.io/Mantella/" target="_blank">{tr("ui.footer.installation_guide", self._config.ui_language)}</a>
                    </div>
                """)
        return main_block

    def __generate_settings_page(self) -> gr.Column:
        # with gr.Column() as settings:
        for cf in self._config.definitions.base_groups:
            if not cf.is_hidden:
                with gr.Tab(tr(f"ui.section.{cf.identifier}", self._config.ui_language)):
                    cf.accept_visitor(self.__constructor)
        return None #settings
    
    def __generate_chat_page(self):
        return gr.Column()
    
    def __generate_character_editor_page(self):
        return gr.Column() 

    def __get_theme(self):
        return gr.themes.Soft(primary_hue="green",
                            secondary_hue="green",
                            neutral_hue="zinc",
                            font=['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                            font_mono=['IBM Plex Mono', 'ui-monospace', 'Consolas', 'monospace']).set(
                                input_text_size='*text_md',
                                input_padding='*spacing_md',
                            )

    
    def add_route_to_server(self, app: FastAPI):
        @app.get("/favicon.ico")
        async def favicon():
            return FileResponse("Mantella.ico")

        gr.mount_gradio_app(app,
                            self.create_main_block(),
                            path="/ui")
        
        link = f'http://localhost:{str(self._config.port)}/ui?__theme=dark'
        logger.log(24, f'\nMantella settings can be changed via this link:')
        logger.log(25, link)
        if self._config.auto_launch_ui == True:
            if not webbrowser.open(link, new=2):
                logger.warning('\nFailed to open Mantella settings UI automatically. To edit settings, see here:')
                logger.log(25, link)
    
    def __load_css(self):
        with open('src/ui/style.css', 'r') as file:
            css_content = file.read()
        return css_content
    
    def _setup_route(self):
        pass

    