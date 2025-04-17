#[cfg(test)]
mod test_lexer {
    use gox_compiler::lexer::{
        ControlKeyword, DeclarationKeyword, LiteralType, OneCharToken, TokenType, TwoCharToken,
        tokenize,
    };

    #[test]
    fn test_keywords() {
        let input = "if while const var";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 5);
        assert_eq!(
            tokens[0].token_type,
            TokenType::ControlKeyword(ControlKeyword::If)
        );
        assert_eq!(
            tokens[1].token_type,
            TokenType::ControlKeyword(ControlKeyword::While)
        );
        assert_eq!(
            tokens[2].token_type,
            TokenType::DeclarationKeyword(DeclarationKeyword::Const)
        );
        assert_eq!(
            tokens[3].token_type,
            TokenType::DeclarationKeyword(DeclarationKeyword::Var)
        );
    }

    #[test]
    fn test_literals() {
        let input = "123 3.14 true false 'a'";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 6);
        assert_eq!(
            tokens[0].token_type,
            TokenType::Literal(LiteralType::Integer)
        );
        assert_eq!(tokens[1].token_type, TokenType::Literal(LiteralType::Float));
        assert_eq!(tokens[2].token_type, TokenType::Literal(LiteralType::Bool));
        assert_eq!(tokens[3].token_type, TokenType::Literal(LiteralType::Bool));
        assert_eq!(tokens[4].token_type, TokenType::Literal(LiteralType::Char));
    }

    #[test]
    fn test_identifiers() {
        let input = "var x my_var _privateVar";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 5);
        assert_eq!(
            tokens[0].token_type,
            TokenType::DeclarationKeyword(DeclarationKeyword::Var)
        );
        assert_eq!(tokens[1].token_type, TokenType::Identifier);
        assert_eq!(tokens[2].token_type, TokenType::Identifier);
        assert_eq!(tokens[3].token_type, TokenType::Identifier);
    }

    #[test]
    fn test_one_char_operators() {
        let input = "+ - * / < > ^ = ; ( ) { } , ` !";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 17);
        assert_eq!(tokens[0].token_type, TokenType::OneChar(OneCharToken::Plus));
        assert_eq!(
            tokens[1].token_type,
            TokenType::OneChar(OneCharToken::Minus)
        );
        assert_eq!(
            tokens[2].token_type,
            TokenType::OneChar(OneCharToken::Times)
        );
        assert_eq!(
            tokens[3].token_type,
            TokenType::OneChar(OneCharToken::Divide)
        );
        assert_eq!(
            tokens[4].token_type,
            TokenType::OneChar(OneCharToken::Lt)
        );
        assert_eq!(
            tokens[5].token_type,
            TokenType::OneChar(OneCharToken::Gt)
        );

        assert_eq!(
            tokens[6].token_type,
            TokenType::OneChar(OneCharToken::Grow)
        );
        assert_eq!(
            tokens[7].token_type,
            TokenType::OneChar(OneCharToken::Assign)
        );
        assert_eq!(
            tokens[8].token_type,
            TokenType::OneChar(OneCharToken::Semi)
        );
        assert_eq!(
            tokens[9].token_type,
            TokenType::OneChar(OneCharToken::LParen)
        );
        assert_eq!(
            tokens[10].token_type,
            TokenType::OneChar(OneCharToken::RParen)
        );
        assert_eq!(
            tokens[11].token_type,
            TokenType::OneChar(OneCharToken::LBrace)
        );
        assert_eq!(
            tokens[12].token_type,
            TokenType::OneChar(OneCharToken::RBrace)
        );
        assert_eq!(
            tokens[13].token_type,
            TokenType::OneChar(OneCharToken::Comma)
        );
        assert_eq!(
            tokens[14].token_type,
            TokenType::OneChar(OneCharToken::Deref)
        );
        assert_eq!(
            tokens[15].token_type,
            TokenType::OneChar(OneCharToken::Not)
        );
    }

    #[test]
    fn test_two_char_operators() {
        let input = "&& || <= >= == !=";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 7);
        assert_eq!(tokens[0].token_type, TokenType::TwoChar(TwoCharToken::Land));
        assert_eq!(tokens[1].token_type, TokenType::TwoChar(TwoCharToken::Lor));
        assert_eq!(tokens[2].token_type, TokenType::TwoChar(TwoCharToken::Le));
        assert_eq!(tokens[3].token_type, TokenType::TwoChar(TwoCharToken::Ge));
        assert_eq!(tokens[4].token_type, TokenType::TwoChar(TwoCharToken::Eq));
        assert_eq!(tokens[5].token_type, TokenType::TwoChar(TwoCharToken::Ne));
    }

    #[test]
    fn test_whitespace_and_newlines() {
        let input = "if   x > 10 \n while x < 5";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 9);
        assert_eq!(
            tokens[0].token_type,
            TokenType::ControlKeyword(ControlKeyword::If)
        );
        assert_eq!(tokens[1].token_type, TokenType::Identifier);
        assert_eq!(tokens[2].token_type, TokenType::OneChar(OneCharToken::Gt));
        assert_eq!(
            tokens[3].token_type,
            TokenType::Literal(LiteralType::Integer)
        );
        assert_eq!(
            tokens[4].token_type,
            TokenType::ControlKeyword(ControlKeyword::While)
        );
        assert_eq!(tokens[5].token_type, TokenType::Identifier);
    }

    #[test]
    fn test_unknown_characters() {
        let input = "@ # $ % ^ as.a &";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 8);
        assert_eq!(tokens[0].token_type, TokenType::Illegal);
        assert_eq!(tokens[1].token_type, TokenType::Illegal);
        assert_eq!(tokens[2].token_type, TokenType::Illegal);
        assert_eq!(tokens[3].token_type, TokenType::Illegal);
        assert_eq!(tokens[4].token_type, TokenType::OneChar(OneCharToken::Grow));
        assert_eq!(tokens[5].token_type, TokenType::Illegal);
        assert_eq!(tokens[6].token_type, TokenType::Illegal);
    }

    #[test]
    fn test_eof_token() {
        let input = "var x = 10";
        let tokens = tokenize(input);

        assert_eq!(tokens[tokens.len() - 1].token_type, TokenType::EOF);
    }

    #[test]
    fn test_comments() {
        let input = "// This is a comment\n var x = 10 // another comment";
        let tokens = tokenize(input);

        assert_eq!(tokens.len(), 5); // El número de tokens no debe contar los comentarios
        assert_eq!(
            tokens[0].token_type,
            TokenType::DeclarationKeyword(DeclarationKeyword::Var)
        );
        assert_eq!(tokens[1].token_type, TokenType::Identifier);
        assert_eq!(
            tokens[2].token_type,
            TokenType::OneChar(OneCharToken::Assign)
        );
        assert_eq!(
            tokens[3].token_type,
            TokenType::Literal(LiteralType::Integer)
        );
    }
}
