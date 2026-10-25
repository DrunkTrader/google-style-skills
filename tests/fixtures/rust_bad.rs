use std::*;

pub fn open_path(path: &String) -> bool {
    std::fs::metadata(path).is_ok()
}
