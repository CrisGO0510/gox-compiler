mod lexer;

fn main() {
    println!("Hello, world2!");

    let text = "hola && 21 > 'a' <= true;";

    println!("{}, {:?}", text, text.chars());

    let tokens = lexer::tokenize(text);

    for token in tokens {
        println!("{:?}", token);
    }
}
