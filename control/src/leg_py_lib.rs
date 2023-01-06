use nalgebra::Vector3;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyFloat};

#[path = "./leg_module.rs"] mod leg_module;
use leg_module::{LegModule};

#[pymodule]
fn leg_controller(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<LegPy>()?;
    Ok(())
}

#[pyclass]
pub struct LegPy {
    leg: LegModule
}

#[pymethods]
impl LegPy {
    #[new]
    fn new(foot_position: &PyList) -> Self {
        let v: Vec<f32> = foot_position.extract().unwrap();
        LegPy {
            leg: LegModule::new(Vector3::new(v[0], v[1], v[2]))
        }
    }

    // Get the string infos of the leg
    fn to_string(&self) -> String {
        format!("{:?}", self.leg)
    }

    // Setters
    fn set_foot_position(&mut self, foot_position: &PyList) -> PyResult<()> {
        let v: Vec<f32> = foot_position.extract()?;
        match self.leg.set_foot_position(&Vector3::new(v[0], v[1], v[2])) {
            Ok(_) => Ok(()),
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyException, _>(e)),
        }
    }

    // Positions Getters
    fn get_foot_position(&self) -> PyResult<Py<PyList>> {
        Python::with_gil(|py| {
            let list = PyList::new(py, &self.leg.get_foot_position());
            Ok(list.into())
        })
    }
    fn get_forearm_position(&self) -> PyResult<Py<PyList>> {
        Python::with_gil(|py| {
            let list = PyList::new(py, &self.leg.get_forearm_position());
            Ok(list.into())
        })
    }
    fn get_arm_position(&self) -> PyResult<Py<PyList>> {
        Python::with_gil(|py| {
            let list = PyList::new(py, &self.leg.get_arm_position());
            Ok(list.into())
        })
    }
    fn get_shoulder_position(&self) -> PyResult<Py<PyList>> {
        Python::with_gil(|py| {
            let list = PyList::new(py, &self.leg.get_shoulder_position());
            Ok(list.into())
        })
    }

    // Angles Getters
    fn get_forearm_angle(&self) -> PyResult<Py<PyFloat>> {
        Python::with_gil(|py| {
            let angle = PyFloat::new(py, self.leg.get_forearm_angle().into());
            Ok(angle.into())
        })
    }
    fn get_arm_angle(&self) -> PyResult<Py<PyFloat>> {
        Python::with_gil(|py| {
            let angle = PyFloat::new(py, self.leg.get_arm_angle().into());
            Ok(angle.into())
        })
    }
    fn get_shoulder_angle(&self) -> PyResult<Py<PyFloat>> {
        Python::with_gil(|py| {
            let angle = PyFloat::new(py, self.leg.get_shoulder_angle().into());
            Ok(angle.into())
        })
    }
}