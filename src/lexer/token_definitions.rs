use super::{OneCharToken, Token, TokenType, TwoCharToken};

pub fn tokenize(text: &str) -> Vec<Token> {
    let mut index: usize = 0;
    let mut tokens: Vec<Token> = Vec::new();
    let mut lineno: usize = 1;

    let mut position_char: char;

    loop {
        if text.chars().nth(index).is_none() {
            break;
        };

        position_char = text.chars().nth(index).unwrap();

        if position_char == '\n' {
            index += 1;
            lineno += 1;
            continue;
        }

        if position_char.is_whitespace() {
            index += 1;
            continue;
        }

        if let Some(token_type) = OneCharToken::is_one_char_token(position_char) {
            tokens.push(Token::new(
                TokenType::OneChar(token_type),
                position_char.to_string(),
                lineno,
            ));
            index += 1;
            continue;
        }

        if index + 1 < text.len() {
            if let Some(token_type) =
                TwoCharToken::is_two_char_token(position_char, text.chars().nth(index + 1).unwrap())
            {
                tokens.push(Token::new(
                    TokenType::TwoChar(token_type),
                    format!("{}{}", position_char, text.chars().nth(index + 1).unwrap()),
                    lineno,
                ));
                index += 2;
                continue;
            }
        }
        index += 1;
    }

    tokens.push(Token::new(TokenType::EOF, "".to_string(), lineno));

    return tokens;
}
