from .config import (
    RealsenseCameraCfg,
    RealsenseD435CameraCfg,
    RealsenseL515CameraCfg,
    RealsenseCameraColorCfg,
    RealsenseCameraIMUCfg,
    RealsenseCameraEndpointCfg,
    RealsenseCameraDepthCfg,
    RealsenseSystemCfg,
    new_camera_config_by_device,
    new_camera_config_by_product_id,
    new_camera_config_by_name,
    new_system_config,
    get_device_by_cfg
)
from .record import (
    RealsenseSystemModel,
    RealsenseCameraModel,
    new_realsense_camera_system_from_config,
    new_realsense_camera_system_from_yaml_file,
    new_system_config,
)


class CALLBACKS:
    save_path_cb = "save_path_cb"
    tag_cb = "tag_cb"
    camera_friendly_name = "camera_friendly_name"

#
# CALLBACKS = Callbacks()