use std::io;

/// The `ODriveResult` type is used as a return type for operations which read to
/// or write from the ODrive.
pub type ODriveResult<T> = Result<T, ODriveError>;

#[derive(Debug)]
pub enum ODriveError {
    Axis(AxisError),
    Motor(MotorError),
    Encoder(EncoderError),
    Controller(ControllerError),
    /// Used when the ODrive sends us an invalid message.
    /// If you see this, file an issue.
    InvalidMessageReceived(String),
    NoMessageReceived,
    Io(io::Error)
}

#[repr(u16)]
#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone)]
pub enum AxisError {
    ErrorNone = 0x00,
    /// An invalid state was requested
    ErrorInvalidState = 0x01,
    ErrorDcBusUnderVoltage = 0x02,
    ErrorDcBusOverVoltage = 0x04,
    ErrorCurrentMeasurementTimeout = 0x08,
    /// The brake resistor was unexpectedly disarmed
    ErrorBrakeResistorDisarmed = 0x10,
    /// The motor was unexpectedly disarmed
    ErrorMotorDisarmed = 0x20,
    ErrorMotorFailed = 0x40,
    ErrorSensorlessEstimatorFailed = 0x80,
    ErrorEncoderFailed = 0x100,
    ErrorControllerFailed = 0x200,
    ErrorPosCtrlDuringSensorless = 0x400,
    ErrorWatchdogTimerExpired = 0x800,
}

#[repr(u16)]
#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone)]
pub enum MotorError {
    ErrorNone = 0,
    ErrorPhaseResistanceOutOfRange = 0x0001,
    ErrorPhaseInductanceOutOfRange = 0x0002,
    ErrorAdcFailed = 0x0004,
    ErrorDrvFault = 0x0008,
    ErrorControlDeadlineMissed = 0x0010,
    ErrorNotImplementedMotorType = 0x0020,
    ErrorBrakeCurrentOutOfRange = 0x0040,
    ErrorModulationMagnitude = 0x0080,
    ErrorBrakeDeadTimeViolation = 0x0100,
    ErrorUnexpectedTimerCallback = 0x0200,
    ErrorCurrentSenseSaturation = 0x0400,
    ErrorCurrentUnstable = 0x1000,
}

#[repr(u8)]
#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone)]
pub enum EncoderError {
    ErrorNone = 0,
    ErrorUnstableGain = 0x01,
    ErrorCprOutOfRange = 0x02,
    ErrorNoResponse = 0x04,
    ErrorUnsupportedEncoderMode = 0x08,
    ErrorIllegalHallState = 0x10,
    ErrorIndexNotFoundYet = 0x20,
}

#[repr(u8)]
#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone)]
pub enum ControllerError {
    ErrorNone = 0,
    ErrorOverspeed = 0x01,
}