use nalgebra::Vector3;

mod robot_module;
use robot_module::RobotModule;

fn main() {
    // create a new Leg instance
    let mut my_robot = RobotModule::new(Vector3::new(120.0, 50.0, -425.0));
    println!("{:?}", my_robot.get_leg());

    // init the robot
    my_robot.init_robot().expect("Error during robot initialization");

    // RUN A SIMPLE TEST
    // loop and go to an given position
    // my_robot.set_foot_position(&Vector3::new(120.0, number as f32, -425.0))
    //     .expect("Error setting foot position");
    loop {
        for number in -50..50 {
            my_robot.set_foot_position(&Vector3::new(120.0, number as f32, -425.0))
                .expect("Error setting foot position");
            println!("{:?}", my_robot.get_leg());
        }
        for number in (-50..50).rev() {
            my_robot.set_foot_position(&Vector3::new(120.0, number as f32, -425.0))
                .expect("Error setting foot position");
            println!("{:?}", my_robot.get_leg());
        }
    }
}
