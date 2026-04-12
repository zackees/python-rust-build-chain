/// Add two numbers. This is a placeholder for the real logic.
pub fn add(left: i64, right: i64) -> i64 {
    left + right
}

/// Return the library version.
pub fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn test_version() {
        assert_eq!(version(), "0.1.0");
    }
}
