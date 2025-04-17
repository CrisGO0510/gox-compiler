use colored::*;

pub enum Error {
    UnknownLiteral(String),
    UnknownCharacter(char),
}

pub fn print_error(error: Error) {
    match error {
        Error::UnknownLiteral(lit) => {
            println!("{} {}", "Unknown literal:".red(), lit);
        }
        Error::UnknownCharacter(ch) => {
            println!("{} {}", "Unknown character:".red(), ch);
        }
    }
}
