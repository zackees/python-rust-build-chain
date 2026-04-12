use pyo3::prelude::*;

/// Add two numbers.
#[pyfunction]
fn add(left: i64, right: i64) -> i64 {
    my_project_core::add(left, right)
}

/// Return the native library version.
#[pyfunction]
fn version() -> &'static str {
    my_project_core::version()
}

/// The native extension module.
#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
