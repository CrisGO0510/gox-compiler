use std::fs;
mod lexer;
mod utils;

fn main() {
    let file_path = "./gox_examples/ejemplo.gox";

    let text = fs::read_to_string(file_path).expect("No se pudo leer el archivo");

    let tokens = lexer::tokenize(&text);

    for token in tokens {
        println!("{:?}", token);
    }
}
