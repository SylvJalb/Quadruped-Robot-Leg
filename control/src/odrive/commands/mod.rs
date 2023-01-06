use std::fmt::Display;
use std::io::{BufReader, Error, Read, Write};
use std::io;
use std::time::Instant;

use super::enumerations::{AxisID, AxisState, ControlMode, EncoderMode};
use super::enumerations::errors::{ODriveError, ODriveResult};

/// The `ODrive` struct manages a connection with an ODrive motor over the ASCII protocol.
/// It acts as a newtype around a connection stream.
/// This has been tested using serial types from `serialport-rs`.
#[derive(Debug)]
pub struct ODrive<T> where T: Read {
    io_stream: BufReader<T>,
}

impl<T> ODrive<T> where T: Read {
    /// Although any type can be passed in here, it is suggested that the supplied type `T` be
    /// `Read + Write`. Doing so will unlock the full API.
    pub fn new(io_stream: T) -> Self {
        Self {
            io_stream: BufReader::new(io_stream)
        }
    }
}

/// An implementation of `Write` has been provided as an escape hatch to enable the usage of
/// operations not yet supported by this library.
impl<T> Write for ODrive<T> where T: Write + Read {
    fn write(&mut self, buf: &[u8]) -> Result<usize, Error> {
        self.io_stream.get_mut().write(buf)
    }

    fn flush(&mut self) -> Result<(), Error> {
        self.io_stream.get_mut().flush()
    }
}

/// An implementation of `Write` has been provided as an escape hatch to enable the usage of
/// operations not yet supported by this library. Be advised that using this implementation may
/// place the connection into an inconsistent state.
impl<T> Read for ODrive<T> where T: Read {
    fn read(&mut self, buf: &mut [u8]) -> Result<usize, Error> {
        self.io_stream.read(buf)
    }
}

impl<T> ODrive<T> where T: Read {
    /// Reads the next message sent by the ODrive as a string.
    /// If their is no message, this function should return `None`
    ///
    /// It is suggested that you only use this if you are directly using the `Write` implementation
    /// and are expecting a response, as normally the supplied for the ODrive can directly support
    /// reading any response.
    pub fn read_string(&mut self) -> io::Result<Option<String>> {
        let mut string = String::with_capacity(20);
        let duration = Instant::now();
        loop {
            let mut buffer = [0; 1];
            while self.read(&mut buffer).unwrap_or_default() == 0 {
                if duration.elapsed().as_millis() >= 1_000 {
                    return Ok(None);
                }
            }
            let ch = buffer[0];
            if ch as char == '\n' {
                break;
            }

            string.push(ch as char);
        }

        Ok(Some(string.trim().to_owned()))
    }

    pub fn read_odrive_response(&mut self) -> ODriveResult<String> {
        let mut string = String::with_capacity(20);
        let duration = Instant::now();
        loop {
            let mut buffer = [0; 1];
            while self.read(&mut buffer).unwrap_or_default() == 0 {
                if duration.elapsed().as_millis() >= 1_000 {
                    return Err(ODriveError::NoMessageReceived);
                }
            }
            let ch = buffer[0];
            if ch as char == '\n' {
                break;
            }

            string.push(ch as char);
        }

        Ok(string.trim().to_owned())
    }

    /// Reads the next message as a float. This will return zero if the message is not a valid
    /// float.
    ///
    /// It is suggested that you only use this if you are directly using the `Write` implementation
    /// and are expecting a response, as normally the supplied for the ODrive can directly support
    /// reading any response.
    pub fn read_float(&mut self) -> io::Result<Option<f32>> {
        Ok(self.read_string()?.map(|s| s.parse().unwrap_or_default()))
    }

    /// Reads the next message as an int. This will return zero if the message is not a valid int.
    ///
    /// It is suggested that you only use this if you are directly using the `Write` implementation
    /// and are expecting a response, as normally the supplied for the ODrive can directly support
    /// reading any response.
    pub fn read_int(&mut self) -> io::Result<Option<i32>> {
        Ok(self.read_string()?.map(|s| s.parse().unwrap_or_default()))
    }
}

