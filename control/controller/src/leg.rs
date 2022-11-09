use std::fmt::Debug;
use std::fmt::Formatter;
use std::fs::File;
use std::io::{BufReader, Error, ErrorKind};
use std::f32::consts::PI;
use nalgebra::{Vector3, Rotation3};
use odrive_rs::enumerations::AxisID;

//mod setup;


pub struct Leg {
        foot_pos: Vector3<f32>,
        odrives_ready: bool,
        shoulder: AxisID,
        arm: AxisID,
        forearm: AxisID,
        shoulder_pos: Vector3<f32>,
        arm_pos: Vector3<f32>,
        forearm_pos: Vector3<f32>,
        shoulder_angle: f32,
        arm_angle: f32,
        forearm_angle: f32,
        arm_vertical_pos: Vector3<f32>,
        forearm_vertical_pos: Vector3<f32>,
        foot_vertical_pos: Vector3<f32>,
        params: serde_json::Value
}


impl Debug for Leg {
        fn fmt(&self, f: &mut Formatter) -> Result<(), std::fmt::Error> {
                write!(f, "Leg {{\n\tfoot_pos:\t{:?} \n\tshoulder_angle:\t{:?} \n\tarm_angle:\t{:?} \n\tforearm_angle:\t{:?} \n}}", self.foot_pos, self.shoulder_angle, self.arm_angle, self.forearm_angle)
        }
}

impl Leg {
        /*
        Initialize the leg
        foot_position : position of foot
        */
        pub fn new(foot_position: Vector3<f32>) -> Self {
                let mut new_leg = Leg {
                        foot_pos: foot_position,
                        odrives_ready: false,
                        shoulder: AxisID::Zero,
                        arm: AxisID::Zero,
                        forearm: AxisID::Zero,
                        shoulder_pos: Vector3::zeros(),
                        arm_pos: Vector3::zeros(),
                        forearm_pos: Vector3::zeros(),
                        shoulder_angle: 0.0,
                        arm_angle: 0.0,
                        forearm_angle: 0.0,
                        arm_vertical_pos: Vector3::zeros(),
                        foot_vertical_pos: Vector3::zeros(),
                        forearm_vertical_pos: Vector3::zeros(),
                        params: serde_json::Value::Null
                };


                // read params json file located "./params.json"
                let file = File::open("./params.json").expect("file should open read only");
                let reader = BufReader::new(file);
                new_leg.params = serde_json::from_reader(reader).expect("file should be proper JSON");

                match new_leg.update_positions() {
                        Ok(_) => (),
                        Err(e) => println!("Error: {:?}", e)
                }

                if new_leg.params.get("MODE").unwrap() == "motor" {
                        // TO DO: find and setup odrives cards
                        println!("Odrives not yet implemented");
                } else {
                        println!("Simulation mode");
                        new_leg.odrives_ready = false;
                }
                return new_leg;
        }

        /*
        Calibrate the leg
        */
        pub fn calibrate(&self) -> Result<(), Error> {
                /*
                if self.odrives_ready {
                        println!("Calibrating :");

                        // Calibrate shoulder
                        println!("	shoulder...  ");
                        let mut attempt = 1;
                        while !self.shoulder.motor.is_calibrated {
                                println!("		status : {:?} ", self.shoulder.motor.is_calibrated);
                                if attempt > 3 {
                                        return Err(Error::new(ErrorKind::Other, "Calibration failed on shoulder"));
                                }
                                run_calibration(self.shoulder);
                                attempt += 1;
                                sleep(10);
                        }
                        sleep(5);
                        println!("		status : {:?} ", self.shoulder.motor.is_calibrated);
                        
                        // Calibrate arm
                        println!("	arm...  ");
                        attempt = 1;
                        while !self.arm.motor.is_calibrated {
                                println!("		status : {:?} ", self.arm.motor.is_calibrated);
                                if attempt > 3 {
                                        return Err(Error::new(ErrorKind::Other, "Calibration failed on arm"));
                                }
                                run_calibration(self.arm);
                                attempt += 1;
                                sleep(10);
                        }
                        sleep(5);
                        println!("		status : {:?} ", self.arm.motor.is_calibrated);
                        
                        // Calibrate forearm
                        println!("	forearm...");
                        attempt = 1;
                        while !self.forearm.motor.is_calibrated {
                                println!("		status : {:?} ", self.forearm.motor.is_calibrated);
                                if attempt > 3 {
                                        return Err(Error::new(ErrorKind::Other, "Calibration failed on forearm"));
                                }
                                run_calibration(self.forearm);
                                attempt += 1;
                                sleep(10);
                        }
                        sleep(5);
                        println!("		status : {:?} ", self.forearm.motor.is_calibrated);
                        
                        println!("Calibration done !");

                        blocked_motor_mode(self.shoulder);
                        blocked_motor_mode(self.arm);
                        blocked_motor_mode(self.forearm);
                        println!("Motors blocked !");
                } else {
                        return Err(Error::new(ErrorKind::Other, "ODrives not Ready"));
                }
                */
                return Ok(());
        }

