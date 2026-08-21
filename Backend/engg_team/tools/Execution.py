from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Type
import subprocess

SANDBOX_DIR = Path(__file__).parents[1] / "sandbox"


class RunCommandInput(BaseModel):
    command: str = Field(
        ...,
        description="Terminal command to execute inside the sandbox."
    )


class RunCommandTool(BaseTool):
    name: str = "Run Command Tool"

    description: str = (
        "Executes a shell command inside the sandbox workspace "
        "and returns the command output."
    )

    args_schema: Type[BaseModel] = RunCommandInput

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{SANDBOX_DIR}:/workspace",
                "-w",
                "/workspace",
                "ghcr.io/astral-sh/uv:python3.13-bookworm-slim",
                "sh",
                "-c",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=300,
            check=True,
        )

            return result.stdout or "Command executed successfully."

        except subprocess.CalledProcessError as e:
            return e.stderr or str(e)

class InstallDependenciesTool(BaseTool):
    name:str = "Install Dependencies Tool"

    description:str = (
        "Installs all project dependencies using uv sync."
    )

    def _run(self) -> str:
        try:
            result = subprocess.run(
                [
    "docker",
    "run",
    "--rm",
    "-v",
    f"{SANDBOX_DIR}:/workspace",
    "-w",
    "/workspace",
    "ghcr.io/astral-sh/uv:python3.13-bookworm-slim",
    "uv",
    "sync",
],
                cwd=SANDBOX_DIR,
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout or "Dependencies installed successfully."

        except subprocess.CalledProcessError as e:
            return e.stderr or str(e)

