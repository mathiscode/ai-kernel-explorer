import argparse
import os
import toml

from openai import OpenAI
from textual import work
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (DirectoryTree, Footer, Header, Markdown, MarkdownViewer)

from ai_kernel_explorer.prompt import system_prompt

with open("pyproject.toml", encoding="utf-8") as pyproject:
    version = toml.load(pyproject)["tool"]["poetry"]["version"]

parser = argparse.ArgumentParser(
    prog="ai-kernel-explorer",
    description="Explore the Linux kernel source code with AI-generated summaries.",
    epilog="https://github.com/mathiscode/ai-kernel-explorer"
)

parser.add_argument("root", nargs="?", help="The root directory of the Linux kernel source code. (default: /usr/src)")
parser.add_argument("--api-key", help="Your OpenAI API key. (default: $OPENAI_API_KEY)")
parser.add_argument("--cache", help="The path to store AI responses. (default: ~/.cache/ai-kernel-explorer)")
parser.add_argument("--model", help="The OpenAI model to use. (default: gpt-4o)")
parser.add_argument("--version", action="version", version=f"%(prog)s {version} (https://github.com/mathiscode/ai-kernel-explorer)")
args = parser.parse_args()

if not args.api_key and not os.getenv("OPENAI_API_KEY"):
    parser.error("You must provide an OpenAI API key with --api-key or set the OPENAI_API_KEY environment variable.")

cache_path = args.cache or os.path.expanduser("~/.cache/ai-kernel-explorer/") or "/tmp/ai-kernel-explorer/"
client = OpenAI(api_key=args.api_key or os.getenv("OPENAI_API_KEY"))
root = args.root or "/usr/src"

async def ai_response(prompt):
    return client.chat.completions.create(
        model=args.model or "gpt-4o", messages=[{"role": "user", "content": prompt}]
    )

class Explorer(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [("g", "generate", "Generate"), ("t", "toggle_theme", "Theme"), ("q", "quit", "Quit")]

    path = reactive(root)
    markdown = reactive("# AI Kernel Explorer\n\n## Exploring the Linux kernel\n\nSelect a file or directory to get started! Files will be summarized automatically, or you can press g to generate a summary for the selected directory.")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="AI Kernel Explorer", icon="🐧")
        yield DirectoryTree(root)
        yield MarkdownViewer(markdown=self.markdown)
        yield Footer()

    def watch_markdown(self, markdown: str) -> None:
        self.markdown = markdown

    def action_toggle_theme(self) -> None:
        self.dark = not self.dark

    async def action_generate(self) -> None:
        self.markdown = "# Generating AI summary..."
        await self.query_one(Markdown).update(self.markdown)
        self.fetch_response(self.path, cache_path + str(self.path) + "/response.md")

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        self.path = event.path

    async def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.path = event.path
        self.markdown = "# Getting AI summary..."
        await self.query_one(Markdown).update(self.markdown)

        if os.path.exists(cache_path + str(event.path) + "/response.md"):
            with open(cache_path + str(event.path) + "/response.md", encoding="utf-8") as f:
                content = f.read()

            self.markdown = content
            self.query_one(Markdown).update(self.markdown)
        else:
            self.fetch_response(event.path, cache_path + str(event.path) + "/response.md")

    @work(exclusive=True)
    async def fetch_response(self, path, cache_file) -> None:
        response = await ai_response(system_prompt(path))

        content = response.choices[0].message.content
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(content)

        self.app.markdown = content
        self.app.query_one(Markdown).update(self.app.markdown)

def main():
    app = Explorer()
    app.title = "AI Kernel Explorer"
    app.run()

if __name__ == "__main__":
    main()
