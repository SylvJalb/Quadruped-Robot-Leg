// The `commands` module contains the ODrive structure, which is used to interact with the ODrive protocol.
pub mod commands;

// The `enumerations` module contains enums and constants related to different properties and errors.
pub mod enumerations;

/*
    * The `odrive` module contains all the public items that are used to interact with the ODrive protocol.
    * This includes the ODrive structure, enums and errors.
 */
pub mod odrive {
    pub use super::commands::ODrive;
    pub use super::enumerations::{AxisID, AxisState, EncoderMode, ControlMode, MotorType};
    pub use super::enumerations::errors::{ODriveError, EncoderError, AxisError, ControllerError, MotorError, ODriveResult};
}