import * as vscode from "vscode";

export function activate(context: vscode.ExtensionContext) {
  let terminal: vscode.Terminal | undefined;

  let disposable = vscode.commands.registerCommand("gox-runner.run", () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("No hay un archivo abierto.");
      return;
    }

    const filePath = editor.document.fileName;
    if (!filePath.endsWith(".gox")) {
      vscode.window.showErrorMessage("Este no es un archivo .gox.");
      return;
    }

    // Reutilizar la terminal si ya existe, o crear una nueva si no
    if (!terminal || terminal.exitStatus !== undefined) {
      terminal = vscode.window.createTerminal("Gox Runner");
    }

    terminal.show();

    const venvPython =
      process.platform === "win32"
        ? ".venv\\Scripts\\python"
        : ".venv/bin/python";
    terminal.sendText(`${venvPython} src/main.py "${filePath}"`);
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