impl<T> ODrive<T> where T: Write + Read {
    /// Move the motor to a position. Use this command if you have a real-time controller which
    /// is streaming setpoints and tracking a trajectory.
    /// `axis` The motor to be used for the operation.
    /// `position` is the desired position, in encoder counts.
    /// `velocity_feed_forward` is the velocity feed forward term, in encoder counts per second.
    /// `current_feed_forward` is the current feed forward term, in amps.
    /// If `None` is supplied for a feed forward input, zero will be provided as a default.
    pub fn set_position_p(&mut self, axis: AxisID, position: f32, velocity_feed_forward: Option<f32>,
                          current_feed_forward: Option<f32>) -> io::Result<()> {
        let velocity_feed_forward = velocity_feed_forward.unwrap_or_default();
        let current_feed_forward = current_feed_forward.unwrap_or_default();
        writeln!(self, "p {} {} {} {}", axis as u8, position, velocity_feed_forward, current_feed_forward)?;
        self.flush()
    }

    /// Move the motor to a position. Use this command if you are sending one setpoint at a time.
    /// `axis` The motor to be used for the operation.
    /// `position` is the desired position, in encoder counts.
    /// `velocity_limit` is the velocity limit, in encoder counts per second.
    /// `current_limit` is the current limit, in amps.
    /// If `None` is supplied for a limit, zero will be provided as a default.
    pub fn set_position_q(&mut self, axis: AxisID, position: f32, velocity_limit: Option<f32>,
                          current_limit: Option<f32>) -> io::Result<()> {
        let velocity_limit = velocity_limit.unwrap_or_default();
        let current_limit = current_limit.unwrap_or_default();
        writeln!(self, "q {} {} {} {}", axis as u8, position, velocity_limit, current_limit)?;
        self.flush()
    }

    /// Specifies a velocity setpoint for the motor.
    /// `axis` The motor to be used for the operation.
    /// `velocity` is the velocity setpoint, in encoder counts per second.
    /// `current_feed_forward` is the current feed forward term, in amps.
    /// If `None` is supplied for a feed forward input, zero will be provided as a default.
    pub fn set_velocity(&mut self, axis: AxisID, velocity: f32, current_feed_forward: Option<f32>) -> io::Result<()> {
        let current_feed_forward = current_feed_forward.unwrap_or_default();
        writeln!(self, "v {} {} {}", axis as u8, velocity, current_feed_forward)?;
        self.flush()
    }

    /// Specifies a velocity setpoint for the motor.
    /// `axis` The motor to be used for the operation.
    /// `current` is the current to be supplied, in amps.
    pub fn set_current(&mut self, axis: AxisID, current: f32) -> io::Result<()> {
        writeln!(self, "c {} {}", axis as u8, current)?;
        self.flush()
    }

    /// Moves a motor to a given position
    /// For general movement, this is the best command.
    /// `axis` The motor to be used for the operation.
    /// `position` is the desired position, in encoder counts.
    pub fn set_trajectory(&mut self, axis: AxisID, position: f32) -> io::Result<()> {
        writeln!(self, "t {} {}", axis as u8, position)?;
        self.flush()
    }
}

impl<T> ODrive<T> where T: Read + Write {
    /// Retrieves the velocity of a motor, in counts per second.
    pub fn get_velocity(&mut self, axis: AxisID) -> io::Result<Option<f32>> {
        writeln!(self, "r axis{} .encoder.vel_estimate", axis as u8)?;
        self.flush()?;
        self.read_float()
    }

    /// Changes the state of an axis.
    /// The `wait` flag indicates whether this command should block until the state is updated.
    /// Returns true unless we are in blocking mode and the operation times out.
    /// The current timeout is 10 seconds.
    ///
    /// This command will likely be deprecated and reworked in a future release.
    pub fn run_state(&mut self, axis: AxisID, requested_state: AxisState, wait: bool) -> io::Result<bool> {
        let timer = Instant::now();
        writeln!(self, "w axis{}.requested_state {}", axis as u8, requested_state as u8)?;
        self.flush()?;
        if wait {
            while {
                writeln!(self, "r axis{}.current_state", axis as u8)?;
                self.flush()?;

                self.read_int()?.unwrap_or_default() != AxisState::Idle as i32
                    && timer.elapsed().as_millis() < 10_000 // exit
            } {}
        }

        Ok(timer.elapsed().as_millis() < 10_000)
    }
}

