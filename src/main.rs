mod lexer;
fn main() {
    println!("Hello, world2!");

    let text = "2 + 1";

    println!("{}, {:?}", text, text.chars());

    let tokens = lexer::tokenize(text);

    // for token in tokens {
    //     println!("{:?}", token);
    // }
}
