# LogRotate Theory of Operation

## Introduction

This appendix describes the theory of operation for the `LogRotate` data model and its relationship with the `VendorLogFile` data model.

The `LogRotate` data model provides a mechanism to rotate vendor-specific log files. This is useful for managing log file sizes and preventing them from consuming too much disk space.

The `VendorLogFile` data model defines a list of vendor-specific log files that can be downloaded from the device by a remote management system e.g. USP Controller.

## How it works

The `LogRotate` data model can work independently, but it can also work on top of the `VendorLogFile` data model. To use `LogRotate` with `VendorLogFile`, you first need to consider the vendor log files that you want to rotate using the `VendorLogFile` data model.

Once the vendor log files are defined, you can configure the `LogRotate` data model to rotate them. The `LogRotate` data model provides several parameters for configuring log rotation, such as the maximum file size, the number of files to keep, and the rotation frequency.

When a log file (e.g., `my-log.log`) reaches a configured limit, the following rotation process occurs:

1.  The oldest rotated log file is deleted, only if the number of existing rotated files has reached `NumberOfFiles`. For example, if `NumberOfFiles` is 5, `my-log.log.5` is deleted.
2.  The remaining rotated log files are renamed, incrementing their numeric suffix. For example, `my-log.log.4` becomes `my-log.log.5`, `my-log.log.3` becomes `my-log.log.4`, and so on.
3.  The current log file is renamed to become the newest rotated log file. For example, `my-log.log` becomes `my-log.log.1`.
4.  A new, empty log file is created with the original name (e.g., `my-log.log`) to receive new log entries.

The `NumberOfFiles` parameter defines how many archived (rotated) log files are retained, not including the active log file itself.

## Examples

### Example 1: Basic Log Rotation

This example shows how to configure `LogRotate` to rotate a vendor log file based on its size.

1.  **Consider the vendor log file:**

    `Device.DeviceInfo.VendorLogFile.1.Name` = `/var/log/my-log.log`

2.  **Configure `LogRotate`:**

    `Device.DeviceInfo.LogRotate.1.Enable` = `true`\
    `Device.DeviceInfo.LogRotate.1.Name` = `file:///var/log/my-log.log`\
    `Device.DeviceInfo.LogRotate.1.MaxFileSize` = `1024`\
    `Device.DeviceInfo.LogRotate.1.NumberOfFiles` = `5`

In this example, `my-log.log` will be rotated when it reaches 1024 KB. The rotated files will be named `my-log.log.1`, `my-log.log.2`, ..., `my-log.log.5`. When a new rotated file needs to be created beyond the configured limit, `my-log.log.5` will be deleted to make room, ensuring that only the 5 most recent rotated log files are kept.

### Example 2: Time-based Log Rotation

This example shows how to configure `LogRotate` to rotate a vendor log file based on a time interval.

1.  **Consider the vendor log file:**

    `Device.DeviceInfo.VendorLogFile.2.Name` = `/var/log/another-log.log`

2.  **Configure `LogRotate`:**

    `Device.DeviceInfo.LogRotate.2.Enable` = `true`\
    `Device.DeviceInfo.LogRotate.2.Name` = `file:///var/log/another-log.log`\
    `Device.DeviceInfo.LogRotate.2.RollOver` = `1440`\
    `Device.DeviceInfo.LogRotate.2.NumberOfFiles` = `10`

In this example, `another-log.log` will be rotated every 1440 minutes (24 hours), as defined by the `RollOver` parameter which sets the maximum age of a log file before rotation. The rotated files will be named `another-log.log.1`, `another-log.log.2`, ..., `another-log.log.10`. When a new rotated file needs to be created beyond the configured limit, `another-log.log.10` will be deleted, ensuring that only the 10 most recent rotated log files are kept.

### Example 3: Log Rotation with Retention

This example shows how to configure `LogRotate` to rotate a log file and delete the rotated files after a certain period of time.

1.  **Consider the vendor log file:**

    `Device.DeviceInfo.VendorLogFile.3.Name` = `/var/log/debug-log.log`

2.  **Configure `LogRotate`:**

    `Device.DeviceInfo.LogRotate.3.Enable` = `true`\
    `Device.DeviceInfo.LogRotate.3.Name` = `file:///var/log/debug-log.log`\
    `Device.DeviceInfo.LogRotate.3.MaxFileSize` = `2048`\
    `Device.DeviceInfo.LogRotate.3.NumberOfFiles` = `10`\
    `Device.DeviceInfo.LogRotate.3.Retention` = `10080`

In this example, `debug-log.log` will be rotated when it reaches 2048 KB. The rotated files will be named `debug-log.log.1`, `debug-log.log.2`, ..., `debug-log.log.10`. When a new rotated file needs to be created beyond the configured limit, `debug-log.log.10` will be deleted. The `Retention` parameter, which defines the maximum time in minutes to keep rotated log files, will cause files older than 10080 minutes (7 days) to be deleted, regardless of the number of files.

### Example 4: Advanced Log Rotation

This example shows how to configure `LogRotate` to rotate a log file based on both size and time, with a retention policy.

1.  **Consider the vendor log file:**

    `Device.DeviceInfo.VendorLogFile.4.Name` = `/var/log/advanced-log.log`

2.  **Configure `LogRotate`:**

    `Device.DeviceInfo.LogRotate.4.Enable` = `true`\
    `Device.DeviceInfo.LogRotate.4.Name` = `file:///var/log/advanced-log.log`\
    `Device.DeviceInfo.LogRotate.4.MaxFileSize` = `4096`\
    `Device.DeviceInfo.LogRotate.4.RollOver` = `10080`\
    `Device.DeviceInfo.LogRotate.4.NumberOfFiles` = `20`\
    `Device.DeviceInfo.LogRotate.4.Retention` = `43200`

In this example, `advanced-log.log` will be rotated when it reaches 4096 KB or after 10080 minutes (7 days), whichever comes first. The `RollOver` parameter sets this maximum age for rotation. The rotated files will be named `advanced-log.log.1`, `advanced-log.log.2`, ..., `advanced-log.log.20`. When a new rotated file needs to be created beyond the configured limit, `advanced-log.log.20` will be deleted. Additionally, the `Retention` parameter, which defines the maximum time in minutes to keep rotated log files, will ensure that files older than 43200 minutes (30 days) are deleted, regardless of the number of files.