        /*
        Set the foot position, and update all leg properties
        foot_position : New position of the foot
        */
        pub fn set_foot_position(&mut self, foot_position: &Vector3<f32>) -> Result<(), Error> {
                // get state in memory
                let leg_copy = Leg {
                        foot_pos: self.foot_pos,
                        odrives_ready: self.odrives_ready,
                        shoulder: self.shoulder,
                        arm: self.arm,
                        forearm: self.forearm,
                        shoulder_pos: self.shoulder_pos,
                        arm_pos: self.arm_pos,
                        forearm_pos: self.forearm_pos,
                        shoulder_angle: self.shoulder_angle,
                        arm_angle: self.arm_angle,
                        forearm_angle: self.forearm_angle,
                        arm_vertical_pos: self.arm_vertical_pos,
                        foot_vertical_pos: self.foot_vertical_pos,
                        forearm_vertical_pos: self.forearm_vertical_pos,
                        params: self.params.clone()
                };

                // update foot position
                self.foot_pos = foot_position.clone();

                // calcul all others positions
                let err = self.update_positions();
                if err.is_err() {
                        *self = leg_copy;
                        return Err(Error::new(ErrorKind::Other, "Error while setting foot position. Previous state restored !"));
                }

                return Ok(());
        }

        /*
        Update all leg positions
        The order is very important
        */
        pub fn update_positions(&mut self) -> Result<(), Error> {
                self.shoulder_pos = Vector3::new(0 as f32, 0 as f32, 0 as f32);
                match self.calcul_arm_position() {
                        Ok(_) => (),
                        Err(e) => return Err(e)
                }
                match self.calcul_shoulder_angle() {
                        Ok(_) => (),
                        Err(e) => return Err(e)
                }

                // To simplify the next calculations we simulate a rotation of shoulder to have the arm verticaly.
                self.arm_vertical_pos = Rotation3::from_axis_angle(&Vector3::y_axis(), self.shoulder_angle) * self.arm_pos;
                self.foot_vertical_pos = Rotation3::from_axis_angle(&Vector3::y_axis(), self.shoulder_angle) * self.foot_pos;
                
                match self.calcul_forearm_position() {
                        Ok(_) => (),
                        Err(e) => return Err(e)
                }
                match self.calcul_arm_angle() {
                        Ok(_) => (),
                        Err(e) => return Err(e)
                }
                match self.calcul_forearm_angle() {
                        Ok(_) => (),
                        Err(e) => return Err(e)
                }

                if self.odrives_ready {
                        // Update the motors positions
                        // self.shoulder.controller.input_pos = ((self.shoulder_angle/360)/REDUCTION_COEF);
                        // self.arm.controller.input_pos = ((self.arm_angle/360)/REDUCTION_COEF);
                        // self.forearm.controller.input_pos = ((self.forearm_angle/360)/REDUCTION_COEF);
                }
                return Ok(());
        }

        /*
        Calculates the Arm position from the foot position
        Link used : https://stackoverflow.com/a/49987361
        */
        fn calcul_arm_position(&mut self) -> Result<(), Error> {
                // (Px, Py) = (self.foot_pos.x, self.foot_pos.z);
                // (Cx, Cy) = (self.shoulder_pos.x, self.shoulder_pos.z);
                let a = self.params.get("LEG").unwrap().get("SHOULDER_LENGTH").unwrap().as_f64().unwrap() as f32;
                let b = ((self.foot_pos.x - self.shoulder_pos.x).powi(2) + (self.foot_pos.z - self.shoulder_pos.z).powi(2)).sqrt();
                let th = (a / b).acos(); // angle theta
                let d = (self.foot_pos.z - self.shoulder_pos.z).atan2(self.foot_pos.x - self.shoulder_pos.x);
                let d1 = d + th; // direction angle of point 1
                let d2 = d - th; // direction angle of point 2
                let t1x = self.shoulder_pos.x + (a*d1.cos());
                let t2x = self.shoulder_pos.x + (a*d2.cos());
                
                // take the bigest x value as the arm position
                if t1x < t2x {
                        // Do a virtual rotation of axes to fit the result with general coordinates
                        self.arm_pos = Vector3::new(t2x as f32, 0 as f32, (self.shoulder_pos.z + (a*d2.sin())) as f32);
                } else {
                        // Do a virtual rotation of axes to fit the result with general coordinates
                        self.arm_pos = Vector3::new(t1x as f32, 0 as f32, (self.shoulder_pos.z + (a*d1.sin())) as f32);
                }

                return Ok(());
        }

        /*
        Calculates the Shoulder angle from the arm position
        Use SOHCAHTOA method
        */
        fn calcul_shoulder_angle(&mut self) -> Result<(), Error> {
                let adj = self.arm_pos.x - self.shoulder_pos.x;
                let hyp = self.params.get("LEG").unwrap().get("SHOULDER_LENGTH").unwrap().as_f64().unwrap() as f32;
                // Calculate the angle : cos(angle) = adj / hyp => angle = acos(adj / hyp)
                self.shoulder_angle = -((adj/hyp).acos() * 180.0f32 / PI); // * 180.0f32 / PI -> to convert to degrees
                return Ok(());
        }

