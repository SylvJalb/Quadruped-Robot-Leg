use nalgebra::Vector3;
use pyo3::prelude::*;
use pyo3::types::PyList;
pub mod leg;

#[pymodule]
fn leg_controller(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<LegPy>()?;
    Ok(())
}

#[pyclass]
pub struct LegPy {
    leg: leg::Leg,
}

#[pymethods]
impl LegPy {
    #[new]
    fn new(foot_position: &PyList) -> Self {
        let v: Vec<f32> = foot_position.extract().unwrap();
        LegPy {
            leg: leg::Leg::new(Vector3::new(v[0], v[1], v[2])),
        }
    }
    fn set_foot_position(&mut self, foot_position: &PyList) -> PyResult<()> {
        let v: Vec<f32> = foot_position.extract()?;
        match self.leg.set_foot_position(&Vector3::new(v[0], v[1], v[2])) {
            Ok(_) => Ok(()),
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyException, _>(e)),
        }
    }
    fn to_string(&self) -> String {
        format!("{:?}", self.leg)
    }
}