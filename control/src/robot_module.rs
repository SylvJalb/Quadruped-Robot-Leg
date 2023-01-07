use nalgebra::{Vector3};
use std::io::{Error, ErrorKind};

use motor_module::{AxisID};

// import the joint block module
#[path = "./motor_module.rs"] mod motor_module;
use motor_module::{MotorModule};
// import leg module
#[path = "./leg_module.rs"] mod leg_module;
use leg_module::{LegModule};

pub struct RobotModule {
    leg: LegModule,

    // odrives stuff
    odrives_ready: bool,
    shoulder_joint: MotorModule,
    arm_joint: MotorModule,
    forearm_joint: MotorModule,
}

impl RobotModule {
    pub fn new(foot_position: Vector3<f32>) -> Self {
        RobotModule {
            leg: LegModule::new(foot_position),

            // odrives stuff
            odrives_ready: false,
            shoulder_joint: MotorModule::new("shoulder".to_owned(), AxisID::Zero).expect("Error creating shoulder joint"),
            arm_joint: MotorModule::new("arm".to_owned(), AxisID::Zero).expect("Error creating arm joint"),
            forearm_joint: MotorModule::new("forearm".to_owned(), AxisID::One).expect("Error creating forearm joint"),
        }
    }

    pub fn init_robot(&mut self) -> Result<(), Error> {
        // init the odrives
        self.shoulder_joint.configure().expect("Error setting up shoulder joint");
        self.arm_joint.configure().expect("Error setting up arm joint");
        self.forearm_joint.configure().expect("Error setting up forearm joint");

        self.shoulder_joint.calibrate().expect("Error during shoulder calibration");
        self.arm_joint.calibrate().expect("Error during arm calibration");
        self.forearm_joint.calibrate().expect("Error during forearm calibration");

        self.shoulder_joint.arm().expect("Error during shoulder arming");
        self.arm_joint.arm().expect("Error during arm arming");
        self.forearm_joint.arm().expect("Error during forearm arming");

        // check if the odrives are ready
        self.odrives_ready = self.shoulder_joint.is_ready() && self.arm_joint.is_ready() && self.forearm_joint.is_ready();

        if self.odrives_ready {
            println!("Odrives are ready");
            return Ok(());
        } else {
            return Err(Error::new(ErrorKind::Other, "Odrives not ready"));
        }
    }

    pub fn set_foot_position(&mut self, foot_position: &Vector3<f32>) -> Result<(), Error> {
        if self.odrives_ready {
            // set the foot position
            self.leg.set_foot_position(foot_position).expect("Error when foot position is calculated");

            // Update the motors positions
            self.shoulder_joint.set_position_and_velocity(self.leg.get_shoulder_angle(), 3.0)
                .expect("Error setting shoulder position");
            self.arm_joint.set_position_and_velocity(self.leg.get_arm_angle(), 3.0)
                .expect("Error setting arm position");
            self.forearm_joint.set_position_and_velocity(self.leg.get_forearm_angle(), 3.0)
                .expect("Error setting forearm position");
        } else {
            return Err(Error::new(ErrorKind::Other, "Odrives not ready"));
        }
        Ok(())
    }

    pub fn get_leg(&self) -> &LegModule {
        &self.leg
    }

}