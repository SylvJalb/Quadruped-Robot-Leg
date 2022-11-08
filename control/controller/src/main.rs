use nalgebra::Vector3;
#[path = "./services/leg.rs"] pub mod leg;

fn main() {
    // create a new Leg instance
    let mut leg = leg::Leg::new(Vector3::new(120 as f32, 50 as f32, -425 as f32));

    println!("{:?}", leg);
}
