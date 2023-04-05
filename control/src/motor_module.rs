use std::f32::consts::PI;
use std::path::Path;
use std::io::{BufReader, Error};
use std::fs::File;
use std::fmt::{Debug, Formatter};
use serialport::{SerialPortSettings, posix::TTYPort};

mod odrive;
pub use odrive::commands::{ODrive};
pub use odrive::enumerations::{AxisState, AxisID, ControlMode};

pub struct MotorModule {
    name: String,
    axis_id: AxisID,
    odrive: ODrive<TTYPort>,
    odrive_ready: bool,
    params: serde_json::Value,
}

impl Debug for MotorModule {
    fn fmt(&self, f: &mut Formatter) -> Result<(), std::fmt::Error> {
            write!(f, "Motor {{\n\tname:\t{:?} \n\taxis_id:\t{:?} \n\todrive:\t{:?} \n\todrive_ready:\t{:?} \n}}", self.name, self.axis_id, self.odrive, self.odrive_ready)
    }
}

impl MotorModule {
    pub fn new(name: String, axis_id: AxisID)-> Result<MotorModule, Error> {
        let file = File::open("./params.json").expect("file should open read only");
        let reader = BufReader::new(file);
        let params: serde_json::Value = serde_json::from_reader(reader).expect("file should be proper JSON");

        // Create serial port settings
        let mut settings = SerialPortSettings::default();
        // ODrive uses 115200 baud
        settings.baud_rate = 115_200;
        // Create serial port
        let serial = TTYPort::open(Path::new(params.get("PATHS").unwrap().get(name.to_ascii_uppercase() + "_USB").unwrap().as_str().unwrap()), &settings).expect("Failed to open usb port");
        // Create and return ODrive
        let odrive = ODrive::new(serial);

        Ok(MotorModule {
            name: name,
            axis_id: axis_id,
            odrive: odrive,
            odrive_ready: false,
            params: params,
        })
    }

    // Configure the motor
    // Use the params.json file to set the motor properties
    pub fn configure(&mut self)-> Result<(), Error> {
        println!("{}", self.odrive.get_config_property("encoder.config.cpr").unwrap().to_string());
        self.odrive.set_axis_property(self.axis_id, "controller.config.vel_limit", self.params.get("MOTORS").unwrap().get("VEL_LIMIT").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "encoder.config.cpr", self.params.get("MOTORS").unwrap().get("CPR").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "motor.config.pole_pairs", self.params.get("MOTORS").unwrap().get("POLE_PAIRS").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "motor.config.current_lim", self.params.get("MOTORS").unwrap().get("CURRENT_LIM").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "motor.config.calibration_current", self.params.get("MOTORS").unwrap().get("CURRENT_LIM").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "motor.config.resistance_calib_max_voltage", self.params.get("MOTORS").unwrap().get("CALIB_VOLTAGE_LIM").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "motor.config.torque_constant", self.params.get("MOTORS").unwrap().get("TORQUE_CONSTANT").unwrap()).unwrap();
        self.odrive.set_axis_property(self.axis_id, "config.startup_motor_calibration", false).unwrap();
        self.odrive.set_axis_property(self.axis_id, "config.startup_encoder_index_search", false).unwrap();
        self.odrive.set_axis_property(self.axis_id, "config.startup_encoder_offset_calibration", false).unwrap();
        self.odrive.set_axis_property(self.axis_id, "config.startup_closed_loop_control", false).unwrap();
        self.odrive.set_axis_property(self.axis_id, "config.startup_sensorless_control", false).unwrap();
        self.odrive.set_axis_property(self.axis_id, "encoder.config.use_index", false).unwrap();

        
        self.odrive.set_control_mode(self.axis_id, ControlMode::PositionControl).unwrap();
    
        self.odrive.save_configuration().unwrap();
        Ok(())
    }
    
    // Run the motor calibration routine
    pub fn calibrate(&mut self)-> Result<(), Error> {
        // Calibrate ODrive
        self.odrive.run_state(self.axis_id, AxisState::MotorCalibration, true).unwrap();
        // set motor pre calibrated
        self.odrive.set_motor_pre_calibrated(self.axis_id, true).unwrap();
        self.odrive.run_state(self.axis_id, AxisState::EncoderOffsetCalibration, true).unwrap();
        self.odrive.set_encoder_pre_calibrated(self.axis_id, true).unwrap();
        self.odrive.save_configuration().unwrap();
        Ok(())
    }

    // Arm the motor to be ready to move
    pub fn arm(&mut self)-> Result<(), Error> {
        // Arm ODrive
        self.odrive.run_state(self.axis_id, AxisState::ClosedLoopControl, false).unwrap();
        self.odrive_ready = true;
        Ok(())
    }

    // Set the motor position and velocity
    // Position is given in degrees
    pub fn set_position_and_velocity(&mut self, position: f32, velocity: f32)-> Result<(), Error> {
        // Set position and velocity
        // Position is in degrees, so convert to radians
        self.odrive.set_position_p(self.axis_id, position * PI / 180.0, Some(velocity), None).unwrap();
        Ok(())
    }

    pub fn is_ready(&self)-> bool {
        self.odrive_ready
    }
}

