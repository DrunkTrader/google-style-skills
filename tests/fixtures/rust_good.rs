use std::path::Path;

/// Opens a path and reports an expected I/O failure to the caller.
pub fn open_path(path: &Path) -> Result<(), std::io::Error> {
    std::fs::metadata(path).map(|_| ())
}
