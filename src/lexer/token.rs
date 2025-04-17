use regex::Regex;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Token {
    pub token_type: TokenType,
    pub value: String,
    pub lineno: usize,
}

impl Token {
    pub fn new(token_type: TokenType, value: String, lineno: usize) -> Token {
        Token {
            token_type,
            value,
            lineno,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TokenType {
    TwoChar(TwoCharToken),
    OneChar(OneCharToken),
    Literal(LiteralType),
    ControlKeyword(ControlKeyword),
    DeclarationKeyword(DeclarationKeyword),
    BuiltinKeyword(BuiltinKeyword),
    Identifier,
    EOF,
    Illegal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LiteralType {
    Integer,
    Float,
    Bool,
    Char,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ControlKeyword {
    If,
    Else,
    While,
    Break,
    Continue,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DeclarationKeyword {
    Var,
    Const,
    Func,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BuiltinKeyword {
    Print,
    Return,
    Import,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TwoCharToken {
    Land,
    Lor,
    Le,
    Ge,
    Eq,
    Ne,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OneCharToken {
    Plus,
    Minus,
    Times,
    Divide,
    Lt,
    Gt,
    Grow,
    Assign,
    Semi,
    LParen,
    RParen,
    LBrace,
    RBrace,
    Comma,
    Deref,
    Not,
}

impl OneCharToken {
    pub fn is_one_char_token(c: char) -> Option<OneCharToken> {
        match c {
            '+' => Some(OneCharToken::Plus),
            '-' => Some(OneCharToken::Minus),
            '*' => Some(OneCharToken::Times),
            '/' => Some(OneCharToken::Divide),
            '<' => Some(OneCharToken::Lt),
            '>' => Some(OneCharToken::Gt),
            '^' => Some(OneCharToken::Grow),
            '=' => Some(OneCharToken::Assign),
            ';' => Some(OneCharToken::Semi),
            '(' => Some(OneCharToken::LParen),
            ')' => Some(OneCharToken::RParen),
            '{' => Some(OneCharToken::LBrace),
            '}' => Some(OneCharToken::RBrace),
            ',' => Some(OneCharToken::Comma),
            '`' => Some(OneCharToken::Deref),
            '!' => Some(OneCharToken::Not),
            _ => None,
        }
    }
}

impl TwoCharToken {
    pub fn is_two_char_token(char1: char, char2: char) -> Option<TwoCharToken> {
        match (char1, char2) {
            ('&', '&') => Some(TwoCharToken::Land),
            ('|', '|') => Some(TwoCharToken::Lor),
            ('<', '=') => Some(TwoCharToken::Le),
            ('>', '=') => Some(TwoCharToken::Ge),
            ('=', '=') => Some(TwoCharToken::Eq),
            ('!', '=') => Some(TwoCharToken::Ne),
            _ => None,
        }
    }
}

impl TokenType {
    pub fn from_literal(s: &str) -> Option<TokenType> {
        let is_integer = Regex::new(r"^\d+$").unwrap();
        let is_float = Regex::new(r"^\d+\.\d+$").unwrap();
        let is_identifier = Regex::new(r"^[a-zA-Z_][a-zA-Z0-9_]*$").unwrap();
        let is_char = Regex::new(r"^'.'$").unwrap();

        match s.to_lowercase().as_str() {
            "if" => Some(TokenType::ControlKeyword(ControlKeyword::If)),
            "else" => Some(TokenType::ControlKeyword(ControlKeyword::Else)),
            "while" => Some(TokenType::ControlKeyword(ControlKeyword::While)),
            "break" => Some(TokenType::ControlKeyword(ControlKeyword::Break)),
            "continue" => Some(TokenType::ControlKeyword(ControlKeyword::Continue)),

            "var" => Some(TokenType::DeclarationKeyword(DeclarationKeyword::Var)),
            "const" => Some(TokenType::DeclarationKeyword(DeclarationKeyword::Const)),
            "func" => Some(TokenType::DeclarationKeyword(DeclarationKeyword::Func)),

            "print" => Some(TokenType::BuiltinKeyword(BuiltinKeyword::Print)),
            "return" => Some(TokenType::BuiltinKeyword(BuiltinKeyword::Return)),
            "import" => Some(TokenType::BuiltinKeyword(BuiltinKeyword::Import)),

            s if s == "true" || s == "false" => Some(TokenType::Literal(LiteralType::Bool)),
            s if is_integer.is_match(s) => Some(TokenType::Literal(LiteralType::Integer)),
            s if is_float.is_match(s) => Some(TokenType::Literal(LiteralType::Float)),
            s if is_char.is_match(s) => Some(TokenType::Literal(LiteralType::Char)),
            s if is_identifier.is_match(s) => Some(TokenType::Identifier),
            _ => None,
        }
    }
}
