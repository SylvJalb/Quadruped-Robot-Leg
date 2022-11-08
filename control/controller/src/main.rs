use nalgebra::Vector3;
#[path = "./services/leg.rs"] pub mod leg;

fn main() {
    // create a new Leg instance
    let mut leg = leg::Leg::new(Vector3::new(120.0, 50.0, -425.0));
    println!("{:?}", leg);

    // RUN A SIMPLE TEST
    // loop from -100 to 50 with a step of 10
    for i in (-100..51).step_by(10) {
        // move the leg
        match leg.set_foot_position(&Vector3::new(120.0, i as f32, -425.0)) {
            Ok(_) => println!("{:?}", leg),
            Err(e) => println!("Error: {}", e),
        }
    }
}
