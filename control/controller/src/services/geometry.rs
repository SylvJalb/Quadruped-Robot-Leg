use nalgebra::{Vector3, Rotation3};

/*
Rotate a vector around an axis by a given angle
*/
pub fn rotate_around_axis(pos: &Vector3<f32>, angle: f32, axis: &Vector3<u8>) -> Vector3<f32> {
    let rotation = Rotation3::from_axis_angle(axis, angle);
    rotation * pos
}