// Implement helper methods
impl<T> ODrive<T> where T: Read + Write {
    pub fn set_config_property<D: Display>(&mut self, param: &str, value: D) -> ODriveResult<()> {
        writeln!(self, "w {} {}", param, value).map_err(ODriveError::Io)?;
        self.flush().map_err(ODriveError::Io)
    }

    pub fn get_config_property(&mut self, param: &str) -> ODriveResult<String> {
        writeln!(self, "r {}", param).map_err(ODriveError::Io)?;
        self.flush().map_err(ODriveError::Io)?;
        self.read_odrive_response()
    }

    pub fn set_axis_property<D: Display>(&mut self, axis: AxisID, property: &str, value: D) -> ODriveResult<()> {
        let config = format!("axis{}.{}", axis as u8, property);
        self.set_config_property(&config, value)
    }

    pub fn get_axis_property(&mut self, axis: AxisID, property: &str) -> ODriveResult<String> {
        let config = format!("axis{}.{}", axis as u8, property);
        self.get_config_property(&config)
    }

    pub fn set_axis_config_property<D: Display>(&mut self, axis: AxisID, name: &str, value: D) -> ODriveResult<()> {
        let config = format!("axis{}.config.{}", axis as u8, name);
        self.set_config_property(&config, value)
    }

    pub fn get_axis_config_property(&mut self, axis: AxisID, name: &str) -> ODriveResult<String> {
        let config = format!("axis{}.config.{}", axis as u8, name);
        self.get_config_property(&config)
    }
}

/// # Startup Configuration
/// The ODrive motor controllers have several optional startup procedures which can be enabled.
/// Each of them has an associated getter and setter which can be invoked to read to and write from
/// their value.
///
/// From the official documentation:
/// > By default the ODrive takes no action at startup and goes to idle immediately.
/// > In order to change what startup procedures are used, set the startup procedures you want to `true`.
/// > The ODrive will sequence all enabled startup actions selected in the order shown below.
///
/// > 1. `<axis>.config.startup_motor_calibration`
/// > 2. `<axis>.config.startup_encoder_index_search`
/// > 3. `<axis>.config.startup_encoder_offset_calibration`
/// > 4. `<axis>.config.startup_closed_loop_control`
/// > 5. `<axis>.config.startup_sensorless_control`
///
/// For further information, see the documentation for `AxisState`.
impl<T> ODrive<T> where T: Read + Write {
    pub fn set_startup_motor_calibration(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_config_property(axis, "startup_motor_calibration", value as u8)
    }

    pub fn set_startup_encoder_index_search(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_config_property(axis, "startup_encoder_index_search", value as u8)
    }

    pub fn set_startup_encoder_offset_calibration(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_config_property(axis, "startup_encoder_offset_calibration", value as u8)
    }

    pub fn set_startup_closed_loop_control(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_config_property(axis, "startup_closed_loop_control", value as u8)
    }

    pub fn set_startup_sensorless_control(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_config_property(axis, "startup_sensorless_control", value as u8)
    }

    pub fn read_startup_motor_calibration(&mut self, axis: AxisID) -> ODriveResult<bool> {
        let response = self.get_axis_config_property(axis, "startup_motor_calibration")?;
        match response.parse::<u8>() {
            Ok(val) => match val {
                0 => Ok(false),
                1 => Ok(true),
                _ => Err(ODriveError::InvalidMessageReceived(response))
            },
            Err(_error) => {
                Err(ODriveError::InvalidMessageReceived(response))
            }
        }
    }

    pub fn read_startup_encoder_index_search(&mut self, axis: AxisID, value: bool) -> ODriveResult<bool> {
        let response = self.get_axis_config_property(axis, "startup_encoder_index_search")?;
        match response.parse::<u8>() {
            Ok(val) => match val {
                0 => Ok(false),
                1 => Ok(true),
                _ => Err(ODriveError::InvalidMessageReceived(response))
            },
            Err(_error) => {
                Err(ODriveError::InvalidMessageReceived(response))
            }
        }
    }

