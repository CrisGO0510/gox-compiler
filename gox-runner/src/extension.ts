import * as vscode from "vscode";
import * as path from "path";

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

    // terminal.sendText(`python lexicalAnalyzer.py "${filePath}"`);
    terminal.sendText(`python lexicalAnalyzer.py`);
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