        /*
        Calculates the Forearm position from the foot position and the arm position
        APF points : A->Arm, P->Foot, F->Forearm
        Work in 3D space (x, y, z)
        How it's working :
                1) Covert to 2D the y and z coordinates of the vertical arm -> (temporarily renamed 'x' and 'y')
                2) We calculate intersections between the circle around A and around P.
                3) Get the intersection have the lowest x value.
                4) Reconvert the intersection result to the 3D space. And reverse rotation.
        */
        fn calcul_forearm_position(&mut self) -> Result<(), Error> {
                // Parameters for the calculations
                let p_radius = self.params.get("LEG").unwrap().get("FOREARM_LENGTH").unwrap().as_f64().unwrap() as f32;
                let a_radius = self.params.get("LEG").unwrap().get("ARM_LENGTH").unwrap().as_f64().unwrap() as f32;

                // 1) Convert to "2D" space
                let p_point = Vector3::new(self.foot_vertical_pos.y as f32, self.foot_vertical_pos.z as f32, 0 as f32);
                let a_point = Vector3::new(self.arm_vertical_pos.y as f32, self.arm_vertical_pos.z as f32, 0 as f32);
                
                // 2) We calculate intersections between the circle around A and around P.
                let delta = ((a_point.x - p_point.x).powi(2) + (a_point.y - p_point.y).powi(2)).sqrt();
                // no intersecting
                if delta > (p_radius + a_radius) {
                        return Err(Error::new(ErrorKind::Other, "No intersecting"));
                }
                // one circle within other
                if delta < (p_radius - a_radius).abs() {
                        return Err(Error::new(ErrorKind::Other, "No intersecting"));
                }
                // coincident circles
                if delta == 0.0 && p_radius == a_radius {
                        return Err(Error::new(ErrorKind::Other, "No intersecting"));
                }

                let a = ((p_radius.powi(2) - a_radius.powi(2)) + delta.powi(2))/(2.0*delta);
                let h = (p_radius.powi(2) - a.powi(2)).sqrt();
                let x2 = p_point.x + ((a*(a_point.x - p_point.x))/delta);
                let y2 = p_point.y + ((a*(a_point.y - p_point.y))/delta);

                // 3) Get the intersection have the lowest x value.
                let x3 = x2 + ((h*(a_point.y - p_point.y))/delta);
                let x4 = x2 - ((h*(a_point.y - p_point.y))/delta);
                let intersection_point: Vector3<f32>;
                if x3 < x4 {
                        intersection_point = Vector3::new(x3 as f32, (y2 - ((h*(a_point.x - p_point.x))/delta)) as f32, 0 as f32);
                } else {
                        intersection_point = Vector3::new(x4 as f32, (y2 + ((h*(a_point.x - p_point.x))/delta)) as f32, 0 as f32);
                }

                // 4) Reconvert the intersection result to the 3D space.
                self.forearm_vertical_pos = Vector3::new(self.params.get("LEG").unwrap().get("SHOULDER_LENGTH").unwrap().as_f64().unwrap() as f32, intersection_point.x, intersection_point.y);
                // Reverse rotation
                self.forearm_pos = Rotation3::from_axis_angle(&Vector3::y_axis(), -(self.shoulder_angle)) * self.forearm_vertical_pos;

                return Ok(());
        }

        /*
        Calculates the Arm angle from the arm position and forearm position
        Use SOHCAHTOA method
        */
        fn calcul_arm_angle(&mut self) -> Result<(), Error> {
                let a = vec![0.0, -100.0];
                let b = vec![self.arm_vertical_pos.y, self.arm_vertical_pos.z];
                let c = vec![self.forearm_vertical_pos.y, self.forearm_vertical_pos.z];
                self.arm_angle = 0.0 - (((c[1] - b[1]).atan2(c[0] - b[0]) - (a[1] - b[1]).atan2(a[0] - b[0]))) * 180.0f32 / PI; // * 180.0f32 / PI is to convert radian to degrees
                return Ok(());
        }

        /*
        Calculates the Forearm angle from the forearm position
        */
        fn calcul_forearm_angle(&mut self) -> Result<(), Error> {
                let a = vec![self.arm_vertical_pos.y, self.arm_vertical_pos.z];
                let b = vec![self.forearm_vertical_pos.y, self.forearm_vertical_pos.z];
                let c = vec![self.foot_vertical_pos.y, self.foot_vertical_pos.z];
                self.forearm_angle = -180.0 - (((c[1] - b[1]).atan2(c[0] - b[0]) - (a[1] - b[1]).atan2(a[0] - b[0]))) * 180.0f32 / PI; // * 180.0f32 / PI is to convert radian to degrees
                return Ok(());
        }
}