    pub fn read_startup_encoder_offset_calibration(&mut self, axis: AxisID, value: bool) -> ODriveResult<bool> {
        let response = self.get_axis_config_property(axis, "startup_encoder_offset_calibration")?;
        match response.parse::<u8>() {
            Ok(val) => match val {
                0 => Ok(false),
                1 => Ok(true),
                _ => Err(ODriveError::InvalidMessageReceived(response))
            },
            Err(_error) => {
                Err(ODriveError::InvalidMessageReceived(response))
            }
        }
    }

    pub fn read_startup_closed_loop_control(&mut self, axis: AxisID, value: bool) -> ODriveResult<bool> {
        let response = self.get_axis_config_property(axis, "startup_closed_loop_control")?;
        match response.parse::<u8>() {
            Ok(val) => match val {
                0 => Ok(false),
                1 => Ok(true),
                _ => Err(ODriveError::InvalidMessageReceived(response))
            },
            Err(_error) => {
                Err(ODriveError::InvalidMessageReceived(response))
            }
        }
    }

    pub fn read_startup_sensorless_control(&mut self, axis: AxisID, value: bool) -> ODriveResult<bool> {
        let response = self.get_axis_config_property(axis, "startup_sensorless_control")?;
        match response.parse::<u8>() {
            Ok(val) => match val {
                0 => Ok(false),
                1 => Ok(true),
                _ => Err(ODriveError::InvalidMessageReceived(response))
            },
            Err(_error) => {
                Err(ODriveError::InvalidMessageReceived(response))
            }
        }
    }
}

/// Configuration management.
impl<T> ODrive<T> where T: Read + Write {
    /// Saves the current configuration of properties to the ODrives non-volatile memory, allowing
    /// the configuration to persist after reboots.
    pub fn save_configuration(&mut self) -> ODriveResult<()> {
        writeln!(self, "ss").map_err(ODriveError::Io)?;
        self.flush().map_err(ODriveError::Io)
    }

    /// Reset the current configuration to the factory default settings.
    pub fn erase_configuration(&mut self) -> ODriveResult<()> {
        writeln!(self, "se").map_err(ODriveError::Io)?;
        self.flush().map_err(ODriveError::Io)
    }
}

/// Motor configuration
impl<T> ODrive<T> where T: Read + Write {
    pub fn set_motor_pole_pairs(&mut self, axis: AxisID, value: u16) -> ODriveResult<()> {
        self.set_axis_property(axis, "motor.config.pole_pairs", value)
    }

    pub fn set_motor_resistance_calib_max_voltage(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "motor.config.resistance_calib_max_voltage", value)
    }

    pub fn set_motor_requested_current_range(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "motor.config.requested_current_range", value)
    }

    pub fn set_motor_current_control_bandwidth(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "motor.config.current_control_bandwidth", value)
    }

    pub fn set_motor_pre_calibrated(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_property(axis, "motor.config.pre_calibrated", value as u8)
    }
}

/// Encoder configuration
impl<T> ODrive<T> where T: Read + Write {
    pub fn set_encoder_mode(&mut self, axis: AxisID, value: EncoderMode) -> ODriveResult<()> {
        self.set_axis_property(axis, "encoder.config.mode", value as u8)
    }

    pub fn set_encoder_cpr(&mut self, axis: AxisID, value: u16) -> ODriveResult<()> {
        self.set_axis_property(axis, "encoder.config.cpr", value)
    }

    pub fn set_encoder_bandwidth(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "encoder.config.bandwidth", value)
    }

    pub fn set_encoder_pre_calibrated(&mut self, axis: AxisID, value: bool) -> ODriveResult<()> {
        self.set_axis_property(axis, "encoder.config.pre_calibrated", value as u8)
    }
}

/// Controller configuration
impl<T> ODrive<T> where T: Read + Write {
    pub fn set_position_gain(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "controller.config.pos_gain", value)
    }

    pub fn set_velocity_gain(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "controller.config.vel_gain", value)
    }

    pub fn set_velocity_integrator_gain(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "controller.config.vel_integrator_gain", value)
    }

    pub fn set_velocity_limit(&mut self, axis: AxisID, value: f32) -> ODriveResult<()> {
        self.set_axis_property(axis, "controller.config.vel_limit", value)
    }

    pub fn set_control_mode(&mut self, axis: AxisID, mode: ControlMode) -> ODriveResult<()> {
        self.set_axis_property(axis, "controller.config.control_mode", mode as u8)
    }
}