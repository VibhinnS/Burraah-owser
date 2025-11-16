use pyo3::prelude::*;

#[pyfunction]
fn compute_layout(text: &str, width: i32, hstep: i32, vstep: i32) -> PyResult<Vec<(i32, i32, char)>> {
    let mut cursor_x = hstep;
    let mut cursor_y = vstep;
    let mut result = Vec::new();

    for character in text.chars() {
        if cursor_x >= width {
            cursor_y += vstep;
            cursor_x = hstep;
        }
        result.push((cursor_x, cursor_y, character));
        cursor_x += hstep;
        }
        Ok(result)
    }

#[pymodule]
fn layout_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compute_layout,m)?)?;
    Ok(())
}