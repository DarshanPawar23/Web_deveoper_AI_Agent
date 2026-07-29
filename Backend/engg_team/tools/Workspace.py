from crewai.tools import BaseTool
from pathlib import Path
from pydantic import BaseModel,Field
from typing import  Type
import shutil
import subprocess

SANDBOX_DIR = Path(__file__).parents[1] / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

class ResetSandboxTool(BaseTool):
    name:str="Reset_sandbox"
    description:str=(
        "Before adding the new project remove the exsited project"
    )
    def _run(self) ->None:
        if SANDBOX_DIR.exists():
         shutil.rmtree(SANDBOX_DIR)
        SANDBOX_DIR.mkdir(parents=True)
        subprocess.run(["uv", "init", "--bare", "--python", "3.13"], cwd=SANDBOX_DIR, check=True)
        subprocess.run(["uv", "add", "gradio"], cwd=SANDBOX_DIR, check=True)

class ListSandboxFilesTool(BaseTool):
    name: str = "list_sandbox_files"
    description: str = (
        "List all files currently available in the sandbox directory."
    )

    def _run(self) -> str:
        names = sorted(p.name for p in SANDBOX_DIR.iterdir())
        return "\n".join(names) if names else "The sandbox is empty."

class ReadDirectoryTreeTool(BaseTool):
    name: str = "read_directory_tree"
    description: str = (
        "Display the complete directory tree of the sandbox workspace, "
        "including all folders and files. Use this tool to understand the "
        "project structure before creating, updating, or deleting files."
    )

    def _build_tree(self, directory: Path, prefix: str = "") -> list[str]:
        """Recursively build a directory tree."""
        lines = []

        items = sorted(
            directory.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower())
        )

        for index, item in enumerate(items):
            connector = "└── " if index == len(items) - 1 else "├── "
            lines.append(f"{prefix}{connector}{item.name}")

            if item.is_dir():
                extension = "    " if index == len(items) - 1 else "│   "
                lines.extend(
                    self._build_tree(item, prefix + extension)
                )

        return lines

    def _run(self) -> str:
        if not SANDBOX_DIR.exists():
            return "Sandbox directory does not exist."

        tree = [SANDBOX_DIR.name]
        tree.extend(self._build_tree(SANDBOX_DIR))

        return "\n".join(tree)

class CreateDirectoryInput(BaseModel):
    directory_path: str = Field(
        ...,
        description="Relative directory path inside the sandbox."
    )

class CreateDirectoryTool(BaseTool):
    name: str = "Create Directory Tool"
    description: str = (
        "Creates a directory inside the sandbox workspace. "
        "If the directory already exists, nothing happens."
    )
    args_schema: Type[BaseModel] = CreateDirectoryInput

    def _run(self, directory_path: str) -> str:
        try:
            full_path = SANDBOX_DIR / directory_path
            if full_path.exists():
                return f"Directory already exsist :{directory_path}"

            full_path.mkdir(
                parents=True,
                exist_ok=True
            )
            return f"Directory created: {directory_path}"

        except Exception as e:
            return f"Error: {str(e)}"


class ReadFileInput(BaseModel):
    file_path: str = Field(
        ...,
        description="Relative path of the file inside the sandbox."
    )

class ReadFileTool(BaseTool):
    name: str = "Read File Tool"
    description: str = (
        "Reads the contents of a file inside the sandbox workspace."
    )
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, file_path: str) -> str:
        try:
            full_path = SANDBOX_DIR / file_path

            if not full_path.exists():
                return f"Error: File '{file_path}' does not exist."

            if not full_path.is_file():
                return f"Error: '{file_path}' is not a file."

            return full_path.read_text(encoding="utf-8")

        except Exception as e:
            return f"Error reading file: {str(e)}"

class WriteFileInput(BaseModel):
    file_path: str = Field(
        ...,
        description="Relative path of the file to create inside the sandbox."
    )

    content: str = Field(
        ...,
        description="Content to write into the file."
    )
class WriteFileTool(BaseTool):
    name: str = "Write File Tool"

    description: str = (
        "Creates a new file inside the sandbox and writes the provided content. "
        "If parent directories do not exist, they are created automatically."
    )

    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            full_path = SANDBOX_DIR / file_path
            if full_path.exists():
                return (
                        f"Error: '{file_path}' already exists. "
                        "Use UpdateFileTool instead."
                        )
            full_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            full_path.write_text(
                content,
                encoding="utf-8"
            )

            return f"Successfully wrote file: {file_path}"

        except Exception as e:
            return f"Error writing file: {str(e)}"

class UpdateFileInput(BaseModel):
    file_path: str = Field(
        ...,
        description="Relative path of the file inside the sandbox."
    )

    content: str = Field(
        ...,
        description="New content to replace the existing file."
    )


class UpdateFileTool(BaseTool):
    name: str = "Update File Tool"

    description: str = (
        "Updates an existing file inside the sandbox."
    )

    args_schema: Type[BaseModel] = UpdateFileInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            full_path = SANDBOX_DIR / file_path

            if not full_path.exists():
                return f"Error: File '{file_path}' does not exist."

            if not full_path.is_file():
                return f"Error: '{file_path}' is not a file."

            full_path.write_text(
                content,
                encoding="utf-8"
            )

            return f"Successfully updated: {file_path}"

        except Exception as e:
            return f"Error updating file: {str(e)}"


class DeleteFileInput(BaseModel):
    file_path: str = Field(
        ...,
        description="Relative path of the file to delete."
    )


class DeleteFileTool(BaseTool):
    name: str = "Delete File Tool"

    description: str = (
        "Deletes a file from the sandbox workspace."
    )

    args_schema: Type[BaseModel] = DeleteFileInput

    def _run(self, file_path: str) -> str:
        try:
            full_path = SANDBOX_DIR / file_path

            if not full_path.exists():
                return f"Error: File '{file_path}' does not exist."

            if not full_path.is_file():
                return f"Error: '{file_path}' is not a file."

            full_path.unlink()

            return f"Successfully deleted: {file_path}"

        except Exception as e:
            return f"Error deleting file: {str(e)}"