use super::{OneCharToken, Token, TokenType, TwoCharToken};
use crate::utils::error_enum::{Error, print_error};

pub fn tokenize(text: &str) -> Vec<Token> {
    let mut index: usize = 0;
    let mut tokens: Vec<Token> = Vec::new();
    let mut lineno: usize = 1;

    let position_char = |index: usize| text.chars().nth(index);

    loop {
        let current_char = match position_char(index) {
            Some(c) => c,
            None => break,
        };

        if current_char == '\n' {
            index += 1;
            lineno += 1;
            continue;
        }

        if current_char.is_whitespace() {
            index += 1;
            continue;
        }

        if let (Some(c1), Some(c2)) = (position_char(index), position_char(index + 1)) {
            if c1 == '/' && c2 == '/' {
                index += 2;
                while let Some(c) = position_char(index) {
                    if c == '\n' {
                        lineno += 1;
                        index += 1;
                        break;
                    }
                    index += 1;
                }
                continue;
            }

            if c1 == '/' && c2 == '*' {
                index += 2;
                while let (Some(c1), Some(c2)) = (position_char(index), position_char(index + 1)) {
                    if c1 == '*' && c2 == '/' {
                        index += 2;
                        break;
                    }
                    if c1 == '\n' {
                        lineno += 1;
                    }
                    index += 1;
                }
                continue;
            }

            if let Some(token_type) = TwoCharToken::is_two_char_token(c1, c2) {
                tokens.push(Token::new(
                    TokenType::TwoChar(token_type),
                    format!("{}{}", c1, c2),
                    lineno,
                ));
                index += 2;
                continue;
            }
        }

        if let Some(token_type) = OneCharToken::is_one_char_token(current_char) {
            tokens.push(Token::new(
                TokenType::OneChar(token_type),
                current_char.to_string(),
                lineno,
            ));
            index += 1;
            continue;
        }

        let mut literal = String::new();
        while let Some(c) = position_char(index) {
            if c.is_alphanumeric() || c == '_' || c == '\'' || c == '.' {
                literal.push(c);
                index += 1;
            } else {
                break;
            }
        }

        if !literal.is_empty() {
            if let Some(token_type) = TokenType::from_literal(&literal) {
                tokens.push(Token::new(token_type, literal, lineno));
                continue;
            }

            tokens.push(Token::new(TokenType::Illegal, literal.clone(), lineno));
            print_error(Error::UnknownLiteral(literal.clone()));
            continue;
        }

        tokens.push(Token::new(
            TokenType::Illegal,
            current_char.to_string(),
            lineno,
        ));
        print_error(Error::UnknownCharacter(current_char));
        index += 1;
    }

    tokens.push(Token::new(TokenType::EOF, "".to_string(), lineno));

    return tokens;
}
