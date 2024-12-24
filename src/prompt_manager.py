from typing import Dict, Optional

from jinja2 import Template


class PromptManager:
    """
    A class to manage reading and rendering prompts from .j2 template files.
    """

    def __init__(self, template_dir: str) -> None:
        """
        Initialize the PromptManager with the directory containing .j2 templates.

        Args:
            template_dir: The directory where the .j2 template files are stored.
        """
        self.template_dir = template_dir

    def read_template(self, template_name: str) -> str:
        """
        Read the content of a .j2 template file.

        Args:
            template_name: The name of the template file.

        Returns:
            The content of the template as a string.

        Raises:
            FileNotFoundError: If the template file does not exist.
        """
        file_path = f"{self.template_dir}/{template_name}"
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Template file '{template_name}' not found in directory '{self.template_dir}'."
            )

    def render_template(
        self, template_name: str, context: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Render a .j2 template with the given context.

        Args:
            template_name: The name of the template file.
            context: A dictionary of variables to be used in the template.

        Returns:
            The rendered template as a string.
        """
        context = context or {}
        template_content = self.read_template(template_name)
        template = Template(template_content)
        return template.render(context)
